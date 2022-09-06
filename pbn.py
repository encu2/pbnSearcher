from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
import os
import sys
import argparse

my_parser = argparse.ArgumentParser(description='List the content of a folder')

my_parser.add_argument('-L',
	                    metavar='Login Cred',
	                    action='store',
	                    type=str,
	                    help='Input Login Cred, Format:"Username:Password"')

my_parser.add_argument('-d',
	                    metavar="Domain(s)",
	                    action='store',
	                    type=str,
	                    help='Domain name (Up to 20 Keyword), Default = "domain"',
	                    nargs="?",
	                    default="domain")

my_parser.add_argument('-t',
	                    metavar='Time',
	                    action='store',
	                    type=int,
	                    help='Choose: \
	                    1 (2 week ago), 2 (a month ago), 3 (2 months ago), \
	                    and 4 (3 months ago), Default = 2',
	                  	choices=[1,2,3,4], 
	                  	default=False)

my_parser.add_argument('-x',
	                    metavar='Exclude Name',
	                    action='store',
	                    type=str,
	                    help='Exclude domain name (Up to 20 Keyword)',
	                    nargs="?",
	                    default=False)

my_parser.add_argument('-c',
	                    metavar='Crawl Count',
	                    action='store',
	                    type=int,
	                    help='Crawl count on Archive.org',
	                    default=False)

my_parser.add_argument('-b',
	                    metavar='Backlinks',
	                    action='store',
	                    type=int,
	                    help='Min. Total Backlinks on a domain', 
	                    default=False)

my_parser.add_argument('-i',
						'--interactive',
	                    action='store_true',
	                    default=False)

args = my_parser.parse_args()

print(__file__)

options = Options()
options.headless = True
driver=webdriver.Firefox(executable_path=__file__.replace('pbn.py','geckodriver'),options=options) #headless option
# driver=webdriver.Firefox(executable_path='/home/sicingik/geckodriver')
driver.get("https://www.expireddomains.net/login/")
delay = 15 # seconds
z=1
title=0
page=""
domainName=args.d
timeExp=args.t
crawlMin=str(args.c)
minBl=str(args.b)
exKw=args.x

#log cred
if args.L==None:
	print("Anda belum memasukkan Data Login, Silahkan Coba Lagi")
	exit()
elif args.L.find(":")==-1:
	print("Format Login Yang Anda Masukkan Salah, Silahkan Coba Lagi")
	exit()
loginCred=args.L.split(":")


#request input interactive start
if args.interactive==True:


	print('''
Masukkan data login ke akun expireddomain.net
		''')
	loginCred=input("Format Input, Username:Password >")
	if loginCred.find(":")==-1:
		print("Format Login Yang Anda Masukkan Salah, Silahkan Coba Lagi")
		exit()
	print('''
Sebelum pencarian expired domain, silahkan masukkan kata kunci
dengan contoh:

Single kata kunci
input : murah 
hasil : murahmobilbaru.com, rumahmurah.com, ...

multiple kata kunci (untuk memisahkan masing-masing kata kunci
gunakan space, max 30 kata kunci)
input : murah travel sendok motor
hasil : barangmewahmurah.com, outdoortravel.com, thesendoks.com, motormotors.com, ...
		''')
	domainName=input("Masukkan Kata Kunci Disini: \n")

	print('''
Pilih jangka Waktu yang dipilih untuk mencari expired domain:
1. 14 hari
2. 30 hari
3. 60 hari
4. 90 hari

Pilih berdasarkan angka list (tidak boleh memasukkan multiple input), contoh:

input: 2
		''')
	timeExp=input("Masukkan Jangka Waktu yang Dipilih: \n")

	print('''
Tentukan minimal berapa kali sebuah domain sudah di crawl oleh
Archive.org (Rekomendasi 2)(optional, langsung tekan enter untuk melewati)

Contoh:
Input: 4
	''')
	crawlMin=input("Masukkan Min. Crawl di Archive.org Disini: \n") or False

	print('''
Masukkan minimal jumlah backlink yang sudah tertaut di sebuah domain.
(Rekomendasi 100)(optional, langsung tekan enter untuk melewati)

Contoh:
Input: 250
		''')
	minBl=input("Masukkan Min. Backlink yang sudah tertaut: \n") or False

	print('''
Tentukan kata-kata yang tidak akan ditampilkan ketika pencarian Expired Domain.
(optional, langsung tekan enter untuk melewati)

Single kata kunci:
input: pembalut

Multiple kata kunci:
input: tipi sosis telur becek misuh
		''')
	exKw=input("Masukkan Kata Kunci yang Tidak Ingin Ditampilkan Disini: \n") or False


#request input from user end

def load():
	try:
		after=driver.find_element(By.CLASS_NAME,"pageinfo").text
		time.sleep(3)
	except:
		time.sleep(5)
		after=driver.find_element(By.CLASS_NAME,"pageinfo").text

	print("still load")
	if now==after:
		load()	

def waitLoad(dst='container',sltr=By.ID,msg="Page is Ready!"):
	try:
		myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((sltr, dst)))
		print(msg)
	except TimeoutException:
		print("Loading took too much time!")
		waitLoad()

def collectData():
	global now,z,page

	v=driver.find_elements(By.XPATH, "//a[@class='namelinks']")

	try:
		now=driver.find_element(By.CLASS_NAME,"pageinfo").text
	except:
		waitLoad("pageinfo",By.CLASS_NAME,"Credential Info Successfully Load")
		now=driver.find_element(By.CLASS_NAME,"pageinfo").text

	page+=now
	print("Process Now In Page "+ str(z) + " of " + page.split(" ")[3])
	for i in v:
		f.write(i.get_attribute("title")+"\n")

	try:
		# just=driver.find_element(By.CLASS_NAME,"pageinfo").text
		driver.find_element(By.CLASS_NAME,"next").click()
	except:
		return True
	waitLoad("dotted",By.CLASS_NAME,"Successfully get the links")
	load()
	z+=1
	collectData()
	
	

waitLoad()

# login section start
driver.find_element_by_id("inputLogin").send_keys(loginCred[0])
driver.find_element_by_id("inputPassword").send_keys(loginCred[1])
driver.find_element(By.XPATH,"//button[text()='Login']").click()
# login section end

waitLoad()

if str(driver.current_url) == "https://www.expireddomains.net/login/?error=1":
	print("Your Login Wrong, Please Try Again")
	exit()
else:
	driver.get("https://member.expireddomains.net/domains/expiredcom/")

waitLoad('showfilter',By.CLASS_NAME)

# delete .com page start
#1 filter start
driver.find_element(By.XPATH,"//a[text()='Show Filter']").click()
driver.find_element(By.XPATH,"//input[@name='fdomain']").send_keys(domainName)

#Optional filter input start
if exKw!="False":
	driver.find_element(By.XPATH,"//input[@name='fdomainnot']").send_keys(exKw)

if minBl!="False":
	driver.find_element(By.XPATH,"//input[@id='fbl']").send_keys(minBl)

if crawlMin!="False":
	driver.find_element(By.XPATH,"//input[@id='facr']").send_keys(crawlMin)

while timeExp:
	if len(str(timeExp))<2:
		if int(timeExp)>4 or int(timeExp)<1:
			print("Input yang Anda Masukkan Salah")
			exit()
		elif timeExp=="1":
			driver.find_element(By.XPATH,"//input[@name='flast14d']").click()
		elif timeExp=="2":
			driver.find_element(By.XPATH,"//input[@name='flast30d']").click()
		elif timeExp=="3":
			driver.find_element(By.XPATH,"//input[@name='flast60d']").click()
		elif timeExp=="4":
			driver.find_element(By.XPATH,"//input[@name='flast90d']").click()
		break
	else:
		exit()
#Optional filter input end

driver.find_element(By.XPATH,"//input[@id='fwhois']").click()

# time.sleep(1)
# driver.find_element(By.XPATH,"//input[@id='fwhois']").send_keys(Keys.ENTER)
driver.find_element(By.CSS_SELECTOR,"input[value='Apply Filter']").click()
time.sleep(1)
waitLoad("next",By.CLASS_NAME,"Filter applied")

#filter end

#2 get url from list
try:
	f=open("listBl.txt","w+")
except:
	f=open("listBl.txt","w+")

# while True:
# 	if z==1:
# 		break

collectData()

print("finish get all links")
#get url from list end


f.close()
driver.quit()