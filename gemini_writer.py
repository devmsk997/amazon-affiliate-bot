import os
import time
from google import genai
from google.genai.errors import APIError

def generate_review_article(product_data):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY secret is not set.")
        return ""

    client = genai.Client(api_key=api_key)
    
    title = product_data.get('title', 'Amazon Top Electronics Product Review')
    url = product_data.get('url', 'https://www.amazon.com')
    img_url = product_data.get('image', 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600')
    
    affiliate_url = f"{url}?tag=bddeals996-20"

    prompt = f"""
    You are an expert SEO content creator. Generate a high-converting Amazon product review in clean HTML format.

    Product Name Context: {title}
    Product URL: {affiliate_url}
    Image URL: {img_url}

    Strict Rules:
    1. Output ONLY valid HTML inside <div>. Do not use ```html code block markers.
    2. Make a catchy, SEO-friendly article Title inside an <h2> tag at the start.
    3. Include the main image using <img src="{img_url}" alt="{title}" style="max-width:100%; height:auto; display:block; margin: 0 auto 20px auto; border-radius:8px;"> right after title.
    4. Structure with <h2>, <h3>, bullet points, and a specifications comparison table.
    5. Add a prominent, beautiful Call-To-Action (CTA) button linking to: {affiliate_url} with text "Check Price on Amazon".

    Structure to follow:
    - Main Title (H2)
    - Product Image
    - Introduction (SEO keywords included)
    - Key Specifications (Use HTML Table)
    - Key Features & Benefits (Bullet points)
    - Pros & Cons
    - Final Verdict & Buying Recommendation
    - Buy Now Button (Styled with CSS: background #FF9900, color white, padding 12px 24px, display inline-block, border-radius 5px, text-decoration none, font-weight bold)
    """

    target_model = "gemini-3.6-flash"
    max_retries = 6

    print(f"Generating content with model: {target_model}")
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model=target_model,
                contents=prompt,
            )
            if response and response.text:
                content = response.text.replace("```html", "").replace("```", "").strip()
                print("Article generated successfully!")
                return content
        except Exception as e:
            wait_time = attempt * 10  # 10s, 20s, 30s, 40s... পর্যন্ত অপেক্ষা করবে
            print(f"Attempt {attempt}/{max_retries} failed ({e}). Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)

    print("Failed to generate content after maximum retries.")
    return ""
