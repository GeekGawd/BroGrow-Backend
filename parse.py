from bs4 import BeautifulSoup as BSoup
import requests

def percentage_change_sector_fetcher(url):
    r = requests.get(url)
    htmlcontent = r.content
    content = BSoup(htmlcontent, 'html.parser')\
    
    # print(content.select('td[wid]'))
    categories = []
    for table in content.findAll('span', attrs={"class": "FL w120"}):
        categories.append(table.text)
    
    growth = []
    temp = []

    for table in content.findAll('div', attrs={'class':'accrMain'}):
        for i in table.findAll('td', attrs={"width": "85"}):
            temp.append(i.text)
    
    for i in range(1, len(temp), 2):
        growth.append(temp[i].strip())
    
    category_growth =[]

    for i in range(len(categories)):
        category_growth_dict = {'sectorName':categories[i],'percentChange':growth[i]}
        category_growth.append(category_growth_dict)

    return category_growth