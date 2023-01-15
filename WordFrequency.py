import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

QUERY_URL = 'https://www.google.com/search?q={}&aqs=edge..69i57l2j69i59l2j69i61l3.837j0j4&sourceid=chrome&ie=UTF-8'
HEADERS = {
	'sec-ch-ua-arch': '"x86"',
	'sec-ch-ua-bitness': '"64"',
	'sec-ch-ua-full-version': '"109.0.1518.49"',
	'sec-ch-ua-full-version-list': '"Not_A Brand";v="99.0.0.0", "Microsoft Edge";v="109.0.1518.49", "Chromium";v="109.0.5414.87"',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-model': '""',
	'sec-ch-ua-platform': '"Windows"',
	'sec-ch-ua-platform-version': '"10.0.0"',
	'sec-ch-ua-wow64': '?0',
	'sec-fetch-dest': 'document',
	'sec-fetch-mode': 'navigate',
	'sec-fetch-site': 'same-origin',
	'sec-fetch-user': '?1',
	'upgrade-insecure-requests': '1',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

def parseResponse(res):
	s = BeautifulSoup(res.text, 'html.parser')
	stats = s.find('div', {'id': 'result-stats'})

	text = stats.text.split(':')[1]
	text = text.split('(')[0].strip()
	text = text.replace('\xa0', '')
	return int(text)

def getFrequency(word, session):
	url = QUERY_URL.format(word)
	res = session.get(url, headers=HEADERS)
	return parseResponse(res)

def doConsent():
	# driver
	driver = webdriver.Edge() # TODO: the driver give a bunch of errors
	driver.get('https://www.google.com')

	buttons = driver.find_elements(By.XPATH, "//button")
	button = [b for b in buttons if b.text == 'Přijmout vše'][0]
	button.click()
	
	cookies = driver.get_cookies()
	session = requests.Session()
	for cookie in cookies:
		session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
	driver.quit()
	return session

session = doConsent()
f = getFrequency('maso', session)
print(f)
