from seleniumwire import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
import time
import os

delay=1
indexer=0

proxy='194.233.69.90'
port='443'

options = {
    'proxy': {
        'http': f'http://{proxy}:{port}',
        'https': f'https://{proxy}:{port}',
        'no_proxy': 'localhost,127.0.0.1'
    }
}

def userAgent():
    return {
        'Host': 'www.google.com',
        'User-Agent': UA[randNum(y=len(UA))],
        'Accept': driver.requests[cpaId].headers["accept"],
        'Accept-Language': driver.requests[cpaId].headers["accept-language"],
        'Referer': driver.requests[cpaId].headers["referer"],
        'Range': driver.requests[cpaId].headers["range"],
        'DNT': driver.requests[cpaId].headers["DNT"],
        'Alt-Used': driver.requests[cpaId].headers["alt-used"],
        'Connection': driver.requests[cpaId].headers["connection"],
        'Sec-Fetch-Dest': 'audio',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': "trailers"
    }

def randNum(x=0,y=100):
  return floor(random()*(y-x)+x)

def waitLoad(dst='container',sltr=By.ID,msg="Page is Ready!"):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((sltr, dst)))
        print(msg)
    except TimeoutException:
        print("Loading took too much time!")
        waitLoad(dst,sltr,msg)

def iframeLoad():
    try:
        time.sleep(5)
        driver.switch_to.frame(driver.find_element(By.XPATH,'//iframe[@title="reCAPTCHA"]'))
    except:
        iframeLoad()

driver=webdriver.Firefox(executable_path='/home/sicingik/geckodriver',seleniumwire_options=options)
driver.get("https://websiteseochecker.com/")

waitLoad("iframe",By.TAG_NAME)

iframeLoad()

waitLoad('//*[@id="recaptcha-anchor"]',By.XPATH,'element has load')
driver.find_element_by_xpath('//*[@id="recaptcha-anchor"]').click()

driver.switch_to.default_content()

time.sleep(5)

# waitLoad("iframe[title*='challenge'])",By.CSS_SELECTOR,'element has load')
driver.switch_to.frame(driver.find_element_by_css_selector('iframe[title*="challenge"]'))

# waitLoad('//*[@id="recaptcha-audio-button"]',By.XPATH,msg="element has load")
driver.find_element_by_xpath('//*[@id="recaptcha-audio-button"]').click()


print(driver.find_element_by_xpath('//audio[@id="audio-source"]').src)

# waitLoad('//*[@class="rc-audiochallenge-tdownload-link"]',By.XPATH,msg="element has load")
# # driver.find_element_by_xpath('//*[@class="rc-audiochallenge-tdownload-link"]').click()