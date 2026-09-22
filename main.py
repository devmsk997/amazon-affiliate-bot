import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from amazon_scraper import get_amazon_product
from gemini_writer import generate_review_article

# Sample Amazon products to post
SAMPLE_AMAZON_URLS = [
    "https://www.amazon.com/dp/B0CL5KNB9M",
    "https://www.amazon.com/dp/B0BSHF7WH3",
    "https://www.amazon.com/dp/B0C3322Y3X"
]

def send_email_to_blogger(title, content):
    blogger_email = os.environ.get("BLOGGER_EMAIL")
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")

    if not blogger_email or not sender_email or not sender_password:
        print("Error: Missing email secrets (BLOGGER_EMAIL, SENDER_EMAIL, or SENDER_PASSWORD).")
        return

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = blogger_email
    msg['Subject'] = title
    msg.attach(MIMEText(content, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Successfully sent email to Blogger!")
    except Exception as e:
        print(f"Error sending email to Blogger: {e}")

def main():
    selected_url = random.choice(SAMPLE_AMAZON_URLS)
    print(f"Fetching product data from: {selected_url}")
    
    product_data = get_amazon_product(selected_url)
    if not product_data:
        print("Failed to scrape product data.")
        return
        
    print(f"Generating review for: {product_data['title']}")
    article_html = generate_review_article(product_data)
    
    if article_html:
        print("Publishing to Blogger via Email...")
        send_email_to_blogger(product_data['title'], article_html)
    else:
        print("Skipping post due to empty review content.")

if __name__ == "__main__":
    main()
