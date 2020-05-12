from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import csv
import io

options = Options()
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument("--incognito")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

scopus_id = ''
sorted_by = ''
#1 - All articles
#2 - Date(Newest)
#3 - Date(Oldest)
#4 - Cited by(Highest)
#5 - Cited by(Lowest)
min_year =  #0 to ignore
max_year =  #0 to ignore
size =   #max 200, for sorted_by == 1 or to get the maximum, fill with 0

cdriver = webdriver.Chrome(options=options, executable_path=r"chromedriver") #needs to specify the webdriver path
cdriver.implicitly_wait(10)
cdriver.get('https://www.scopus.com/authid/detail.uri?authorId='+scopus_id)

#To close a popup window in authors page
try:
            janela = WebDriverWait(cdriver,5).until(EC.presence_of_element_located((By.ID, '_pendo-close-guide_')))
            cdriver.find_element_by_id('_pendo-close-guide_').click()
finally:
            articles = []
            author = cdriver.find_element_by_class_name('wordBreakWord').get_attribute("innerText")

#Creating the author folder
if not os.path.exists(author):
    os.makedirs(author)

box = WebDriverWait(cdriver,30).until(EC.presence_of_element_located((By.ID,'resultDataRow0')))

if sorted_by != 1:
                cdriver.find_elements_by_class_name('ui-selectmenu-text')[0].click()
                #selecting article's classification
                if sorted_by ==3:
                    cdriver.find_element_by_id('ui-id-2').click()
                    time.sleep(2)

                elif sorted_by == 4:
                    cdriver.find_element_by_id('ui-id-3').click()
                    time.sleep(2)

                elif sorted_by == 5:
                    cdriver.find_element_by_id('ui-id-4').click()
                    time.sleep(2)

                cdriver.find_elements_by_class_name('ui-selectmenu-text')[1].click()
                cdriver.find_element_by_id('ui-id-12').click()
                time.sleep(3)

                pages = cdriver.find_elements_by_class_name('ddmDocTitle')
                years = cdriver.find_elements_by_class_name('ddmPubYr')
                links = []

                if (max_year != 0 and min_year !=0):
                    for i in range(0,len(pages)):
                        if(int(years[i].get_attribute("innerText"))<=max_year and int(years[i].get_attribute("innerText")) >= min_year):
                            links.append(pages[i].get_attribute("href"))
                elif (max_year != 0 and min_year ==0):
                        for i in range(0,len(pages)):
                            if(int(years[i].get_attribute("innerText"))<=max_year):
                                links.append(pages[i].get_attribute("href"))
                elif (max_year == 0 and min_year !=0):
                        for i in range(0,len(pages)):
                            if(int(years[i].get_attribute("innerText"))>=min_year):
                                links.append(pages[i].get_attribute("href"))
                count = 0
                for link in links:
                    if (count==size and size != 0):
                        break
                    cdriver.get(link)

                    if(cdriver.find_element_by_id('fwciValue').text ):#Check if FWCI value exist
                        item = []
                        count+=1
                        #Articles name
                        item.append(cdriver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "h3", " " ))]').text)
                        if(cdriver.find_element_by_id('fwciValue').text == ''):
                            continue
                        #FWCI
                        item.append(cdriver.find_element_by_id('fwciValue').text)
                        #Journal with date
                        item.append(cdriver.find_element_by_id('journalInfo').text)
                        #authors and co-authors
                        anchors = cdriver.find_elements_by_xpath('//*[(@id = "authorlist")]//*[contains(concat( " ", @class, " " ), concat( " ", "anchorText", " " ))]')
                        #authors count
                        item.append(len(anchors))
                        #prominence percentile
                        item.append(cdriver.find_element_by_class_name('percentText').text)
                        key_words = cdriver.find_elements_by_xpath('//*[(@id = "topicSection")]//*[contains(concat( " ", @class, " " ), concat( " ", "secondaryLink", " " ))]')
                        #3 keywords by scopus
                        if(key_words):
                            item.append(key_words[1].get_attribute('innerText')) 
                        anchors_text = ''
                        for i in anchors:
                            anchors_text=anchors_text+"|"+i.text
                        #name of authors and co-authors
                        item.append(anchors_text)
                        articles.append(item)
                print(articles)


else: #To harvest data of all articles
    cdriver.get(cdriver.find_element_by_class_name('ddmDocTitle').get_attribute("href"))
    next_button_wait = WebDriverWait(cdriver,5).until(EC.presence_of_element_located((By.CLASS_NAME,'nextLink')))
    count = 0
    while True:
        try:
            next_button_wait = WebDriverWait(cdriver,5).until(EC.presence_of_element_located((By.CLASS_NAME,'nextLink'))) #Verifica se há mais artigos para coletar
            if (cdriver.find_element_by_id('fwciValue').text): #Verifica se existe o valor FWCI
                    item = []
                    count +=1
                    #Articles name
                    item.append(cdriver.find_element_by_class_name('h3').text)
                    if(cdriver.find_element_by_id('fwciValue').text == ''):
                        continue
                    #FWCI
                    item.append(cdriver.find_element_by_id('fwciValue').text)
                    #Journal with date
                    item.append(cdriver.find_element_by_id('journalInfo').text)
                    #authors and co-authors
                    anchors = cdriver.find_elements_by_xpath('//*[(@id = "authorlist")]//*[contains(concat( " ", @class, " " ), concat( " ", "anchorText", " " ))]')
                    #authors count
                    item.append(len(anchors))
                    #prominence percentile
                    item.append(cdriver.find_element_by_class_name('percentText').text)
                    #3 keywords by scopus
                    key_words = cdriver.find_elements_by_xpath('//*[(@id = "topicSection")]//*[contains(concat( " ", @class, " " ), concat( " ", "secondaryLink", " " ))]')
                    item.append(key_words[1].get_attribute('innerText'))
                    for i in anchors:
                            anchors_text=anchors_text+"|"+i.text
                    #name of authors and co-authors
                    item.append(anchors_text)
                    anchors_text = ''
                    articles.append(item)
            cdriver.find_element_by_class_name('nextLink').click()
        except: #in case of next button does not appear
            while(cdriver.current_url=='https://www.scopus.com/error.uri'): #Handling with scopus error
                cdriver.execute_script("window.history.go(-1)")
                try:
                    WebDriverWait(cdriver,10).until(EC.presence_of_element_located((By.CLASS_NAME,'nextLink')))	
                except:
                    continue
            try:
                next_button_wait = WebDriverWait(cdriver,5).until(EC.presence_of_element_located((By.CLASS_NAME,'nextLink'))) #Verifica se há mais artigos para coletar
                cdriver.find_element_by_class_name('nextLink').click()
            except:
                cdriver.refresh()
                try:
                    next_button_wait = WebDriverWait(cdriver,5).until(EC.presence_of_element_located((By.CLASS_NAME,'nextLink'))) #Verifica se há mais artigos para coletar
                    cdriver.find_element_by_class_name('nextLink').click()
                except:
                    print(articles)
                    break

#Writing in csv
with open(author+"\\" + scopus_id +"_"+ str(sorted_by) +"_"+ str(size) +"_"+ str(min_year) +"_"+ str(max_year)+".csv", "w", encoding="utf-8",newline='') as f:
    c = csv.writer(f)
    c.writerow(["Article_name", "FWCI", "year" ,"authors_count","Prominence percentile","Topics","Anchors"])
    c.writerows(articles)
    f.close()
    print("CSV file written with success")
