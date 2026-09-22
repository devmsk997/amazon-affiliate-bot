import os
from google import genai

def generate_review_article(product_info):
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    prompt = f"""
    Write a detailed SEO-friendly blog post review in English for the following product:
    Title: {product_info['title']}
    
    Structure of the post:
    1. Catchy Title
    2. Introduction
    3. Key Features & Specifications
    4. Pros & Cons
    5. Who should buy this?
    6. Conclusion with Call-to-Action to buy from Amazon.

    Important: Format as HTML. Include an image using <img src="{product_info['image']}"> and an affiliate buy button link pointing to {product_info['affiliate_link']}.
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text