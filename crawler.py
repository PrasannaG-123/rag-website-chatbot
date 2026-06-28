import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = input("Enter website URL: ")

visited = []
to_visit = [url]

all_text = ""

while len(to_visit) > 0 and len(visited) < 3:

    current_url = to_visit.pop(0)

    response = requests.get(current_url)

    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text()

    all_text += text

    links = soup.find_all("a")

    for link in links:

        href = link.get("href")

        if href:

            full_url = urljoin(current_url, href)

            to_visit.append(full_url)