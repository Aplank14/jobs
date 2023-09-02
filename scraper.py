from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class JobScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 20)
        self.bad_titles = ['senior', 'lead', 'principal', 'staff', 'manager', 'director', 'specialist', 'assistant', 'analyst', 'sr.', 'iii', 'representative', 'counsel', 'bilingual', 'associate emea', 'head', 'manger', 'coordinator', 'europe', 'asia']

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
        return self.spotify() + self.discord() + self.remitly() + self.paylocity() + self.reddit() + self.turnitin()

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
        url = 'https://remitly.wd5.myworkdayjobs.com/Remitly_Careers'
        self.driver.get(url)

        try:
            self.wait_and_click("//button[@data-automation-id='distanceLocation']")
            self.wait_and_click("//label[@for='82e0c5da80581000d124020d6a840000']")
            self.wait_and_click("//button[@data-automation-id='jobFamilyGroup']")
            self.wait_and_click("//label[@for='c9699b32e2da1029a051260e906d0000']")
        except Exception:
            print("Remitly element took too long to load or was not found.")

        html = self.driver.page_source
        soup = BeautifulSoup(html.lower(), "html.parser")
        listings = soup.find_all('a', href=lambda href: href and "/job/" in href)

        jobs = ['\nRemitly:\n']
        for job in listings:
            if self.filter_jobs(job.text):
                jobs.append("Remitly " + job.text + "\n" + "https://careers.remitly.com" + job['href'] + "\n")
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
        url = 'https://careers.smartrecruiters.com/TurnitinLLC'
        self.driver.get(url)

        try:
            self.wait_and_click("//input[@id='remoteLocationFilter']")
        except Exception:
            print("Turnitin element took too long to load or was not found.")

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

