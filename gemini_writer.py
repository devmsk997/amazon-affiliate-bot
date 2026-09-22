import os
import time
from google import genai

def generate_review_article(product_data):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY secret is not set.")
        return ""

    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    Write a detailed, engaging SEO-friendly product review article in HTML format for the following product:
    Title: {product_data.get('title')}
    URL: {product_data.get('url')}
    
    Include:
    - An attractive Introduction
    - Key Features
    - Pros and Cons
    - A Call to Action (CTA) button with affiliate link: {product_data.get('url')}?tag=bddeals996-20
    """

    # 503 এরর এড়ানোর জন্য রিট্রাই (Retry) লজিক
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )
            return response.text
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print("Waiting 10 seconds before retrying...")
                time.sleep(10)
            else:
                print("All retry attempts failed.")
                return ""
