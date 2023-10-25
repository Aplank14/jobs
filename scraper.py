from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller

from pyvirtualdisplay import Display

class JobScraper:
    def __init__(self, dev):
        self.bad_titles = []
        with open('deny.txt', 'r') as file:
            self.bad_titles = [line.strip() for line in file]
        
        if not dev:
            chromedriver_autoinstaller.install() 
            display = Display(visible=0, size=(800, 800))  
            display.start()

        chrome_options = webdriver.ChromeOptions()    
        options = [
            "--window-size=1200,1200",
            "--ignore-certificate-errors"   
            "--headless",
        ]

        for option in options:
            chrome_options.add_argument(option)

        self.driver = webdriver.Chrome(options = chrome_options)
        self.wait = WebDriverWait(self.driver, 10)


    def filter_jobs(self, i):
        for title in self.bad_titles:
            if title in i:
                return False
        return True

    def wait_and_click(self, xpath):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        btn = self.driver.find_element(By.XPATH, xpath)
        btn.click()

    def get_jobs(self):
        return self.spotify() + self.discord() + self.remitly() + self.paylocity() + self.reddit() + self.turnitin() + self.zillow() + self.pintrest() + self.onepassword() + self.capitalone() + self.salesforce()

    def spotify(self):
        url = 'https://lifeatspotify.com/jobs?l=remote-americas&l=remote-emea&l=remote-estamericas-remote&c=backend&c=client-c&c=data&c=developer-tools-infrastructure&c=engineering-leadership&c=machine-learning&c=mobile&c=network-engineering-it&c=security&c=tech-research&c=web'
        self.driver.get(url)

        try:
            self.wait_and_click("//button[text()='Load more jobs']")
        except Exception:
            print("Spotify element took too long to load or was not found.")

        html = self.driver.page_source
        soup = BeautifulSoup(html.lower(), "html.parser")
        listings = soup.find_all('a', href=lambda href: href and "/jobs/" in href)

        jobs = ['\nSpotify:\n']
        for job in listings:
            if self.filter_jobs(job.text):
                jobs.append("Spotify " + job.text + "\n" + "https://lifeatspotify.com" + job['href'] + "\n")

        return jobs

    def discord(self):
        url = 'https://discord.com/careers'
        self.driver.get(url)

        try:
            self.wait_and_click("//a[@data-department-name='Product Engineering']")
        except Exception:
            print("Discord element took too long to load or was not found.")

        html = self.driver.page_source
        soup = BeautifulSoup(html.lower(), "html.parser")
        listings = soup.find_all('a', href=lambda href: href and "/jobs/" in href)

        jobs = ['\nDiscord:\n']
        for job in listings:
            name = job.find('h3').text
            if self.filter_jobs(name):
                jobs.append("Discord " + name + "\n" + "https://discord.com" + job['href'] + "\n")
        return jobs

    def remitly(self):
        url = 'https://remitly.wd5.myworkdayjobs.com/Remitly_Careers?jobFamilyGroup=c9699b32e2da1029a051260e906d0000&locationCountry=bc33aa3152ec42d4995f4791a106ed09&timeType=56d53b9ae3a1102534c884fb37ef0001'
        self.driver.get(url)

        html = self.driver.page_source
        soup = BeautifulSoup(html.lower(), "html.parser")
        listings = soup.find_all('a', href=lambda href: href and "/job/" in href)

        jobs = ['\nRemitly:\n']
        for job in listings:
            if self.filter_jobs(job.text):
                jobs.append("Remitly " + job.text + "\n" + "https://remitly.wd5.myworkdayjobs.com" + job['href'] + "\n")
        return jobs


    def paylocity(self):
        url = 'https://www.paylocity.com/careers/product-technology/'
        self.driver.get(url)

        try:
            self.wait_and_click("//span[text()='filter by location']")
            self.wait_and_click("//button[@title='Remote, US']")
            self.wait_and_click("//a[@aria-label='show 30 results per page']")
        except Exception:
            print("Paylocity element took too long to load or was not found.")

        html = self.driver.page_source
        soup = BeautifulSoup(html.lower(), "html.parser")
        listings = soup.find_all('div', class_='jobs-availability-div')

        jobs = ['\nPaylocity:\n']
        for job in listings:
            name = job.a.div.text
            if self.filter_jobs(name):
                jobs.append("Paylocity " + name + "\n" + job.a['href'] + "\n")

        return jobs

    def reddit(self):
        url = 'https://www.redditinc.com/careers/'
        self.driver.get(url)

        try:
            self.wait_and_click("//h3[text()='Engineering']")
        except Exception:
            print("Reddit element took too long to load or was not found.")

        html = self.driver.page_source
        soup = BeautifulSoup(html.lower(), "html.parser")
        listings = soup.find_all('a', href=lambda href: href and "/jobs/" in href)

        jobs = ['\nReddit:\n']
        for job in listings:
            name = job.div.text
            if self.filter_jobs(name):
                jobs.append("Reddit " + name + "\n" + job['href'] + "\n")

        return jobs


    def turnitin(self):
        url = 'https://careers.smartrecruiters.com/TurnitinLLC?search=software&remoteLocation=true'
        self.driver.get(url)

        html = self.driver.page_source
        soup = BeautifulSoup(html.lower(), "html.parser")
        listings = soup.find_all('a', href=lambda href: href and "https://jobs.smartrecruiters.com/turnitinllc/" in href)

        jobs = ['\nTurnItIn:\n']
        for job in listings:
            name = job.h4.text
            if "(usa remote)" not in name:
                continue
            if self.filter_jobs(name):
                jobs.append("TurnItIn " + name + "\n" + job['href'] + "\n")

        return jobs
    
    def onepassword(self):
        url = 'https://jobs.lever.co/1password?workplaceType=remote&location=Remote%20%28US%20or%20Canada%29'
        self.driver.get(url)

        html = self.driver.page_source
        soup = BeautifulSoup(html.lower(), "html.parser")

        # Filter the div elements based on their children's text content
        listings = soup.find_all('a', href=lambda href: href and "https://jobs.lever.co/1password/" in href)

        jobs = ['\n1Password:\n']
        for job in listings:
            if job.h5 == None: continue
            name = job.h5.text
            # Special filter for 1password
            if "designer" in name or "analyst" in name: continue
            if self.filter_jobs(name):
                jobs.append("1Password " + name + "\n" + job['href'] + "\n")

        return jobs
    
    def pintrest(self):
        url = 'https://www.pinterestcareers.com/en/jobs/?search=engineer&team=Engineering&type=Regular&remote=true&pagesize=50#results'
        self.driver.get(url)

        html = self.driver.page_source
        soup = BeautifulSoup(html.lower(), "html.parser")
        listings = soup.find_all('a', class_='js-view-job')

        jobs = ['\nPintrest:\n']
        for job in listings:
            name = job.text
            if self.filter_jobs(name):
                jobs.append("Pintrest " + name + "\n" + "https://www.pinterestcareers.com" + job['href'] + "\n")

        return jobs
    
    def salesforce(self):
        url = 'https://careers.salesforce.com/en/jobs/?search=&country=United+States+of+America&location=Remote&location=Indianapolis&location=Chicago&team=Software+Engineering&pagesize=50#results'
        self.driver.get(url)
        
        html = self.driver.page_source
        soup = BeautifulSoup(html.lower(), "html.parser")
        listings = soup.find_all('a', class_='js-view-job')

        jobs = ['\nSalesforce:\n']
        for job in listings:
            name = job.text
            if self.filter_jobs(name):
                jobs.append("Salesforce " + name + "\n" + "https://careers.salesforce.com" + job['href'] + "\n")

        return jobs
    
    def zillow(self):
        url = 'https://zillow.wd5.myworkdayjobs.com/Zillow_Group_External?locations=bf3166a9227a01f8b514f0b00b147bc9&jobFamilyGroup=a90eab1aaed6105e8dd41df427a82ee6'
        self.driver.get(url)

        html = self.driver.page_source
        soup = BeautifulSoup(html.lower(), "html.parser")
        listings = soup.find_all('a', attrs={"data-automation-id": "jobTitle"})

        jobs = ['\nZillow:\n']
        for job in listings:
            name = job.text
            if self.filter_jobs(name):
                jobs.append("Zillow " + name + "\n" + "https://zillow.wd5.myworkdayjobs.com/" + job['href'] + "\n")

        return jobs
    
    def capitalone(self):
        url = 'https://www.capitalonecareers.com/category/engineering-jobs/234/29016/1'
        self.driver.get(url)

        try:
            self.wait_and_click("//button[@id='custom_fields.remote-toggle']")
            self.wait_and_click("//input[@data-display='Remote']")
            self.wait_and_click("//input[@data-display='Remote Eligible']")
        except Exception:
            print("CapitalOne element took too long to load or was not found.")

        html = self.driver.page_source
        soup = BeautifulSoup(html.lower(), "html.parser")
        listings = soup.find_all('a')

        jobs = ['\nCapitalOne:\n']
        for job in listings:
            if not job.has_attr('data-job-id'): continue
            name = job.h2.text
            if self.filter_jobs(name):
                jobs.append("CapitalOne " + name + "\n" + "https://www.capitalonecareers.com" + job['href'] + "\n")

        return jobs
    