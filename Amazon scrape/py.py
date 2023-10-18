import requests
from bs4 import BeautifulSoup
import pandas as pd

# Part 1: Scrape product listings
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
product_data = []

for page_num in range(1, 21):  # Scraping 20 pages
    url = base_url + str(page_num)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all("div", {"data-component-type": "s-search-result"})

    for product in products:
        product_url = product.find("a", {"class": "a-link-normal"})['href']
        product_name = product.find("span", {"class": "a-text-normal"}).text
        product_price = product.find("span", {"class": "a-offscreen"}).text
        rating = product.find("span", {"class": "a-icon-alt"}).text if product.find("span", {"class": "a-icon-alt"}) else "N/A"
        num_reviews = product.find("span", {"class": "a-size-base"}).text if product.find("span", {"class": "a-size-base"}) else "N/A"
        product_data.append([product_url, product_name, product_price, rating, num_reviews])

# Part 2: Scrape additional product details
for product_info in product_data:
    product_url = "https://www.amazon.in" + product_info[0]
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    description = soup.find("div", {"id": "productDescription"}).get_text() if soup.find("div", {"id": "productDescription"}) else "N/A"
    asin = soup.find("th", text="ASIN").find_next("td").get_text() if soup.find("th", string="ASIN") else "N/A"
    product_description = soup.find("th", text="Product Description").find_next("td").get_text() if soup.find("th", string="Product Description") else "N/A"
    manufacturer = soup.find("th", text="Manufacturer").find_next("td").get_text() if soup.find("th", string="Manufacturer") else "N/A"
    product_info.extend([description, asin, product_description, manufacturer])

# Create a DataFrame and export to CSV
df = pd.DataFrame(product_data, columns=["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews", "Description", "ASIN", "Product Description", "Manufacturer"])
df.to_csv("amazon_products.csv", index=False)
