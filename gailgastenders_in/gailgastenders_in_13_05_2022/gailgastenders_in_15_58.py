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
main_list = []
conn = sqlite3.connect(sqlite_path)
cur = conn.cursor()



if os.path.exists(all_file_path):
    pass
else:
    os.makedirs(all_file_path)
if os.path.exists(download_path):
    pass
else:
    os.makedirs(download_path)


search_url = 'http://gailgastenders.in/gglTender/home.asp'
options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : all_file_path}
options.add_argument("user-data-dir=C:\\Path")
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options = options,service=Service(executable_path=f"{all_file_path}\chromedriver.exe"))
driver.get(search_url) 
driver.maximize_window()

action = ActionChains(driver)

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


def insert_data_from_web_to_db_page(main_lis):
    try:
        for first_row in main_lis:
            print(first_row[1],'\t',first_row[2])
            cur.execute("SELECT Tender_Notice_No FROM tenders WHERE Tender_Summery = ? and Tender_Notice_No = ?", (first_row[1], first_row[2],))
            a = cur.fetchone()
            if a is None:
                print('data inserted successfully','\n')
                tou = tuple(first_row)
                q = '''INSERT INTO tenders(Bid_deadline_2,Tender_Summery,Tender_Notice_No) VALUES(?,?,?)'''
                cur.execute(q, tou)
                conn.commit()
            else:
                print('data already available in sqlite','\n')

        # conn.commit()
        cur.execute("SELECT flag FROM tenders WHERE flag = ?", (1,))
        data = cur.fetchone()
        cur.execute("SELECT Tender_Notice_No,Tender_Summery,Bid_deadline_2 FROM tenders WHERE flag = ?", (1,))
        data2 = cur.fetchall()

        if data != None:
            with pyodbc.connect('DRIVER={SQL Server};SERVER=153TESERVER;DATABASE=CrawlingDB;UID=hrithik;PWD=hrithik@123') as conns:
                with conns.cursor() as cursor:
                    q = f"IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{app_name}' AND xtype='U') CREATE TABLE {app_name}(Id INTEGER PRIMARY KEY IDENTITY(1,1)\
                                     ,Tender_Notice_No TEXT\
                                     ,Tender_Summery TEXT\
                                     ,Tender_Details TEXT\
                                     ,Bid_deadline_2 TEXT\
                                     ,Documents_2 TEXT\
                                     ,TenderListing_key TEXT\
                                     ,Notice_Type TEXT\
                                     ,Competition TEXT\
                                     ,Purchaser_Name TEXT\
                                     ,Pur_Add TEXT\
                                     ,Pur_State TEXT\
                                     ,Pur_City TEXT\
                                     ,Pur_Country TEXT\
                                     ,Pur_Email TEXT\
                                     ,Pur_URL TEXT\
                                     ,Bid_Deadline_1 TEXT\
                                     ,Financier_Name TEXT\
                                     ,CPV TEXT\
                                     ,scannedImage TEXT\
                                     ,Documents_1 TEXT\
                                     ,Documents_3 TEXT\
                                     ,Documents_4 TEXT\
                                     ,Documents_5 TEXT\
                                     ,currency TEXT\
                                     ,actualvalue TEXT\
                                     ,TenderFor TEXT\
                                     ,TenderType TEXT\
                                     ,SiteName TEXT\
                                     ,createdOn TEXT\
                                     ,updateOn TEXT\
                                     ,Content TEXT\
                                     ,Content1 TEXT\
                                     ,Content2 TEXT\
                                     ,Content3 TEXT\
                                     ,DocFees TEXT\
                                     ,EMD TEXT\
                                     ,OpeningDate TEXT\
                                     ,Tender_No TEXT)"
                    cursor.execute(q)
                    conns.commit()
                    q = f"INSERT INTO {app_name}(Tender_Notice_No,Tender_Summery,Bid_deadline_2) VALUES(?,?,?)"
                    cursor.execute(q, data2[0])
                    print(f'Data inserted on server')

            sql1 = f'UPDATE tenders SET flag ={0} WHERE flag = {1};'
            cur.execute(sql1)
            conn.commit()
        else:
            print(f'Data already available in sqlite database')
    except Exception as e:
        print(f'insert data from web to db {str(e)}')


def another_database_table_check():
    try:

        cur.execute("SELECT flag FROM tenders WHERE flag = ?", (1,))
        data = cur.fetchone()
        cur.execute("SELECT Tender_Notice_No,Tender_Summery,Bid_deadline_2 FROM tenders WHERE flag = ?", (1,))
        data2 = cur.fetchall()

        if data != None:
            with pyodbc.connect('DRIVER={SQL Server};SERVER=153TESERVER;DATABASE=CrawlingDB;UID=hrithik;PWD=hrithik@123') as conn:
                with conn.cursor() as cursor:
                    q = f"IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{app_name}' AND xtype='U') CREATE TABLE {app_name}(Id INTEGER PRIMARY KEY IDENTITY(1,1)\
                             ,Tender_Notice_No TEXT\
                             ,Tender_Summery TEXT\
                             ,Tender_Details TEXT\
                             ,Bid_deadline_2 TEXT\
                             ,Documents_2 TEXT\
                             ,TenderListing_key TEXT\
                             ,Notice_Type TEXT\
                             ,Competition TEXT\
                             ,Purchaser_Name TEXT\
                             ,Pur_Add TEXT\
                             ,Pur_State TEXT\
                             ,Pur_City TEXT\
                             ,Pur_Country TEXT\
                             ,Pur_Email TEXT\
                             ,Pur_URL TEXT\
                             ,Bid_Deadline_1 TEXT\
                             ,Financier_Name TEXT\
                             ,CPV TEXT\
                             ,scannedImage TEXT\
                             ,Documents_1 TEXT\
                             ,Documents_3 TEXT\
                             ,Documents_4 TEXT\
                             ,Documents_5 TEXT\
                             ,currency TEXT\
                             ,actualvalue TEXT\
                             ,TenderFor TEXT\
                             ,TenderType TEXT\
                             ,SiteName TEXT\
                             ,createdOn TEXT\
                             ,updateOn TEXT\
                             ,Content TEXT\
                             ,Content1 TEXT\
                             ,Content2 TEXT\
                             ,Content3 TEXT\
                             ,DocFees TEXT\
                             ,EMD TEXT\
                             ,OpeningDate TEXT\
                             ,Tender_No TEXT)"
                    cursor.execute(q)
                    cursor.execute(f"SELECT flag FROM {app_name} WHERE flag = ?", (0,))
                    da = cursor.fetchall()
                    if da == []:
                        print(f'Data inserted on server')
                        q = f"INSERT INTO {app_name}(Id,Closing_Date,Tender_Subject,Ref_No,flag) VALUES(?,?,?,?,?)"
                        cursor.execute(q, data2[0])
                        print(f'Data inserted on server')
                    else:
                        print(f'Data not inserted on server')
            sql1 = f'UPDATE tenders SET flag ={0} WHERE flag = {1};'
            cur.execute(sql1)
            con.commit()
        else:
            print(f'Data already available in sqlite database')
    except Exception as e:
        print(str(e))


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
    length_of_tr = WebDriverWait(driver, 200).until(EC.presence_of_all_elements_located((By.XPATH, f'/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr')))
    print(len(length_of_tr))
    for p,i in enumerate(WebDriverWait(driver, 200).until(EC.presence_of_all_elements_located((By.XPATH, f'/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr')))[1:len(length_of_tr) - 1]):

        cloasing_date = WebDriverWait(i, 200).until(EC.presence_of_element_located((By.XPATH, f'/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[{p+2}]/td[2]'))).text
        x = cloasing_date.replace(',','')
        y = x.split(' ')
        date_string = y[2] + ' ' + y[1] + ' ' + y[3]
        date_object = datetime.strptime(date_string, "%d %b %Y")
        dates = str(date_object).split(' ')[0]
        d = dates.split('-')
        Bid_deadline_2 = d[2] + '/' + d[1] + '/' + d[0]
        data_list.append(Bid_deadline_2)
        print(Bid_deadline_2)

        Tender_Summery = WebDriverWait(i, 200).until(EC.presence_of_element_located((By.XPATH, f'/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[{p+2}]/td[3]'))).text
        data_list.append(Tender_Summery)
        print(Tender_Summery)

        Tender_Notice_No = WebDriverWait(i, 200).until(EC.presence_of_element_located((By.XPATH, f'/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[{p+2}]/td[4]'))).text
        data_list.append(Tender_Notice_No)
        print(Tender_Notice_No,'\n')

    main_list.append(data_list)


every_element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'sub_ul')))
display_prop = every_element.value_of_css_property('display')
if display_prop == 'none':
    driver.execute_script("arguments[0].style.display = 'block';", every_element)
    every_element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="primary_nav_wrap"]/ul/li[3]/ul/li[4]/a'))).click()
page = 1
while True:
    page = 2
    try:
        sql = """  CREATE TABLE IF NOT EXISTS tenders(Id INTEGER PRIMARY KEY AUTOINCREMENT
                                                                 ,Tender_Notice_No TEXT
                                                                 ,Tender_Summery TEXT
                                                                 ,Tender_Details TEXT
                                                                 ,Bid_deadline_2 TEXT
                                                                 ,Documents_2 TEXT
                                                                 ,TenderListing_key TEXT
                                                                 ,Notice_Type TEXT
                                                                 ,Competition TEXT
                                                                 ,Purchaser_Name TEXT
                                                                 ,Pur_Add TEXT
                                                                 ,Pur_State TEXT
                                                                 ,Pur_City TEXT
                                                                 ,Pur_Country TEXT
                                                                 ,Pur_Email TEXT
                                                                 ,Pur_URL TEXT
                                                                 ,Bid_Deadline_1 TEXT
                                                                 ,Financier_Name TEXT
                                                                 ,CPV TEXT
                                                                 ,scannedImage TEXT
                                                                 ,Documents_1 TEXT
                                                                 ,Documents_3 TEXT
                                                                 ,Documents_4 TEXT
                                                                 ,Documents_5 TEXT
                                                                 ,currency TEXT
                                                                 ,actualvalue TEXT
                                                                 ,TenderFor TEXT
                                                                 ,TenderType TEXT
                                                                 ,SiteName TEXT
                                                                 ,createdOn TEXT
                                                                 ,updateOn TEXT
                                                                 ,Content TEXT
                                                                 ,Content1 TEXT
                                                                 ,Content2 TEXT
                                                                 ,Content3 TEXT
                                                                 ,DocFees TEXT
                                                                 ,EMD TEXT
                                                                 ,OpeningDate TEXT
                                                                 ,Tender_No TEXT
                                                                 ,flag INT DEFAULT 1);  """


        cur.execute(sql)
        conn.commit()
        new_scraping_code()
        insert_data_from_web_to_db_page(main_list)
        # another_database_table_check(sqlite_path)

        # conn.close()
        WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[7]/img'))).click()
    
    except Exception as e:
        print(f'Page Loop {e}')
        driver.quit()
        break
    finally:
        driver.quit()
        break
