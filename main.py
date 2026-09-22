import os
import random
from amazon_scraper import get_amazon_product
from gemini_writer import generate_review_article
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Sample Amazon products to post
SAMPLE_AMAZON_URLS = [
    "https://www.amazon.com/dp/B0CL5KNB9M",
    "https://www.amazon.com/dp/B0BSHF7WH3",
    "https://www.amazon.com/dp/B0C3322Y3X"
]

def post_to_blogger(title, content):
    blog_id = os.environ.get("BLOGGER_BLOG_ID")
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not blog_id:
        print("Error: BLOGGER_BLOG_ID secret is not set.")
        return

    try:
        blogger = build('blogger', 'v3', developerKey=api_key)
        body = {
            "kind": "blogger#post",
            "title": title,
            "content": content
        }
        
        # Publish post
        posts = blogger.posts()
        request = posts.insert(blogId=blog_id, body=body)
        response = request.execute()
        print(f"Successfully posted to Blogger! Post URL: {response.get('url')}")
    except Exception as e:
        print(f"Error posting to Blogger: {e}")

def main():
    selected_url = random.choice(SAMPLE_AMAZON_URLS)
    print(f"Fetching product data from: {selected_url}")
    
    product_data = get_amazon_product(selected_url)
    if not product_data:
        print("Failed to scrape product data.")
        return
        
    print(f"Generating review for: {product_data['title']}")
    article_html = generate_review_article(product_data)
    
    print("Publishing to Blogger...")
    post_to_blogger(product_data['title'], article_html)

if __name__ == "__main__":
    main()
