import random

# Real Amazon Products with valid ASINs & Images
HIGH_SEARCH_TECH_KEYWORDS = [
    {
        "title": "Sony WF-1000XM5 Truly Wireless Noise Canceling Earbuds 2026",
        "url": "https://www.amazon.com/dp/B0C33XXS56",
        "image": "https://m.media-amazon.com/images/I/5144XvS8fAL._AC_SL1200_.jpg"
    },
    {
        "title": "Apple AirPods Pro (2nd Generation) Wireless Earbuds 2026",
        "url": "https://www.amazon.com/dp/B0C9C5B28M",
        "image": "https://m.media-amazon.com/images/I/61SUj2aKoEL._AC_SL1500_.jpg"
    },
    {
        "title": "JBL Flip 6 Portable Bluetooth Speaker 2026",
        "url": "https://www.amazon.com/dp/B09G3ZH93C",
        "image": "https://m.media-amazon.com/images/I/718bI3q8e9L._AC_SL1500_.jpg"
    },
    {
        "title": "Logitech MX Master 3S Wireless Performance Mouse 2026",
        "url": "https://www.amazon.com/dp/B09HM94VDS",
        "image": "https://m.media-amazon.com/images/I/61ni3t1ryQL._AC_SL1500_.jpg"
    }
]

def get_high_search_product():
    return random.choice(HIGH_SEARCH_TECH_KEYWORDS)
