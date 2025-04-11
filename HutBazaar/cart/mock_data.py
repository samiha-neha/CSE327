"""
Mock product data for development/testing without a Product model.
"""

MOCK_PRODUCTS = [
    {"id": 1, "name": "Mock Shoes", "price": 49.99},
    {"id": 2, "name": "Mock Hat", "price": 19.99},
    {"id": 3, "name": "Mock T-shirt", "price": 25.00},
]


def get_product_by_id(product_id):
    return next((p for p in MOCK_PRODUCTS if p["id"] == product_id), None)