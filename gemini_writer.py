import os
import time
from google import genai

def generate_review_article(product_data):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY secret is not set.")
        return ""

    client = genai.Client(api_key=api_key)
    
    title = product_data.get('title', 'Best Smart Tech Gadget Review 2026')
    url = product_data.get('url', 'https://www.amazon.com')
    img_url = product_data.get('image', 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600')
    
    affiliate_url = f"{url}?tag=bddeals996-20"

    prompt = f"""
    You are an expert SEO affiliate content writer. Write a high-converting, viral tech review targeting high search volume keywords.

    Product Context: {title}
    Product URL: {affiliate_url}
    Image URL: {img_url}

    Strict Rules:
    1. Output MUST start immediately with the <img> tag for Blogger Featured Image detection.
       Example: <p><img src="{img_url}" alt="{title}" style="max-width:100%; height:auto; display:block; margin:0 auto 20px auto; border-radius:8px;"></p>
    2. Target high-volume search terms like "Best Tech Gadget 2026", "Worth the Money?", "Top Features & Deals".
    3. Year context MUST strictly be 2026.
    4. Return raw HTML inside <div> without markdown code blocks.
    5. Include an engaging <h2> Title, Introduction, Key Specs Table, Features & Benefits, Pros & Cons, and Final Buyer Recommendation.
    6. Include a high-converting CTA button:
       <a href="{affiliate_url}" target="_blank" style="background:#FF9900; color:#fff; padding:14px 28px; text-decoration:none; font-weight:bold; border-radius:5px; display:inline-block; margin:20px 0; font-size:16px;">Check Lowest Price on Amazon</a>
    """

    target_model = "gemini-3.6-flash"
    max_retries = 5

    print(f"Generating content with model: {target_model}")
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model=target_model,
                contents=prompt,
            )
            if response and response.text:
                content = response.text.replace("```html", "").replace("```", "").strip()
                if "<img" not in content[:300]:
                    img_header = f'<p><img src="{img_url}" alt="{title}" style="max-width:100%; height:auto; display:block; margin:0 auto 20px auto; border-radius:8px;"></p>\n'
                    content = img_header + content
                print("High-converting SEO article generated successfully!")
                return content
        except Exception as e:
            wait_time = attempt * 10
            print(f"Attempt {attempt}/{max_retries} failed ({e}). Waiting {wait_time}s...")
            time.sleep(wait_time)

    return ""
