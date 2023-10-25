from scraper import JobScraper
import difflib

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os
from dotenv import load_dotenv
load_dotenv()

import argparse

def scrape(dev, func=None):

    # Init the job scraper
    scraper = JobScraper(dev)
    scraped_jobs=[]
    try:
        if (dev and func):
            # If running in -f mode only run one function. For testing only
            devFunc = getattr(scraper, func)
            scraped_jobs = devFunc()
        else:
            # Running normally, scrape all jobs
            scraped_jobs = scraper.get_jobs()
    except Exception as e:
        print("Scraping failure")
        print(e)
        exit(1)
    finally:
        scraper.driver.close()

    # Convert list to str and return
    return ''.join(scraped_jobs)

def saveToFileAndDiff(new_jobs):
    # Save old file contents to compare later
    old_file = []
    with open('jobs.txt', 'r') as f:
        old_file = f.readlines()

    # Write new jobs to file
    with open('jobs.txt', 'w') as f:
        f.write("%s" % new_jobs)

    # Get new file contents to compare to old
    new_file = []
    with open('jobs.txt', 'r') as f:
        new_file = f.readlines()

    # Get the difference between the old and new jobs
    differ = difflib.Differ()
    diff = list(differ.compare(old_file, new_file))

    return diff

def generateEmailMessage(diff, all_jobs):
    changes = False

    message_body = "Here is the job feed for today:\n\n"

    message_body += "\n----New Jobs----\n\n"
    for line in diff:
        if line.startswith('+ '):
            changes = True
            message_body += line

    message_body += "\n\n---Removed Jobs----\n\n"
    for line in diff:
        if line.startswith('- '):
            changes = True
            message_body += line

    message_body += "\n\n---All Jobs----\n"
    message_body += all_jobs

    if changes == False:
        return None

    return message_body

def sendMail(message_body):
    # Login to Gmail
    sender_email = os.environ.get("EMAIL")
    sender_password = os.environ.get("PASSWORD")
    recipient_emails = os.environ.get("RECIPIENT_EMAILS").split(",")

    # Send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        for recipient_email in recipient_emails:
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient_email
            msg["Subject"] = "Job Feed"
            msg.attach(MIMEText(message_body, "plain"))
            server.sendmail(sender_email, recipient_email, msg.as_string())

def main(args):

    # If running in dev mode for testing
    dev = (os.environ.get("DEV") == "True")

    # Get the jobs from the scraper. Calls scraper.py
    new_jobs = scrape(dev, args.func)

    # Save jobs to file for history. Get the diff from previous save.
    diff = saveToFileAndDiff(new_jobs)

    message_body = generateEmailMessage(diff, new_jobs)
    if message_body == None:
        print("No changes... Exiting without sending email")
        return

    if (args.noemail):
        print("Running in no email mode... Here are the email contents:\n", message_body)
    else:
        sendMail(message_body)
        print("Email sent successfully.")

if __name__ == "__main__":
    # Create the job file if it doesn't exist
    with open("jobs.txt","a+") as f:
        f.write("")

    # Initialize parser
    parser = argparse.ArgumentParser(prog='Job Scraper', description='A simple Selenium job scraper')
    parser.add_argument("-noemail", help = "No email mode", action = 'store_true')
    parser.add_argument("-func", type=str, help = "Only run one scraper function", required=False)
    args = parser.parse_args()

    # Start logger with arguments
    main(args)