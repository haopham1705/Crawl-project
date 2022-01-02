# Step1: import libraries and packages for object
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

print("Hello i am crawler v0.1! \n")

# Step2: Read user and password account
with open('acc_linkedin.txt') as f:
    content = f.readlines()
    username = content[0]
    password = content[1]
    print("username: ", username)
    print("password: ", password)

keyword = input("Please enter your keywords: ")
page_no = int(input("How many page do you want to crawl: "))

# Step3: Login linkedin
url_login = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
# Create a driver
driver = webdriver.Chrome()
# Open url_login via driver
driver.get(url_login)
# Hold 2 second
time.sleep(2)
# find the field email
field_email = driver.find_element_by_id('username')
# fill the email field
field_email.send_keys(username)
# Hold 2 second
time.sleep(2)
# find the field password
# field_password = driver.find_element_by_name("session_password")
field_password = driver.find_element_by_id("password")
# fill the field password
field_password.send_keys(password)
# Hold 2 second
time.sleep(2)
# find button sign
# login_field = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
# login_field.click()
# class = btn__primary--large | from__button--floating
button_login = driver.find_element_by_class_name('btn__primary--large')
button_login.click()

# Step4: find the keywords field
# Close popup message
# msg-overlay-bubble-header__details
# flex-row align-items-center ml1
time.sleep(4)
button_hide = driver.find_element_by_class_name(
    'msg-overlay-bubble-header__details')
# button_hide = driver.find_element_by_id("ember218")
button_hide.click()
time.sleep(3)

# class = search-global-typeahead__input | always-show-placeholder
# search-global-typeahead__input always-show-placeholder
time.sleep(3)
field_search = driver.find_element_by_class_name(
    'search-global-typeahead__input')
# //*[@id="ember26"]/input
# field_search = driver.find_element_by_xpath('//*[@id="ember26"]/input')

# keyword = input("Please enter your keywords: ")
field_search.send_keys(keyword)
# Hold 1 seconds
time.sleep(1)
# Press enter for searching
field_search.send_keys(Keys.RETURN)
# Hold 2 second
time.sleep(2)
# Extend the result
button_extend = driver.find_element_by_xpath(
    '//*[@id="main"]/div/div/div[1]/div/a')
button_extend.send_keys(Keys.RETURN)

# Step6: Execute_page loop
titles = []  # contain title each person
jobs = []  # contain jobs each person
locats = []  # contain locats each person
descripts = []  # contain descripts each person


def execute_page(i):

    soup = BeautifulSoup(driver.page_source, 'lxml')  # html.parse
    divs = soup.find_all(
        "div", class_="entity-result__content entity-result__divider pt3 pb3 t-12 t-black--light")
    print("Page: {0} Find out {1} in a page".format(i+1, len(divs)))
    for div in divs:
        # Find title content each div
        title = div.find("a").text
        # Find job content each div
        job = div.find(
            "div", class_="entity-result__primary-subtitle t-14 t-black").text
        # Find locat content each dic
        locat = div.find(
            "div", class_="entity-result__secondary-subtitle t-14").text
        # Find descript each dic
        descript = div.find("p", class_="entity-result__summary").text

        # Append it in to a list
        titles.append(title)
        jobs.append(job)
        locats.append(locat)
        descripts.append(descript)

        print("title: ", title, " job: ", job,
              " locat: ", locat, " descript: ", descript)

# Move to the next page
# page_no = int(input("How many page do you want to crawl: "))
# page_no = 4


for i in range(page_no):
    print("___________________________________________________________________________")
    print("Processing page {}".format(i+1))
    execute_page(i)
    time.sleep(3)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    time.sleep(3)
    next_button = driver.find_element_by_class_name(
        'artdeco-pagination__button--next')
    time.sleep(5)
    next_button.click()
    time.sleep(2)

print("___________________________________________________________________________")
print("Finished crawling! Start to storage data into excel file")

# Step7: Storage data
data = []
for i in range(len(jobs)):
    title = titles[i]
    job = jobs[i]
    locat = locats[i]
    descript = descripts[i]
    data.append([title, job, locat, descript])
    print(data)

df = pd.DataFrame(data, columns=['title', 'job', 'locat', 'descript'])
df.to_excel("crawled_data.xlsx")

print("\n Done! \n")
