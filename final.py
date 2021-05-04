#importing webdriver from selenium
from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import etree
import requests
import csv
from bs4 import BeautifulSoup
from lxml import etree
import requests
import urllib.request  as urllib2 
import mysql.connector
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary #We import this so we can specify the Firefox browser binary location
import os

FF_options = webdriver.FirefoxOptions()
FF_profile = webdriver.FirefoxProfile()
FF_options.add_argument("-headless")
FF_profile.update_preferences()

def insert_varibles_into_table(heading, image, state_name, table_heading, pincode):
    try:
        connection = mysql.connector.connect(host="167.71.157.189",user="bingdb",password="Sahil@41212",database="bingdb")
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO tax (heading, image, state_name, table_heading, pincode) 
                                VALUES (%s, %s, %s, %s, %s) """

        record = (heading, image, state_name, table_heading, pincode)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Record inserted successfully into  table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


f = open("allmainurl.txt", "r")
for x in f:
	URL = x
	HEADERS = ({'User-Agent':
	            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
	            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
	            'Accept-Language': 'en-US, en;q=0.5'})
	   
	#selecting Firefox as the browser
	#in order to select Chrome 
	# webdriver.Chrome() will be used

	# driver = webdriver.Firefox(executable_path = 'geckodriver')
	driver = webdriver.Firefox(options=FF_options, firefox_profile=FF_profile, executable_path=os.environ.get("GECKODRIVER_PATH"), firefox_binary=FirefoxBinary(os.environ.get("FIREFOX_BIN")))

	#URL of the website 
	
	   
	#opening link in the browser
	driver.get(URL)
	# driver.execute_script("""//select//option[last()].value ='5000'""")
	driver.execute_script("""document.getElementsByTagName('option')[0].value='500000';""")
	

	element = driver.find_element_by_xpath("//option[@value='500000']")
	element.click()
	webpage = requests.get(URL, headers=HEADERS)
	soup = BeautifulSoup(webpage.content, "html.parser")
	dom = etree.HTML(str(soup))
	school_name_path = dom.xpath('//a[not(@class)]/@href')
	for x in range(len(school_name_path)):
		if school_name_path[x].find("http") != -1:
			print(school_name_path[x])	
			inner_URL = school_name_path[x] 
			inner_HEADERS = ({'User-Agent':
				'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
				(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
				'Accept-Language': 'en-US, en;q=0.5'})
			webpage = requests.get(inner_URL, headers=inner_HEADERS)
			soup = BeautifulSoup(webpage.content, "html.parser")
			dom = etree.HTML(str(soup))
			#print(dom.xpath('//ul[3]//li').text)
			pincode = dom.xpath('//div[contains(@class,"bottom-spaced")]//div//a/text()')

			heading = dom.xpath('//h1[contains(@class,"heading")]/text()')

			image = dom.xpath('//h1[contains(@class,"heading")]//img/@src')


			table_heading =dom.xpath('//table[contains(@class,"table")]//td/a/text()')

			table_per =dom.xpath('//table[contains(@class,"table")]//td[not(div)]/text()')

			state_name =dom.xpath('//ol[contains(@class,"breadcrumb")]//li[2]/a/text()')
			table_data = []



			for x in range(len(table_heading)):
				table_data.append(table_heading[x] + "!!" + table_per[x])

			all_heading  = ''.join(str(e) for e in heading)
			all_image = '|'.join(str(e) for e in image)
			r = requests.get("https://www.sales-taxes.com/" + all_image)
			all_tableheading = '|'.join(str(e) for e in table_data)
			all_pincode = '|'.join(str(e) for e in pincode)
			all_statename = '|'.join(str(e) for e in state_name)

			insert_varibles_into_table(all_heading, r.text, all_statename, all_tableheading, all_pincode)















   	
	driver.quit()


 