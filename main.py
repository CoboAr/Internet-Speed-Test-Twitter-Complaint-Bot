from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, os

# Promised internet speed
PROMISED_DOWN=150
PROMISED_UP=100

# Environment variabled
TWITTER_EMAIL = os.environ.get("EMAIL")
TWITTER_PASSWORD = os.environ.get("PASSWORD")
TWITTER_USERNAME = os.environ.get("USERNAME")

class InternetSpeedTwitterBot:

    def __init__(self):
        self.chromeoptions = webdriver.ChromeOptions ()
        self.chromeoptions.add_experimental_option ("detach", True)
        self.driver = webdriver.Chrome ( options=self.chromeoptions)
        self.up=0
        self.down=0
        self.internet_provider_name=""

    def get_internet_speed(self):
        self.driver.get (url="https://www.speedtest.net/")
        time.sleep (3)
        start_test_button = self.driver.find_element(by=By.XPATH, value="//*[@id='container']/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]")
        time.sleep(3)
        start_test_button.click()
        time.sleep(60)
        self.down=self.driver.find_element(by=By.XPATH, value="//*[@id='container']/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span")
        self.down=float(self.down.text)
        print (f"Download: {self.down}")
        self.up=self.driver.find_element(by=By.XPATH, value="//*[@id='container']/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span")
        self.up=float(self.up.text)
        print(f"Upload: {self.up}")
        # Internet provider name
        self.internet_provider_name = self.driver.find_element (by=By.XPATH,
                                                  value="//*[@id='container']/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[4]/div/div/div[1]/div[3]/div[2]").text

        print(f"Inter provider name is: {self.internet_provider_name}")

    def tweet_at_provider(self):
        self.driver.get(url="https://twitter.com/i/flow/login")
        time.sleep(5)
        # Login to twitter
        email=self.driver.find_element(by=By.XPATH, value="//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input")
        # Insert email
        email.send_keys(TWITTER_EMAIL)
        time.sleep(2)
        # Next button
        next=self.driver.find_element(by=By.XPATH, value="//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div/span/span")
        next.click()
        time.sleep(5)
        # Insert username
        username = self.driver.find_element(by=By.XPATH, value="//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input")
        username.send_keys(TWITTER_USERNAME)
        # Next button
        next = self.driver.find_element(by=By.XPATH, value="//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/span/span")
        next.click()
        time.sleep (2)
        # Insert password
        password=self.driver.find_element(by=By.XPATH, value="//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input")
        password.send_keys(TWITTER_PASSWORD)
        # Click login
        login=self.driver.find_element(by=By.XPATH, value="//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div/span/span")
        login.click()
        time.sleep(5)
        # #cancel notification table
        # cancel=self.driver.find_element(By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[2]/div/span/span")
        # cancel.click()
        # time.sleep(3)

        #write tweet
        post=self.driver.find_element(by=By.CSS_SELECTOR, value='br[data-text="true"]')
        TWEET_text = f"Hey @{self.internet_provider_name}, why is my internet speed\n test {self.down}down/{self.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?"
        post.send_keys(TWEET_text)
        time.sleep(3)
        #post it
        tweet=self.driver.find_element(by=By.XPATH, value="//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/span/span")
        tweet.click()

        time.sleep(10)
        self.driver.quit()


bot=InternetSpeedTwitterBot()
bot.get_internet_speed()
bot.tweet_at_provider()