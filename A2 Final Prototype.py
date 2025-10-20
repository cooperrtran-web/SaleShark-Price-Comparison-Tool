# price_comparison.py

#importing required pythin libraries
import httpx
from bs4 import BeautifulSoup

# wewbsite for scrape 
url = 'https://www.boohooman.com/au/mens/shoes/smart-shoes'

#user agent to imitate a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}


def extract_product_data(product):
    # get product name and price using tags and class names
    try:
        name = product.find('div', class_='product-tile-name').text.strip()
        price_text = product.find('span', class_='product-standard-price').text.strip()
        
        # remove excess text
        price = float(price_text.replace('$',''))
        return name, price
    #continue through error
    except Exception as e:
        print("Error extracting product:", e)



def scrape_prices():
    # retreive web page
    response = httpx.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('div', class_='product-tile js-product-tile')

    
# Create empty dictionary
    prices = {}
    for product in products:
        name, price = extract_product_data(product)
        if name and price:
            prices[name] = price
    return prices


def main():
    # retrieve prices
    prices = scrape_prices()

    # print dictionary
    for shoe, price in prices.items():
        print(f'{shoe}: ${price:.2f}')
        
    # find and print cheapest
    cheapest = min(prices, key=prices.get)
    print('Cheapest shoe = ', cheapest, 'for $', prices[cheapest])

# run code
if __name__ == "__main__":
    main()
