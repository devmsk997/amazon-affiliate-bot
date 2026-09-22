import os
import random
import smtplib
import time
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from amazon_scraper import get_amazon_product
from gemini_writer import generate_review_article

SAMPLE_AMAZON_URLS = [
    "[https://www.amazon.com/dp/B0CL5KNB9M](https://www.amazon.com/dp/B0CL5KNB9M)",
    "[https://www.amazon.com/dp/B0BSHF7WH3](https://www.amazon.com/dp/B0BSHF7WH3)",
    "[https://www.amazon.com/dp/B0C3322Y3X](https://www.amazon.com/dp/B0C3322Y3X)"
]

def clean_url(url):
    # Extracts only the first valid URL if duplicated
    match = re.search(r'https?://[^\s<"]+', url)
    if match:
        clean = match.group(0)
        # Fix doubled URLs if present
        if "https://" in clean[8:]:
            clean = "https://" + clean[8:].split("https://")[0]
        return clean
    return url

def extract_seo_title(html_content, fallback_title):
    match = re.search(r'<h[12][^>]*>(.*?)</h[12]>', html_content, re.IGNORECASE)
    if match:
        clean_title = re.sub('<[^<]+?>', '', match.group(1)).strip()
        return clean_title
    return fallback_title

def send_email_to_blogger(title, content):
    blogger_email = os.environ.get("BLOGGER_EMAIL")
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")

    if not blogger_email or not sender_email or not sender_password:
        print("Error: Missing email secrets.")
        return False

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = blogger_email
    msg['Subject'] = title
    msg.attach(MIMEText(content, 'html'))

    for attempt in range(3):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            print(f"Successfully sent email to Blogger with title: {title}")
            return True
        except Exception as e:
            print(f"Email attempt {attempt + 1} failed: {e}")
            time.sleep(5)

    return False

def main():
    raw_url = random.choice(SAMPLE_AMAZON_URLS)
    selected_url = clean_url(raw_url)
    print(f"Fetching product data from: {selected_url}")
    
    product_data = None
    try:
        product_data = get_amazon_product(selected_url)
    except Exception as e:
        print(f"Scraper error: {e}")
    
    if not product_data or not product_data.get('title'):
        print("Using fallback product details for review creation.")
        product_data = {
            'title': 'Premium High-Performance Electronics Device Review',
            'url': selected_url,
            'image': '[https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600](https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600)'
        }

    print("Generating SEO-optimized article...")
    article_html = generate_review_article(product_data)
    
    if article_html:
        post_title = extract_seo_title(article_html, product_data['title'])
        print(f"Publishing to Blogger: {post_title}")
        send_email_to_blogger(post_title, article_html)
    else:
        print("Skipping post due to empty review content.")

if __name__ == "__main__":
    main()
