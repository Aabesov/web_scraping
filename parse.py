

# s = int("6000$"[0:-1]) * 83
# print(s)


import requests
from bs4 import BeautifulSoup
import csv

URL = "https://cars.kg/offers"
HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "acccept": "*/*"
}
CSV_FILE = "car.csv"


def get_html(url, header):
    response = requests.get(url, headers=HEADERS)
    return response

def get_content_from_html(html_text) -> list:
    soup = BeautifulSoup(html_text, "html.parser")
    items = soup.find_all("a", class_="catalog-list-item")
    cars = []
    for item in items:
        cars.append(
            {
                "name": item.find("span", class_="catalog-item-caption").get_text().replace("\n", ""),
                "milleage": item.find("span", class_="catalog-item-mileage").get_text().replace("\n", ""),
                "price": item.find("span", class_="catalog-item-price").get_text().replace("\n", ""),
                "price_som": item.find("span", class_="catalog-item-price").get_text().replace("\n", ""),
                "description": item.find("span", class_="catalog-item-descr").get_text().replace("\n ", "").replace(" ", ""),
                "image": item.find("img").get("src")
            }
        )
    return cars


def safe_data(cars: list) -> None:
    with open(CSV_FILE, "w") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(["name", "milleage", "price", "price_som", "description", "image"])
        for car in cars:
            writer.writerow([car["name"], car["milleage"],
                             car["price"], car["price_som"],
                             car["description"], car["image"]])


def get_result_parse():
    html = get_html(URL, HEADERS)
    if html.status_code == 200:
        cars = get_content_from_html(html.text)
        safe_data(cars)
        return cars

get_result_parse()



