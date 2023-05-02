#TEST REQUEST

import requests
from bs4 import BeautifulSoup

# Specify the URL of the website you want to scrape
url = "https://gearvn.com"

# Send a GET request to the website and store the response
response = requests.get(url)

# Parse the HTML content of the response using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all the HTML elements that contain the category links
category_links = soup.find_all("a", class_="sub-cat-item-name")

# Extract the URLs of the category links and store them in a list
category_urls = [(link.get("href") for link in category_links)]

# Print the list of category URLs
print(category_urls)