import os
import time
from google import genai

def generate_review_article(product_data):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY secret is not set.")
        return "", ""

    client = genai.Client(api_key=api_key)
    
    title = product_data.get('title', 'Amazon Top Electronics Product Review')
    url = product_data.get('url', 'https://www.amazon.com')
    img_url = product_data.get('image', 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600') # Fallback image
    
    affiliate_url = f"{url}?tag=bddeals996-20"

    prompt = f"""
    You are an expert SEO content creator. Generate a high-converting Amazon product review in clean HTML format.

    Product Name Context: {title}
    Product URL: {affiliate_url}
    Image URL: {img_url}

    Strict Rules:
    1. Output ONLY valid HTML inside <div>. Do not use ```html code block markers.
    2. Make a catchy, SEO-friendly article Title.
    3. Include the main image using <img src="{img_url}" alt="{title}" style="max-width:100%; height:auto; display:block; margin: 0 auto 20px auto; border-radius:8px;"> at the top.
    4. Structure with <h2>, <h3>, bullet points, and a comparison table.
    5. Add a prominent Call-To-Action (CTA) button linking to: {affiliate_url}

    Structure to follow:
    - Main Image
    - Introduction (SEO keywords included)
    - Key Specifications (Use HTML Table)
    - Key Features & Benefits (Bullet points)
    - Pros & Cons
    - Final Verdict & Buying Recommendation
    - Buy Now Button (Styled with CSS)
    """

    models_to_try = ["gemini-3.6-flash", "gemini-1.5-flash", "gemini-2.0-flash"]

    for model_name in models_to_try:
        print(f"Trying model for SEO content: {model_name}")
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                if response and response.text:
                    content = response.text.replace("```html", "").replace("```", "").strip()
                    return content
            except Exception as e:
                print(f"Attempt {attempt + 1} with {model_name} failed: {e}")
                time.sleep(5)

    return ""
