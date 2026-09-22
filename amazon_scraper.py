import requests
from bs4 import BeautifulSoup
import re
from config import AMAZON_TAG

def get_amazon_product(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.content, 'html.parser')

        # Title
        title_el = soup.find(id="productTitle")
        title = title_el.get_text().strip() if title_el else "Amazon Product"

        # Image
        img_el = soup.find(id="landingImage")
        img_url = img_el['src'] if img_el else ""

        # Extract ASIN and build Affiliate Link
        asin_match = re.search(r'/(?:dp|gp/product)/([A-Z0-9]{10})', url)
        if asin_match:
            asin = asin_match.group(1)
            affiliate_url = f"https://www.amazon.com/dp/{asin}?tag={AMAZON_TAG}"
        else:
            affiliate_url = url

        return {
            "title": title,
            "image": img_url,
            "affiliate_link": affiliate_url
        }
    except Exception as e:
        print(f"Error fetching product: {e}")
        return None