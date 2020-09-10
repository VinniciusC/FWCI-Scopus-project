from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
import os
import csv
import io
import sys
def run_selenium(*args):
    options = Options()
    preferences = {"download.default_directory": os.getcwd() ,
                "directory_upgrade": True,
                "safebrowsing.enabled": True }
    options.add_experimental_option("prefs", preferences)
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    scopus_id = args[0]
    sorted_by = int(args[1])
    #1 - All article
    #2 - Date(Newest)
    #3 - Date(Oldest)
    #4 - Cited by(Highest)
    #5 - Cited by(Lowest)
    min_year = int(args[2]) #0 to ignore
    max_year = int(args[3]) #0 to ignore
    size = int(args[4]) #for sorted_by == 1 or to get the maximum, fill with 0

    cdriver = webdriver.Chrome(options=options, executable_path= args[5]) #needs to specify the webdriver path
    cdriver.implicitly_wait(10)
    cdriver.get('https://www.scopus.com/authid/detail.uri?authorId='+scopus_id)

    #To close a popup window in authors page
    try:
                janela = WebDriverWait(cdriver,10).until(EC.presence_of_element_located((By.ID, 'pendo-backdrop')))
                close_button = WebDriverWait(cdriver,10).until(EC.presence_of_element_located((By.ID, 'pendo-button-cd5cdeac')))
                close_button.click()
    except TimeoutException:
        
        pass
    finally:
                articles = []
                author = cdriver.find_element_by_class_name('wordBreakWord').get_attribute("innerText")

    #Creating the author folder
    path = os.path.join("CSV_Files",author)
    if not os.path.exists(path):
        os.makedirs(path)

    cdriver.find_elements_by_class_name('ui-selectmenu-text')[0].click()

    #selecting article's classification
    if sorted_by == 3:
        cdriver.find_element_by_id('ui-id-2').click()
        time.sleep(4)
        sort = 'Oldest'
        
    elif sorted_by == 4:
        cdriver.find_element_by_id('ui-id-3').click()
        time.sleep(4)
        sort = 'Cited_Highest'

    elif sorted_by == 5:
        cdriver.find_element_by_id('ui-id-4').click()
        time.sleep(4)
        sort = 'Cited_Lowest'

    #downloading csv containing articles url
    cdriver.find_element_by_id('export_results').click()
    radio_btn = cdriver.find_element_by_id('CSV')
    cdriver.execute_script("arguments[0].click();", radio_btn)
    export_btn = cdriver.find_element_by_id('exportTrigger')
    cdriver.execute_script("arguments[0].click();", export_btn)
    time.sleep(3)
    articles_data = pd.read_csv('scopus.csv')
    os.remove('scopus.csv')

    count = 0
    for article in articles_data.itertuples():
        if (count==size and size != 0 and sorted_by != 1):
            break
        if(max_year != 0 and min_year !=0): #between
            if(article.Year>max_year or article.Year<min_year):
                continue
        elif(max_year == 0):
            if(article.Year<min_year):
                if(sorted_by == 2):
                    break
                else:
                    continue
        elif(min_year == 0):
            if(article.Year>max_year):
                if(sorted_by == 3):
                    break
                else:
                    continue
        cdriver.get(article.Link)
        try:
                janela = WebDriverWait(cdriver,5).until(EC.presence_of_element_located((By.ID, '_pendo-close-guide_')))
                cdriver.find_element_by_id('_pendo-close-guide_').click()
        except:
            pass

        try:
            cdriver.find_element_by_id('fwciValue').text#Check if FWCI value exist
            item = []
            #Articles name
            item.append(article.Title)
            if(cdriver.find_element_by_id('fwciValue').text == ''):
                continue
            #FWCI
            count+=1
            item.append(cdriver.find_element_by_id('fwciValue').text)
            #Journal with date
            item.append(cdriver.find_element_by_id('journalInfo').text)
            #year
            item.append(article.Year)
            #authors and co-authors
            anchors = cdriver.find_elements_by_xpath('//*[(@id = "authorlist")]//*[contains(concat( " ", @class, " " ), concat( " ", "anchorText", " " ))]')
            #authors count
            item.append(len(anchors))
            #prominence percentile
            try:
                (cdriver.find_element_by_class_name('percentText').text)
                item.append(cdriver.find_element_by_class_name('percentText').text)
            except:
                pass
            key_words = cdriver.find_elements_by_xpath('//*[(@id = "topicSection")]//*[contains(concat( " ", @class, " " ), concat( " ", "secondaryLink", " " ))]')
            #3 keywords by scopus
            if(key_words):
                item.append(key_words[1].get_attribute('innerText'))
            #name of authors
            item.append(article.Authors)
            articles.append(item)
            print(item)
        except:
            if (cdriver.current_url=='https://www.scopus.com/error.uri'):
                articles_data.append(article)
            continue

    cdriver.close()

    #file name
    if sorted_by == 1:
        file_name = 'all.csv'
    elif sorted_by == 2:
        sort = 'Newest'
        
    file_name = sort + str(size) +"_"+ str(min_year) +"_"+ str(max_year) + ".csv"
    #Writing in csv
    csv_path = os.path.join(path,file_name)
    with open(csv_path, "w", encoding="utf-8",newline='') as f:
        c = csv.writer(f)
        c.writerow(["Article_name", "FWCI","Journal info", "year" ,"authors_count","Prominence percentile","Topics","Anchors"])
        c.writerows(articles)
        f.close()
        print("CSV",file_name, "written with success")
