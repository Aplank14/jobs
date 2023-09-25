from scraper import JobScraper
import difflib

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os
from dotenv import load_dotenv
load_dotenv()

import argparse

def generateEmailMessage(diff, out_str):
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
    message_body += out_str

    if changes == False:
        return None

    return message_body

def scrape(dev, func=None):

    # Scrape the jobs
    scraper = JobScraper(dev)
    scraped_jobs=[]
    try:
        if (dev and func):
            devFunc = getattr(scraper, func)
            scraped_jobs = devFunc()
        else:
            scraped_jobs = scraper.get_jobs()
    except Exception as e:
        with open("log.txt","a+") as f:
            f.write(e)
        print("Scraping failure")
        exit(1)
    finally:
        scraper.driver.close()
    return scraped_jobs

def logJobs(args):

    dev = (os.environ.get("DEV") == "True")

    new_jobs = scrape(dev, args.func)
    out_str = ''.join(new_jobs)

    # Save old file contents to compare later
    old_file = []
    with open('jobs.txt', 'r') as f:
        old_file = f.readlines()

    # Write new jobs to file
    with open('jobs.txt', 'w') as f:
        f.write("%s" % out_str)

    # Get new file contents to compare to old
    new_file = []
    with open('jobs.txt', 'r') as f:
        new_file = f.readlines()

    # Get the difference between the old and new jobs
    differ = difflib.Differ()
    diff = list(differ.compare(old_file, new_file))

    message_body = generateEmailMessage(diff, out_str)
    if message_body == None:
        print("No changes... Exiting without sending email")
        return

    if (args.noemail):
        print("Running in no email mode... Here are the email contents:\n", message_body)
        return

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
    logJobs(args)