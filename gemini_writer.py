import os
import time
from google import genai
from google.genai.errors import APIError

def generate_review_article(product_data, cluster_info=None):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ জেমিনি এপিআই কি (API Key) এনভায়রনমেন্ট ভেরিয়েবলে পাওয়া যায়নি!")

    client = genai.Client(api_key=api_key)

    # Produc-er data theke title, image ebong url ber kora
    title = product_data.get('title', 'Tech Product') if isinstance(product_data, dict) else str(product_data)
    url = product_data.get('url', '#') if isinstance(product_data, dict) else '#'
    img_url = product_data.get('image', '') if isinstance(product_data, dict) else ''
    
    # Affiliate tag jukto link
    affiliate_url = f"{url}?tag=bddeals996-20" if url != '#' else '#'

    prompt = f"""
    আপনি একজন এসইও (SEO) বাংলা টেক ব্লগ রাইটার। নিচের প্রোডাক্টটির জন্য একটি সংক্ষিপ্ত ও আকর্ষণীয় রিভিউ পোস্ট লিখুন।
    প্রডাক্টের নাম: {title}
    
    গুরুত্বপূর্ণ নিয়মাবলী:
    ১. কোনো অবস্থাতেই স্টার (*) বা হ্যাশ (#) চিহ্ন ব্যবহার করবেন না।
    ২. ফরম্যাটিংয়ের জন্য কেবল এইচটিএমএল ট্যাগ (<h2>, <h3>, <b>, <ul>, <li>) ব্যবহার করুন।
    ৩. নিচের সেকশনগুলো সাজিয়ে লিখুন:
        - <h2>{title} এর বিস্তারিত স্পেসিফিকেশন</h2>
        - <h2>কেন এই প্রোডাক্টটি কেনা উচিত?</h2>
        - <h2>বাংলাদেশে {title} এর দাম ও বাজারের অবস্থা</h2>
        - <h2>আমাদের চূড়ান্ত মতামত</h2>
    """

    # Free-tier model-gular talika
    free_models = [
        "gemini-3.8-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.6-flash"
    ]

    generated_text = ""

    # Free version-e fallback loop
    for cycle in range(1, 6):
        for model_name in free_models:
            for attempt in range(1, 3):
                try:
                    print(f"🤖 ফ্রি মডেল টেস্ট করা হচ্ছে: {model_name} (সাইকেল {cycle}, চেষ্টা {attempt})...")
                    
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                    )
                    
                    if response and response.text:
                        print(f"✅ সফল! {model_name} মডেল ব্যবহার করে কন্টেন্ট তৈরি করা হয়েছে।")
                        generated_text = response.text
                        break
                except APIError as e:
                    print(f"⚠️ এপিআই এরর - {model_name} (কোড {e.code}): {e.message}")
                    if e.code == 429:
                        time.sleep(20)
                    elif e.code == 503 or "high demand" in str(e).lower():
                        time.sleep(8)
                    else:
                        time.sleep(3)
                        break 
                except Exception as e:
                    print(f"⚠️ অপ্রত্যাশিত সমস্যা {model_name} এ: {e}")
                    time.sleep(3)
                    break
            if generated_text:
                break
        if generated_text:
            break
        print(f"🔄 সাইকেল {cycle} সম্পন্ন হয়েছে। পুনরায় চেষ্টা করা হচ্ছে...")
        time.sleep(10)

    if not generated_text:
        raise Exception("❌ বর্তমানে সমস্ত ফ্রি মডেলের কোটা লিমিটেড বা অতিরিক্ত ব্যস্ত রয়েছে।")

    # Original product image ebong affiliate link shoh CTA button toiri
    img_tag = f'<p><img src="{img_url}" alt="{title}" width="600" style="max-width:100%; height:auto; display:block; margin:0 auto 20px auto; border-radius:8px;"></p>' if img_url else ''
    
    cta_button = f'''
    <div style="text-align:center; margin:30px 0;">
        <a href="{affiliate_url}" target="_blank" style="background:#FF9900; color:#fff; padding:14px 28px; text-decoration:none; font-weight:bold; border-radius:5px; display:inline-block; font-size:16px;">Check Lowest Price on Amazon</a>
    </div>
    '''

    # Final HTML structure
    final_html = f"{img_tag}\n{generated_text}\n{cta_button}"
    
    return final_html
