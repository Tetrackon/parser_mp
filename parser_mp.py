from bs4 import BeautifulSoup
import requests
import sqlite3

db_urls = "test.db" #Путь к бд с адресами
name_tabl = "URL" #Название таблицы в этой бд
urls = "url" #Название столбца с адресами



def load_url(url):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/109.0.0.0 Safari/537.36 OPR/94.0.4606.65"
    }
    rsp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(rsp.content, "html.parser")
    return soup

def pars(soup, cls):
    res = soup.find("div", class_=cls).get_text(strip=True)
    return res


def set_db(cur, conn, colum, data, id):
    cur.execute(f"UPDATE {name_tabl} SET {colum}=? WHERE {urls} = ?", (data, id))
    conn.commit()
    return None

conn = sqlite3.connect(db_urls)
cur = conn.cursor()
cur.row_factory = None
cur.execute(f"SELECT {urls} from {name_tabl}")
arr_data = []

for item in cur:
    soup = load_url(item[0])
    stock = 1 if pars(soup, "stock") == "In stock" else 0
    print(stock)
    price = pars(soup, "price").split()
    arr_data.append({"url": item[0], "price": price[0], "currency": price[1], "stock":stock})

for i in arr_data:
    for j in ["price", "currency", "stock"]:
        set_db(cur, conn,j, i[j], i["url"])
