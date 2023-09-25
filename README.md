# job-scraper
A selenium based web scraper to automate job searching. Basic flow is as follows:
1. Setup selenium bot to open whatever company page you wish to track.
2. Use beautiful soup to extract information from the page.
3. Filter down to jobs you are interested in.
4. Create diff and send an email to notify recipients of new postings. 

`scraper.py` contains selenium driver, code to direct selenium to company page, and code to download company job postings with beautiful soup.

`logger.py` instantiates scraper, gets job data, writes data to `jobs.txt` file to track diff, then emails recipients if there are new postings based on file diff.

## download
    git clone https://github.com/Aplank14/jobs.git

## dependencies
    pip install -r requirements.txt

## env
Specify the following env vars. Recipients are comma delimited. When running locally, `DEV` should probably be set to `True`.

    DEV='<True_or_False>'
    EMAIL='<YOUR_EMAIL@gmail.com>'
    PASSWORD='<APP_PASSWORD_FOR_GMAIL>'
    RECIPIENT_EMAILS='recipient1@gmail.com,recipient2@gmail.com'

## run
Running once is simple with:

    python logger.py

To run without sending an email:

    python logger.py -n

For development, set the environment variable `DEV` to `True`. Then, you can test a single scraper function name using the following:

    python logger.py -f discord

To recieve email alerts you can set it to run periodically automatically on a local machine or Github actions. For local automation with Linux just use crontab. On Windows you can setup a scheduled task with `Task Scheduler` to run the logger automatically. 
1. Create a new task in `Task Scheduler`
2. Set trigger to be whatever frequency you wish
3. Action should be "Start a program" 
4. Program: `python.exe`
5. Arguments: C:\Users\path\to\jobs\logger.py
6. Start in: C:\Users\path\to\jobs\

It is even easier to run periodically using Github actions! All you have to do is fork this repository, create an environment called `bot`, then set the enviornment variables described above.

## apply
:sob:
