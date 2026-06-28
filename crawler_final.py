import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = input("Enter website URL: ")

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a")

link_list = []

# Find internal links
for link in links:

    href = link.get("href")

    if href and href.startswith("/"):

        full_url = urljoin(url, href)

        link_list.append(full_url)


# Open file to save all extracted text
file = open("all_website_data.txt", "w", encoding="utf-8")


# Visit first 3 pages
for website in link_list[:3]:

    print("Visiting:", website)

    page = requests.get(website)

    page_soup = BeautifulSoup(page.text, "html.parser")

    paragraphs = page_soup.find_all("p")

    # Write page heading
    file.write("\n\n------ NEW PAGE ------\n\n")

    # Extract text
    for para in paragraphs:

        text = para.text.strip()

        if text:

            file.write(text + "\n")


file.close()

print("All website data saved successfully")