from asyncio.windows_events import NULL
from calendar import c
from cgi import print_environ
import os
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium import webdriver
import time
import datetime
import sqlite3
from csv import writer,reader
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import pyodbc
from os import path
from glob import glob



app_name = 'gailgastenders_in'
all_file_path = f'D:\python\projects\{app_name}'
sqlite_path = f'{all_file_path}\{app_name}.db'
csv_path = f'{all_file_path}\{app_name}.csv'
download_path = os.path.expanduser('~') + '\\Documents\\pythonfiles\\' + app_name + '\\files'

search_url = 'http://gailgastenders.in/gglTender/home.asp'
options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : all_file_path}
options.add_argument("user-data-dir=C:\\Path")
options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(options = options,service=Service(executable_path=f"{all_file_path}\chromedriver.exe"))
driver.get(search_url) 
driver.maximize_window()

conn = sqlite3.connect(sqlite_path)
cursor = conn.cursor()

if os.path.exists(all_file_path):
    pass
else:
    os.makedirs(all_file_path)

if os.path.exists(download_path):
    pass
else:
    os.makedirs(download_path)

time.sleep(1)

def insert_data_from_web_to_db_firstrow(databsse_path,first_row):
    conn = sqlite3.connect(databsse_path)
    cur = conn.cursor()
    tou = tuple(first_row)
    try:
        q = '''INSERT INTO tenders(Id,Closing_Date,Tender_Subject,Ref_No) VALUES(?,?,?,?)'''
        cur.execute(q,tou)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'insert data from web to db {str(e)}')


def insert_data_from_web_to_db_page(databsse_path,main_list):
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()

    for first_row in main_list:
        print(first_row[2],'\t',first_row[3])
        cursor.execute("SELECT Ref_No FROM tenders WHERE Tender_Subject = ? and Ref_No = ?", (first_row[2], first_row[3],))
        a = cursor.fetchone()
        if a is None:
            try:
                print('data inserted successfully','\n')
                tou = tuple(first_row)
                q = '''INSERT INTO tenders(Id,Closing_Date,Tender_Subject,Ref_No) VALUES(?,?,?,?)'''
                cursor.execute(q,tou)
                conn.commit()
                conn.close()
            except Exception as e:
                print(f'insert data from web to db {str(e)}')
        else:
            print('data already available','\n')


def another_database_table_check(database_name):
    try:
        con = sqlite3.connect(database_name)
        cur = con.cursor()
        cur.execute("SELECT flag FROM tenders WHERE flag = ?", (1,))
        data = cur.fetchone()
        cur.execute("SELECT * FROM tenders WHERE flag = ?", (1,))
        data2 = cur.fetchall()
        if data != None:
            with pyodbc.connect('DRIVER={SQL Server};SERVER=153TESERVER;DATABASE=CrawlingDB;UID=hrithik;PWD=hrithik@123') as conn:
                with conn.cursor() as cursor:
                    q = f"IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{app_name}' AND xtype='U') CREATE TABLE {app_name}(Id INT NOT NULL,\
                             Closing_Date VARCHAR(500) NOT NULL,\
                             Tender_Subject VARCHAR(500) NOT NULL,\
                             Ref_No VARCHAR(500) NOT NULL,\
                             flag INT NOT NULL)"
                    cursor.execute(q)
                    cursor.execute(f"SELECT flag FROM {app_name} WHERE flag = ?", (0,))
                    da = cursor.fetchall()
                    if da == []:
                        print(f'Data inserted on server')
                        q = f"INSERT INTO {app_name}(Id,Closing_Date,Tender_Subject,Ref_No,flag) VALUES(?,?,?,?,?)"
                        cursor.execute(q,data2[0])
                    else:
                        print(f'Data not inserted on server')
            sql1 = f'UPDATE tenders SET flag ={0} WHERE flag = {1};'
            cur.execute(sql1)
            con.commit()
            cur.close()
            con.close()
        else:
            print(f'Data already available in sqlite database')
    except Exception as e:
        print(e)


def text_month_replace_to_number(date_text):
    emp_str = ""
    for m in date_text:
        if m.isdigit():
            pass
        else:
            emp_str = emp_str + m
    print(emp_str.replace(',','').replace(' ',''))


def new_scraping_code():
    data_list = []

    for p,i in enumerate(WebDriverWait(driver, 200).until(EC.presence_of_all_elements_located((By.XPATH, f'/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[2]')))):
    # for p,i in enumerate(driver.find_elements(By.XPATH,'/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[2]')):
        # data_list.append(i.text)
        index = WebDriverWait(i, 200).until(EC.presence_of_element_located((By.XPATH, f'/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[{p+2}]/td[1]'))).text
        print(index)
        data_list.append(index)
        
        cloasing_date = WebDriverWait(i, 200).until(EC.presence_of_element_located((By.XPATH, f'/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[{p+2}]/td[2]'))).text
        

        x = cloasing_date.replace(',','')
        y = x.split(' ')
        date_string = y[2] + ' ' + y[1] + ' ' + y[3]
        date_object = datetime.strptime(date_string, "%d %b %Y")
        dates = str(date_object).split(' ')[0]
        d = dates.split('-')

        final_date = d[2] + '/' + d[1] + '/' + d[0]
    

        data_list.append(final_date)
        print(final_date)

        tender_subject = WebDriverWait(i, 200).until(EC.presence_of_element_located((By.XPATH, f'/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[{p+2}]/td[3]'))).text
        data_list.append(tender_subject)
        print(tender_subject)

        ref_no = WebDriverWait(i, 200).until(EC.presence_of_element_located((By.XPATH, f'/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[{p+2}]/td[4]'))).text
        data_list.append(ref_no)
        print(ref_no,'\n')
    main_list.append(data_list)


every_element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="primary_nav_wrap"]/ul/li[3]/ul/li[4]/a')))
# every_element = driver.find_element(By.XPATH, '//*[@id="primary_nav_wrap"]/ul/li[3]/ul/li[4]/a')
print(every_element.get_attribute('href'))
driver.get(every_element.get_attribute('href'))
page = 1
while page == 1:
    page = 2
    try:
        
        # every_element = driver.find_element(By.XPATH, '//*[@id="primary_nav_wrap"]/ul/li[3]/ul/li[4]/a')
        # every_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'All Active Tenders ')))
        # ActionChains(driver).move_to_element(every_element).click(every_element).perform()
        # print(every_element.get_attribute('innerHTML'))
        # for element in every_element:
        #     print(element.get_attribute('href'))
        #     ActionChains(driver).move_to_element(element).click(element).perform()
        #     driver.get(element.get_attribute('href'))


        sql = """  CREATE TABLE IF NOT EXISTS tenders(Id INTEGER PRIMARY KEY
                                                     ,Closing_Date VARCHAR(500) NOT NULL DEFAULT nan
                                                     ,Tender_Subject VARCHAR(500) NOT NULL DEFAULT nan
                                                     ,Ref_No VARCHAR(500) NOT NULL DEFAULT nan
                                                     ,flag INT NOT NULL DEFAULT 1);  """
        cursor.execute(sql)
        conn.commit()
        conn.close()

        main_list = []

        new_scraping_code()
        insert_data_from_web_to_db_page(sqlite_path,main_list)
        another_database_table_check(sqlite_path)

        WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[7]/img'))).click()
    
    except Exception as e:
        print(f'Page Loop {str(e)}')
        driver.quit()
        break
    finally:
        driver.quit()
        break
