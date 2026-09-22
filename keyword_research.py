import random

# Real Amazon Products with Reliable Direct Images
HIGH_SEARCH_TECH_KEYWORDS = [
    {
        "title": "Sony WF-1000XM5 Truly Wireless Noise Canceling Earbuds 2026",
        "url": "https://www.amazon.com/dp/B0C33XXS56",
        "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&auto=format&fit=crop&q=80"
    },
    {
        "title": "Apple AirPods Pro (2nd Generation) Wireless Earbuds 2026",
        "url": "https://www.amazon.com/dp/B0C9C5B28M",
        "image": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=800&auto=format&fit=crop&q=80"
    },
    {
        "title": "JBL Flip 6 Portable Bluetooth Speaker 2026",
        "url": "https://www.amazon.com/dp/B09G3ZH93C",
        "image": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800&auto=format&fit=crop&q=80"
    },
    {
        "title": "Logitech MX Master 3S Wireless Performance Mouse 2026",
        "url": "https://www.amazon.com/dp/B09HM94VDS",
        "image": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800&auto=format&fit=crop&q=80"
    }
]

def get_high_search_product():
    return random.choice(HIGH_SEARCH_TECH_KEYWORDS)
