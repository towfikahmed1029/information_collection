import mysql.connector
from bs4 import BeautifulSoup
import requests
import re

mydb = mysql.connector.connect(
host = "127.0.0.1",
user ="root",
password = "password",
database = 'info_collect',
auth_plugin='mysql_native_password'
)
def find_type(dom_name):
    if 'gaming' in dom_name:
        type = 'gaming'
    elif 'product' in dom_name:
        type = 'product'
    elif 'marketplace' in dom_name:
        type = 'marketplace'  
    else:
        type = 'others'
    return type
def findornew(href):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM site WHERE domain ='{0}'".format(href)
    mycursor.execute(sql)
    site = mycursor.fetchone()
    if site==None:
        sql = "INSERT INTO site (domain) VALUES ('{0}')".format(href)
        mycursor.execute(sql)
        domain_id= mycursor.lastrowid
        mydb.commit()
        return domain_id
    else:
        return site[0]
ccount = 1

while True:
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM url WHERE status = 0 LIMIT 1")
    myresult = mycursor.fetchone()
    dom_name = myresult[2]
    url_id = myresult[0]
    print("\nDomain Url---",dom_name)
    mycursor = mydb.cursor()
    sql = "UPDATE url SET status = 1  WHERE id = '{0}' ".format(url_id)
    mycursor.execute(sql)
    mydb.commit()
    dom_name_path = dom_name.split("?")[0]
    dom_root = dom_name.split("/")[2]
    mycursor = mydb.cursor()
    sql = ("INSERT INTO url (domain_id,path) VALUES (%s,%s)")
    dom_id = findornew(dom_root)
    sql_val = dom_id,dom_root
    mycursor.execute(sql,sql_val)
    url_id = mycursor.lastrowid
    mydb.commit() 
    # HTML TAG
    headinfo={
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"en-US,en;q=0.5",
        "Connection":'keep-alive',
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0"
    }
    URL = dom_name
    page = requests.get(URL,headers=headinfo)
    status_code = page.status_code
    print("status_code>>>>>>>>>>>>> ",status_code)

    # if status_code != 200:
    #     continue
    page = requests.get(URL,headers=headinfo).content
    soup = BeautifulSoup(page, 'html.parser')
    h1 = soup.find_all('h1')
    if h1 :
        mycursor = mydb.cursor()
        sql = ("INSERT INTO html_tag (name,url_id) VALUES (%s,%s)")
        sql_val = "H1",url_id
        mycursor.execute(sql,sql_val)
        h1_id =mycursor.lastrowid
        mydb.commit()
        for h1_item in h1:
            h1_item = h1_item.text
            h1_item = re.split(r'[\,\.\n\t]',h1_item)
            for item in h1_item:
                mycursor = mydb.cursor(buffered=True)
                finalItem = item.replace('"','[dq-ps]')
                finalItem = item.replace("'","[sq-ps]")
                print(finalItem)
                sql = "SELECT text FROM sentence WHERE text ='{0}'".format(str(finalItem))
                mycursor.execute(sql)
                dup = mycursor.fetchone()
                if dup == None:
                    type =find_type(dom_name)
                    mycursor = mydb.cursor()
                    sql = ("INSERT INTO sentence (tag_id,text,type) VALUES (%s,%s,%s)")
                    print("H1----------------",finalItem)
                    sql_val = (h1_id,finalItem,type)
                    mycursor.execute(sql,sql_val)
                    mydb.commit()


    h2 = soup.find_all('h2')
    if h2 :
        mycursor = mydb.cursor()
        sql = ("INSERT INTO html_tag (name,url_id) VALUES (%s,%s)")
        sql_val = "H2",url_id
        mycursor.execute(sql,sql_val)
        h2_id = mycursor.lastrowid
        mydb.commit()
        for h2_item in h2:
            h2_item = h2_item.text
            h2_item = re.split(r'[\,\.\n\t]',h2_item)
            for item in h2_item:
                count = len(item.split())
                if 2 < count < 10:
                    mycursor = mydb.cursor(buffered=True)
                    finalItem = item.replace('"','[dq-ps]')
                    finalItem = item.replace("'","[sq-ps]")
                    sql = "SELECT text FROM sentence WHERE text ='{0}'".format(str(finalItem))
                    mycursor.execute(sql)
                    dup = mycursor.fetchone()
                    if dup == None:
                        type =find_type(dom_name)
                        mycursor = mydb.cursor()
                        sql = ("INSERT INTO sentence (tag_id,text,type) VALUES (%s,%s,%s)")
                        print("H2----------------",finalItem)
                        sql_val = (h2_id,finalItem,type)
                        mycursor.execute(sql,sql_val)
                        mydb.commit()


    h3 = soup.find_all('h3')
    if h3 :
        mycursor = mydb.cursor()
        sql = ("INSERT INTO html_tag (name,url_id) VALUES (%s,%s)")
        sql_val = "H3",url_id
        mycursor.execute(sql,sql_val)
        h3_id = mycursor.lastrowid
        mydb.commit()
        for h3_item in h3:
            h3_item = h3_item.text
            h3_item = re.split(r'[\,\.\n\t]',h3_item)
            for item in h3_item:
                count = len(item.split())
                if 2 < count < 10:
                    mycursor = mydb.cursor(buffered=True)
                    finalItem = item.replace('"','[dq-ps]')
                    finalItem = item.replace("'","[sq-ps]")
                    sql = "SELECT text FROM sentence WHERE text ='{0}'".format(str(finalItem))
                    mycursor.execute(sql)
                    dup = mycursor.fetchone()
                    if dup == None:
                        type =find_type(dom_name)
                        mycursor = mydb.cursor()
                        sql = ("INSERT INTO sentence (tag_id,text,type) VALUES (%s,%s,%s)")
                        print("H3----------------",finalItem)
                        sql_val = (h3_id,finalItem,type)
                        mycursor.execute(sql,sql_val)
                        mydb.commit()
    p = soup.find_all('p')
    if p :
        # pass
        mycursor = mydb.cursor()
        sql = ("INSERT INTO html_tag (name,url_id) VALUES (%s,%s)")
        sql_val = "P",url_id
        mycursor.execute(sql,sql_val)
        p_id = mycursor.lastrowid
        mydb.commit()
        for p_item in p:
            p_item = p_item.text
            p_item = re.split(r'[\,\.\n\t]',p_item)
            for item in p_item:
                count = len(item.split())
                if 2 < count < 10:
                    mycursor = mydb.cursor(buffered=True)
                    finalItem = item.replace('"','[dq-ps]')
                    finalItem = item.replace("'","[sq-ps]")
                    sql = "SELECT text FROM sentence WHERE text ='{0}'".format(str(finalItem))
                    mycursor.execute(sql)
                    dup = mycursor.fetchone()
                    if dup == None:
                        type =find_type(dom_name)
                        mycursor = mydb.cursor()
                        sql = ("INSERT INTO sentence (tag_id,text,type) VALUES (%s,%s,%s)")
                        print("P----------------",finalItem)
                        sql_val = (p_id,finalItem,type)
                        mycursor.execute(sql,sql_val)
                        mydb.commit()

    a = soup.find_all('a')
    if a :
        for a in soup.find_all('a', href=True):
            href = ( a['href'])
            if href.startswith("http"):
                mycursor = mydb.cursor(buffered=True)
                sql = "SELECT * FROM url WHERE path ='{0}'".format(href)
                mycursor.execute(sql)
                dupli = mycursor.fetchone()
                if dupli == None:
                    mycursor = mydb.cursor()
                    sql = ("INSERT INTO url (domain_id,path) VALUES (%s,%s)")
                    sql_val = findornew(href),href
                    mycursor.execute(sql,sql_val)
                    h1_id =mycursor.lastrowid
                    mydb.commit()
    print("Count>>>>>>>>>>{ccount}".format(ccount=ccount))

    ccount+=1
    if ccount > 500:
        break
    print("Done")