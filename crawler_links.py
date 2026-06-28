import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Take website URL from user
url = input("Enter website URL: ")

# Open website
response = requests.get(url)

# Convert HTML into readable structure
soup = BeautifulSoup(response.text, "html.parser")

# Find all links
links = soup.find_all("a")

# Empty list to store internal links
link_list = []

# Extract internal links
for link in links:

    href = link.get("href")

    # Check if link exists and is internal
    if href and href.startswith("/"):

        # Convert relative URL into full URL
        full_url = urljoin(url, href)

        # Save inside list
        link_list.append(full_url)


print("Links found:")
print(link_list)


print("\nNow visiting first 3 pages...\n")

# Visit first 3 links automatically
for website in link_list[:3]:

    response = requests.get(website)

    print("Visited:", website)