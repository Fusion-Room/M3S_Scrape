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


def getSearchInfo():
    print('Please enter a search start date in this format - 2/10/2016')
    startdate = raw_input('>').lower()

    print(startdate)

    print('Please enter a search stop date in this format - 2/10/2016"')
    stopdate = raw_input('>').lower()

    print('Please type a source')
    print('Either type in the exact name of the source you require, or type "A" for *all* Arabic sources, "C" for all Chinese, "E" for all English, "F" for all Farsi, or "R" for all Russian.')


    source = raw_input('>').lower()
    print('Please enter your search term.')

    searchTerm = raw_input('>')
    wordLimit = 600
    print(
    'M3S_scraper extracts the first 600 words of an article by default. Extracting the complete text can affect the speed of data pulls.')
    print('Would you like to keep this default setting? Y/N?')
    isLimit = raw_input('>').lower()

    initalInfo = { 'sDate': startdate, 'stDate': stopdate, 'source': source,
                  'sTerm': searchTerm, 'isLimit': isLimit}
    print("""
     _  _  ____  ____
    ( \/ )( __ \/ ___)
    / \/ \ (__ (\___ \\
    \_)(_/(____/(____/

    """)
    print('scraper is now running...')
    return initalInfo




def inputSearchTerm(userData):
    # WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/')))
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/input').click()
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/input').clear()
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/input').send_keys(
        userData['sTerm'])




def inputDateRange(userData):
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/input').click()
    time.sleep(6)
    driver.find_element_by_xpath('// *[ @ id = "panelbar"] / li[2]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="TimestampDropDown"]/div[5] / a').click()
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="TimestampDropDown"]/div[5] / a')))
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "SearchFilterContainerstart_time_adv"]')))
    driver.find_element_by_xpath('// *[ @ id = "SearchFilterContainerstart_time_adv"]').click()
    driver.find_element_by_xpath('// *[ @ id = "SearchFilterContainerstart_time_adv"]').clear()
    driver.find_element_by_xpath('// *[ @ id = "SearchFilterContainerstart_time_adv"]').send_keys(
        userData['sDate'] + ' 12:00 AM')
    driver.find_element_by_xpath('//*[@id="SearchFilterContainerend_time_adv"]').click()
    driver.find_element_by_xpath('//*[@id="SearchFilterContainerend_time_adv"]').clear()
    driver.find_element_by_xpath('//*[@id="SearchFilterContainerend_time_adv"]').send_keys(
        userData['stDate'] + ' 12:00 AM')


def inputSourceLang(userData):
    driver.find_element_by_xpath('//*[@id="panelbar"]/li[3]').click()
    driver.find_element_by_xpath('// *[ @ id = "panelbar"] / li[3]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[3]/span').click()
    # driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[3]/div[1]/div/ul/li/input').click()
    time.sleep(4)
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[2]/span').click()
    time.sleep(4)
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[2]/div[1]/div/ul/li').click()
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[2]/div[1]/div/ul/li/input').clear()
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[2]/div[1]/div/ul/li/input').send_keys(
        userData['source'])
    time.sleep(4)
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[2]/div[1]/div/ul/li/input').send_keys(Keys.RETURN)
    time.sleep(4)



def initialSearch(userData):






    # ENGAGE!!
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[3]/div').click()






def resultsParser(userData):
    wordCount = userData['isLimit']
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ToolbarContentTitle"]/span[1]')))
    resultCount = driver.find_element_by_xpath('//*[@id="ToolbarContentTitle"]/span[1]').text
    resultCount = int(resultCount)
    print(resultCount)
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ListItemTitle')))
    this = driver.find_elements_by_xpath("//*[contains(@id, 'ListItem-')]")
    idString= str(this[0].get_attribute("id"))
    print(idString)
    scriptString = "ResultsList.NavigateToDataEndPoint($('#"+idString+"').children('.ListItem'))"
    driver.execute_script(scriptString)
    articleMonster(resultCount, wordCount)
    print('This scrape is finished.')
    driver.close()

def singleSearchShibboleth(userData):
    langArray = ['a', 'c', 'f', 'r']
    sourceArray = []

    if userData['source'] not in langArray:
        print('test')
        # TODO execute just one search process
    else:
        inputSearchTerm(userData)
        inputDateRange(userData)
        inputSourceLang(userData)

        sourceArray = driver.find_elements_by_css_selector("li[class^='search-choice'] span")
        for x in sourceArray:
            sourceArray.append(x.text)
        return(sourceArray)










def searchGenie(userData): #this is the function that coordinates all other searches.
    source = singleSearchShibboleth(userData)
    if type(source) == list:
        for x in source:
            userData['source'] = x
            inputSearchTerm(userData)
            inputDateRange(userData)
            inputSource(userData)
            driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[3]/div').click()
    else:
        #TODO single source search here









def logOn():
    shelfFile = shelve.open('m3sshelf')
    Username = shelfFile['un']
    Password = shelfFile['pw']
    driver.get("https://m3s.tamu.edu")
    time.sleep(5)

    driver.find_element_by_id('UserName').send_keys(Username)
    driver.find_element_by_id('Password').send_keys(Password)

    driver.find_element_by_class_name('DisplayButton').click()
    time.sleep(2)




def sequence():
    checkForShelve()
    userData = getSearchInfo()
    logOn()
    searchGenie(userData) # this is the function that coordinates all other searches.
    resultsParser(userData) # Parses results and kicks off Ripper
    # ripper

# TODO Fold Ripper logic into search Genie and test the process so far

sequence()

