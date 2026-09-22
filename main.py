import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from keyword_research import get_high_search_product
from topic_cluster import generate_topic_cluster
from duplicate_checker import is_duplicate, mark_as_posted
from gemini_writer import generate_review_article

def send_email_to_blogger(title, content):
    blogger_email = os.environ.get("BLOGGER_EMAIL")
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")

    if not blogger_email or not sender_email or not sender_password:
        print("Missing Email Secrets.")
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
            print(f"Successfully published: {title}")
            return True
        except Exception as e:
            print(f"Email error attempt {attempt + 1}: {e}")
            time.sleep(5)
    return False

def main():
    product = get_high_search_product()
    title = product['title']

    # Duplicate check
    if is_duplicate(title):
        print(f"Skipping: '{title}' is already posted.")
        return

    print(f"Selected High-Search Product: {title}")
    cluster = generate_topic_cluster(title)

    print("Generating SEO Article with Gemini...")
    article_html = generate_review_article(product, cluster)

    if article_html:
        success = send_email_to_blogger(title, article_html)
        if success:
            mark_as_posted(title)
            print("Post pipeline completed successfully!")
    else:
        print("Failed to generate article.")

if __name__ == "__main__":
    main()
