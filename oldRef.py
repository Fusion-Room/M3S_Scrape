import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import unicodecsv as csv
import xlsxwriter
import datetime

# This is a rolled back, single search variant of m3s_scraper.

driver = webdriver.Chrome()
timeRightNow = str(datetime.datetime.now().time())

timeRightNow = timeRightNow[-4:]

workBook = xlsxwriter.Workbook((timeRightNow+'.xlsx'), {'constant_memory': True})
resultDoc = workBook.add_worksheet()


def getInfo():
    Username = raw_input('Please enter your Username:   ')
    Password = raw_input('Please enter your Password:    ')
    print('Please enter a search start date in this format - 2/10/2016')
    startdate = raw_input('>').lower()

    print(startdate)

    print('Please enter a search stop date in this format - 2/10/2016"')
    stopdate = raw_input('>').lower()

    print('Please type a source')
    # print('Type "A" for Arabic, "C" for Chinese, "E" for English, "F" for Farsi, or "R" for Russian.')

    source = raw_input('>').lower()
    print('Please enter your search term.')

    searchTerm = raw_input('>')
    wordLimit = 600
    print('M3S_scraper extracts the first 600 words of an article by default. Extracting the complete text can affect the speed of data pulls.')
    print('Would you like to keep this default setting? Y/N?')
    isLimit = raw_input('>').lower()



    initalInfo = {'uName': Username, 'pWord': Password, 'sDate': startdate, 'stDate': stopdate, 'source': source, 'sTerm':searchTerm, 'isLimit':isLimit}
    print("""
 _  _  ____  ____
( \/ )( __ \/ ___)
/ \/ \ (__ (\___ \\
\_)(_/(____/(____/

""")
    print('scraper is now running...')
    return initalInfo






def logOn(userData):
    driver.get("https://m3s.tamu.edu")
    time.sleep(5)

    driver.find_element_by_id('UserName').send_keys(userData['uName'])
    driver.find_element_by_id('Password').send_keys(userData['pWord'])

    driver.find_element_by_class_name('DisplayButton').click()
    time.sleep(2)

def initialSearch(userData):
    # SEARCH TERM

    # TEST WAIT.... SEE IF IT REDUCES INSTANCES OF FREESING UP
    # WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/')))
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/input').click()
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/input').clear()
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/input').send_keys(
        userData['sTerm'])

    # DATE RANGE
   # TEST WAIT.... SEE IF IT REDUCES INSTANCES OF FREESING UP
    #  WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/input')))
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/input').click()
    time.sleep(6)
    driver.find_element_by_xpath('// *[ @ id = "panelbar"] / li[2]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="TimestampDropDown"]/div[5] / a').click()
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="TimestampDropDown"]/div[5] / a')))
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "SearchFilterContainerstart_time_adv"]')))
    driver.find_element_by_xpath('// *[ @ id = "SearchFilterContainerstart_time_adv"]').click()
    driver.find_element_by_xpath('// *[ @ id = "SearchFilterContainerstart_time_adv"]').clear()
    driver.find_element_by_xpath('// *[ @ id = "SearchFilterContainerstart_time_adv"]').send_keys(
        userData['sDate'] + ' 12:00 AM')
    driver.find_element_by_xpath('//*[@id="SearchFilterContainerend_time_adv"]').click()
    driver.find_element_by_xpath('//*[@id="SearchFilterContainerend_time_adv"]').clear()
    driver.find_element_by_xpath('//*[@id="SearchFilterContainerend_time_adv"]').send_keys(
        userData['stDate'] + ' 12:00 AM')

    # SOURCES
    driver.find_element_by_xpath('//*[@id="panelbar"]/li[3]').click()
    driver.find_element_by_xpath('// *[ @ id = "panelbar"] / li[3]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[3]/span').click()
    # driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[3]/div[1]/div/ul/li/input').click()
    time.sleep(4)
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[2]/span').click()
    time.sleep(4)
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[2]/div[2]/div/ul/li').click()
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[2]/div[2]/div/ul/li/input').clear()
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[2]/div[2]/div/ul/li/input').send_keys(
        userData['source'])
    time.sleep(4)
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[2]/div[2]/div/ul/li/input').send_keys(Keys.RETURN)
    time.sleep(4)

    # driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[3]/div[1]/div/div/ul/li[6]').click()


    # ENGAGE!!
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[3]/div').click()



def sourceTokenTime(encodedlist, words, wordCount):

    if wordCount == 'no':
        encodedlist.extend([(x.text + ' ') for x in words])
        return encodedlist
    else:
        encodedlist.extend([(x.text + ' ') for x in words[:600]]) # conrad
        return encodedlist # conrad









def articleMonster(resultCount, wordCount):
    articlediagnum= 0
    row = 0

    while articlediagnum != resultCount :
        print(articlediagnum)
        words = []
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Source_Name"]')))
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'sourceToken')))
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, 'sourceToken')))
        time.sleep(5)
        words = driver.find_elements_by_class_name('sourceToken')

        articleBufferString = ''


        # Adds Source Tokens to List

        encodedlist = []

        try:
            encodedlist = sourceTokenTime(encodedlist,words, wordCount)

        except:
            print("""ERROR ERROR
                this was unattached. now attempting to go to the next page...
                """)
            time.sleep(7)
            driver.execute_script("AdjustTranscriptLayout.NextButton();")
            words = []
            print('major error')

            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Source_Name"]')))
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'sourceToken')))
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, 'sourceToken')))
            time.sleep(5)
            words = driver.find_elements_by_class_name('sourceToken')

            articleBufferString = ''
            time.sleep(2)
            encodedlist = sourceTokenTime(encodedlist,words, wordCount)

        # metadata

        articleBufferString += articleBufferString.join(encodedlist)

        try:
            videoContent = driver.find_element_by_xpath('//*[@id="MediaPlayerDiv"]')
            print "this exists"
            articleSource = driver.find_element_by_xpath('//*[@id="Source_Name"]')
            articleDate = driver.find_element_by_xpath('// *[ @ id = "Author1"] / td[2] / span')
            printinglist = []
            printinglist.append(articleBufferString)
            articleSource = articleSource.get_attribute('value').encode('utf-8')
            articleDate = articleDate.get_attribute('value').encode('utf-8')

            # # backUPCSV
            # printinglist.append(articleSource)
            # printinglist.append(articleDate)
            # backupresultDoc.writerow(printinglist)
            #
            #



            # Fancy Excel
            col = 0
            resultDoc.write(row, col, articleSource)
            resultDoc.write(row, col + 1, articleDate)
            resultDoc.write(row, col + 2, articleBufferString)
            row += 1

            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "PageForward"]')))
            driver.execute_script("AdjustTranscriptLayout.NextButton();")
            articlediagnum += 1
        except:
            articleSource = driver.find_element_by_xpath('//*[@id="Source_Name"]')
            articleDate = driver.find_element_by_class_name('sourceCaptureTime')
            printinglist = []
            printinglist.append(articleBufferString)
            articleSource = articleSource.get_attribute('value').encode('utf-8')
            articleDate = articleDate.get_attribute('value').encode('utf-8')

            # # backUPCSV
            # printinglist.append(articleSource)
            # printinglist.append(articleDate)
            # backupresultDoc.writerow(printinglist)
            #
            #



            # Fancy Excel
            col = 0
            resultDoc.write(row, col, articleSource)
            resultDoc.write(row, col + 1, articleDate)
            resultDoc.write(row, col + 2, articleBufferString)
            row += 1

            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "PageForward"]')))
            driver.execute_script("AdjustTranscriptLayout.NextButton();")
            articlediagnum += 1





















def sequence():
    userData = getInfo()
    logOn(userData)
    initialSearch(userData)
    searchResultsMonster(userData)
    workBook.close()




sequence()