from scraper import JobScraper
import difflib

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os
from dotenv import load_dotenv
load_dotenv()

# Create the job file if it doesn't exist
with open("jobs.txt","a+") as f:
    f.write("")

# Scrape the jobs
scrape = JobScraper()
new_jobs = scrape.get_jobs()
scrape.driver.close()

# Save old jobs to compare later
old_file = []
with open('jobs.txt', 'r') as f:
    old_file = f.readlines()

# Write new jobs to file
with open('jobs.txt', 'w') as f:
    out_str = ''.join(new_jobs)
    f.write("%s" % out_str)

new_file = []
with open('jobs.txt', 'r') as f:
    new_file = f.readlines()

# Get the difference between the old and new jobs
differ = difflib.Differ()
diff = list(differ.compare(old_file, new_file))
changes = False

# Create the email message
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
    print("No changes... Exiting without sending email")
    exit(0)

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
exit(0)