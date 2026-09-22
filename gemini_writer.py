import os
import time
from google import genai

def generate_review_article(product_data, cluster_info):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is missing.")
        return ""

    client = genai.Client(api_key=api_key)
    
    title = product_data.get('title')
    url = product_data.get('url')
    img_url = product_data.get('image')
    affiliate_url = f"{url}?tag=bddeals996-20"
    keywords = ", ".join(cluster_info.get("SEO_Keywords", []))

    prompt = f"""
    You are an expert SEO affiliate reviewer. Generate a high-converting product review in clean HTML format.

    Product Context: {title}
    Product URL: {affiliate_url}
    Image URL: {img_url}
    Target SEO Keywords: {keywords}

    Strict Requirements:
    1. Output MUST start immediately with the primary featured <img> tag for Blogger thumbnail rendering:
       <p><img src="{img_url}" alt="{title}" width="600" style="max-width:100%; height:auto; display:block; margin:0 auto 20px auto; border-radius:8px;"></p>
    2. Year context MUST strictly be 2026.
    3. Return raw HTML inside <div> without markdown code blocks.
    4. Structure: <h2> Title, Introduction, Key Specifications Table, Key Features, Pros & Cons, Verdict.
    5. Include a high-converting CTA button linking to {affiliate_url}:
       <a href="{affiliate_url}" target="_blank" style="background:#FF9900; color:#fff; padding:14px 28px; text-decoration:none; font-weight:bold; border-radius:5px; display:inline-block; margin:20px 0;">Check Lowest Price on Amazon</a>
    """

    target_model = "gemini-3.6-flash"
    for attempt in range(1, 6):
        try:
            response = client.models.generate_content(
                model=target_model,
                contents=prompt,
            )
            if response and response.text:
                content = response.text.replace("```html", "").replace("```", "").strip()
                if "<img" not in content[:300]:
                    img_header = f'<p><img src="{img_url}" alt="{title}" width="600" style="max-width:100%; height:auto; display:block; margin:0 auto 20px auto; border-radius:8px;"></p>\n'
                    content = img_header + content
                return content
        except Exception as e:
            print(f"Gemini API attempt {attempt} failed ({e}). Waiting {attempt * 10}s...")
            time.sleep(attempt * 10)

    return ""
