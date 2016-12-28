import time
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import shelve
import xlsxwriter
import datetime
driver = webdriver.Chrome('/Users/old/Desktop/2017M3S/chromedriver')

def getUserInfo():
    shelfFile = shelve.open('m3sshelf')

    Username = raw_input('Please enter your Username:   ')
    Password = raw_input('Please enter your Password:    ')
    print('M3S_Scrape will now check to see if these credentials work.')
    driver.get("https://m3s.tamu.edu")
    time.sleep(5)
    driver.find_element_by_id('UserName').send_keys(Username)
    driver.find_element_by_id('Password').send_keys(Password)
    driver.find_element_by_class_name('DisplayButton').click()
    time.sleep(5)
    if len(driver.find_elements_by_id('Password')) == 0:
        shelfFile['un'] = Username
        shelfFile['pw'] = Password
        shelfFile.close()
        return
    else:
        getUserInfo()



def checkForShelve():
    cd = os.getcwd()
    if os.path.exists(os.path.join(cd, 'm3sshelf.db')):
        return True
    else:
        getUserInfo()

checkForShelve()


