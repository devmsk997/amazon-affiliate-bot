import random

HIGH_SEARCH_TECH_KEYWORDS = [
    {"title": "Best Noise Canceling Wireless Earbuds 2026", "url": "https://www.amazon.com/dp/B0CX23VJPZ", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600"},
    {"title": "Top Smartwatches with Long Battery Life 2026", "url": "https://www.amazon.com/dp/B0CHX1W1XY", "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600"},
    {"title": "Best Portable Bluetooth Speakers 2026", "url": "https://www.amazon.com/dp/B0BSHF7WH3", "image": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=600"},
    {"title": "Top Ergonomic Wireless Gaming Mouse 2026", "url": "https://www.amazon.com/dp/B0C3322Y3X", "image": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=600"}
]

def get_high_search_product():
    return random.choice(HIGH_SEARCH_TECH_KEYWORDS)
