
# import package
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
print("import library sucessful")

# open website
url = 'https://propzy.vn/'
browser = webdriver.Chrome()
sleep(2)
browser.get(url)

# searching
search_field = browser.find_element_by_xpath('/html/body/div[1]/section[1]/div[2]/div/div/div[2]/div/div/div/div[1]/div/div[2]/div/input') 
search_query = input('Enter address you want to search?\n')
search_field.send_keys(search_query)
sleep(2)
search_field.send_keys(Keys.RETURN)
sleep(2)

# bs4
soup = BeautifulSoup(browser.page_source, 'lxml')
list_houses = soup.find_all('div', class_='item-listing listing-card view-as-grid item-compare')
# print(list_estates)
data_real_estate = []
sleep(2)

# crawl
input_page = int(input('How many pages you want to scrape: '))
for page in range(input_page):
    for house in list_houses:
        data_house = {
            'title': '',
            'address': '',
            'price': '',
            'area': '',
        }
        try:
            title = house.find('p', class_='p-info-listing').text
            address = house.find('p', class_='p-location').text
            title_price = house.find('h3', class_='h3-title-price').text
            price = title_price.split()[0]+' tỷ'
            bl_tilities = house.find('div', class_='bl-tilities').text
            area = bl_tilities.split()[2]+' m2' 

            data_house['title'] = title
            data_house['address'] = address
            data_house['price'] = price
            data_house['area'] = area
            
            data_real_estate.append(data_house)
        except NameError:
                print('Variable is not defined')
        except:
                print('Some else went wrong')
        
    next_button = browser.find_element_by_css_selector('.next')
    next_button.click()
    sleep(2)
# print(data_real_estate)

# create file csv
df = pd.DataFrame(data_real_estate, columns=['Tile'],columns=['Address'],columns=['Price'],columns=['Area'])
output_data_name = str(input('Enter the file output name: '))
df.to_csv(output_data_name+".csv")
# df.to_excel("data-real-estate.xlsx", index=False)
sleep(4)
browser.close()

