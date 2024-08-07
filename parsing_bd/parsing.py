from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def parsing_money_info(date):
    s = Service('/chromedriver-win64/chromedriver.exe')
    browser = webdriver.Chrome(service=s)
    browser.get(f"""https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To={date}""")
    htext = browser.page_source
    soup = BeautifulSoup(htext, 'lxml')
    try:
        rows = soup.find('table', class_='data').find_all('tr')
    except AttributeError:
        return 0
    else:
        data = []
        for row in rows[1:]:
            tmp = row.find_all("td")[1:]
            data.append([x.get_text(strip=True) for x in tmp])
            data[-1][3] = float(data[-1][3].replace(",", "."))
            data[-1][1] = int(data[-1][1])
            data[-1][1], data[-1][2] = data[-1][2], data[-1][1]
            data[-1].append(date)
        return data


if __name__ == "__main__":
    print(parsing_money_info('29.07.2024'))
