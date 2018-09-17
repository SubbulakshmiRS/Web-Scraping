import requests
from bs4 import BeautifulSoup
import re
import csv

name = []
price = []
author = []
links = []
star = []
rating = []
courses_list = []
count = 0


def get_name(nme):

    for i in range(len(nme)):
        if nme[i] is None:
            name.append("Not available")
        else:
            global count
            count = count + 1
            name.append(nme[i]['alt'])


def get_auth(auth_a):

    for i in range(len(auth_a)):
        a = auth_a[i].find('div', class_='a-row a-size-small')
        if a is None:
            author.append("Not available")
        else:
            author.append(a.get_text())

# print(author)


def get_link(link_a):

    for i in range(len(link_a)):
        link = link_a[i].find('a', attrs={'href': re.compile("^/")})
        if link is None:
            links.append("Not available")
        else:
            links.append("https://www.amazon.com/"+link.get('href'))


def get_star(star_a):

    for i in range(len(star_a)):
        a = star_a[i].find(class_="a-icon-row")
        if a is None or a.find('a') is None:
            star.append("Not available")
        else:
            star.append(a.find('a')['title'])

# print(star)


def get_rate(rate_a):

    for i in range(len(rate_a)):
        a = rate_a[i].find(class_="a-icon-row")
        if a is None or a.find(class_="a-size-small") is None:
            rating.append("Not available")
        else:
            rating.append(a.find(class_="a-size-small").text)

# print(price_a)


def get_price(price_a):

    for i in range(len(price_a)):
        a = price_a[i].find('span', class_='p13n-sc-price')
        if a is None:
            price.append("Not available")
        else:
            price.append(price_a[i].find('span', class_='p13n-sc-price').text)


# print(price)
z = 0


def main():

    url = "https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref = zg_bs_pg_1?_encoding = UTF8&pg="
    for i in range(5):
        a = requests.get(url+str(i+1))
        # print(a.content)
        soup = BeautifulSoup(a.content, 'html.parser')
        # print(soup)
        name_div = soup.select(".zg_itemImmersion .zg_itemWrapper ")
        # print(name_div)
        name_img = [n.find("img") for n in name_div]
        auth_a = soup.select(".zg_itemImmersion .zg_itemWrapper ")
        link_a = soup.select(".zg_itemImmersion .zg_itemWrapper ")
        star_a = soup.select(".zg_itemImmersion .zg_itemWrapper ")
        rate_a = soup.select(".zg_itemImmersion .zg_itemWrapper ")
        price_a = soup.select(".zg_itemImmersion .zg_itemWrapper .a-section ")
        get_name(name_img)
        get_auth(auth_a)
        get_link(link_a)
        get_star(star_a)
        get_rate(rate_a)
        get_price(price_a)
        # print(star[0])


main()

for i in range(len(author)):
    course = [name[i], links[i], author[i],
              price[i*2], rating[i], star[i]]
    # print(course)
    courses_list.append(course)

with open('in_book.csv', 'w') as file:
    writer = csv.writer(file)
    a = ["Name", "URL", "Author", "Price",
         "Number of Ratings", "Average Rating"]
    writer.writerow(a)
    for row in courses_list:
        writer.writerow([unicode(s).encode("utf-8") for s in row])
