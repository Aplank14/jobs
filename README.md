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
    pip install selenium
    pip install beautifulsoup4
    pip install secure-smtplib

## env
specify the following env vars. Recipients are comma delimited.

    EMAIL='<YOUR_EMAIL@gmail.com>'
    PASSWORD='<APP_PASSWORD_FOR_EMAIL>'
    RECIPIENT_EMAILS='recipient1@gmail.com,recipient2@gmail.com'

## run
Running once is simple with:

    python logger.py

On Windows you can setup a scheduled task with `Task Scheduler` to run the logger automatically.
1. Create a new task in `Task Scheduler`
2. Set trigger to be whatever frequency you wish
3. Action should be "Start a program" 
4. Program: `python.exe`
5. Arguments: C:\Users\path\to\jobs\logger.py
6. Start in: C:\Users\path\to\jobs\

## apply
:sob: