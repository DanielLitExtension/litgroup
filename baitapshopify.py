import shopify
import requests
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('API_KEY')
access_token = os.getenv('ACCESS_TOKEN')
api_version = '2024-10'
shop_url = os.getenv('SHOP_URL')

session = shopify.Session(shop_url, api_version, access_token)
shopify.ShopifyResource.activate_session(session)

def create_a_product(product_data):
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session)
    variants = []
    new_product = shopify.Product()
    if 'variants' in product_data:
        for item in product_data['variants']:
            variant = shopify.Variant(item)
            variants.append(variant)
        product_data['variants'] = variants
    
    for key, value in product_data.items():
        setattr(new_product, key, value)
    
    new_product.save()
    print(new_product.id)
    print(new_product.to_dict())


def edit_a_product(product_id, product_data):
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session)

    variants = []
    product = shopify.Product.find(product_id)  

    if 'variants' in product_data:
        for item in product_data['variants']:
            variant = shopify.Variant(item)
            variants.append(variant)
        product_data['variants'] = variants
    
    for key, value in product_data.items():
        setattr(product, key, value)

    result = product.save()
    print(result)

def create_a_customer(customer_data):
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session)

    new_customer = shopify.Customer()
    for key, value in customer_data.items():
        setattr(new_customer, key, value)

    new_customer.save()
    print(new_customer.to_dict())

def edit_a_customer(customer_id, customer_data):
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session)

    customer = shopify.Customer().find(customer_id)
    for key, value in customer_data.items():
        setattr(customer, key, value)

    result = customer.save()
    print(result)

def create_an_order(order_data):
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session)

    new_order = shopify.Order()
    for key, value in order_data.items():       
        setattr(new_order, key, value)

    result = new_order.save()
    print(result)
    print(new_order.id)
    print(new_order.to_dict())

def edit_an_order(order_id, order_data):
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session)

    order = shopify.Order.find(order_id)
    for key, value in order_data.items():       
        setattr(order, key, value)

    result = order.save()
    print(result)

product_json_data = {
    "title": "test title Y", 
    "body_html": "body of the page <br/><br/> test <br/> test", 
    "variants": [
        {
            'price': 1333300, 
            'requires_shipping': False,
            'sku': '000009'
        }
    ]
}
create_a_product(product_json_data)

product_edit_data = {
    "title": "test title Y", 
    "body_html": "body of the page <br/><br/> test <br/> test", 
    "variants": [
        {
            'price': 1200000, 
            'requires_shipping': False,
            'sku':'000008'
        }
    ]
}

edit_a_product(9648802005277, product_edit_data)

customer_create_data = {
    'first_name': 'John', 
    'last_name': 'Travolta', 
    'email': 'travolta@travolta.com'
}
create_a_customer(customer_create_data)

customer_edit_data = {
    'first_name': 'John', 
    'last_name': 'Travolta', 
    'email': 'travolta@gmail.com'
}
# edit_a_customer(2716826796135, customer_edit_data)

order_create_data = {
    "line_items": [
        {
            "title": "A product",
            "price": 74.99,
            "grams": "1300",
            "quantity": 3,
            "tax_lines": [
                { 
                    "price": 13.5,    
                    "rate": 0.06,    
                    "title": "State tax"  
                }
            ]
        }, 
        {
            "title": "Another product",
            "price": 24.99,
            "quantity": 9
        }
    ],
    "email": 'foo@foo.com', 
    "shipping_address": {
        "first_name": "John",
        "last_name": "Smith",
        "address1": "123 Fake Street",
        "phone": "555-555-5555",
        "city": "Fakecity",
        "province": "Ontario",
        "country": "Canada",
        "zip": "K2P 1L4"
    },
    "billing_address": {
        "first_name": "John",
        "last_name": "Smith",
        "address1": "123 Fake Street",
        "phone": "555-555-5555",
        "city": "Fakecity",
        "province": "Ontario",
        "country": "Canada",
        "zip": "K2P 1L4"
    }
}
create_an_order(order_create_data)

# Sửa đơn hàng
order_edit_data = {
    "line_items": [
        {
            "title": "A product",
            "price": 74.99,
            "grams": "1300",
            "quantity": 3,
            "tax_lines": [
                { 
                    "price": 13.5,    
                    "rate": 0.06,    
                    "title": "State tax"  
                }
            ]
        }, 
        {
            "title": "Another product",
            "price": 24.99,
            "quantity": 9
        }
    ],
    "email": 'foo@foo.com', 
    "shipping_address": {
        "first_name": "John",
        "last_name": "Smith",
        "address1": "123 Fake Street",
        "phone": "555-555-5555",
        "city": "Fakecity",
        "province": "Ontario",
        "country": "Canada",
        "zip": "K2P 1L4"
    },
    "billing_address": {
        "first_name": "John",
        "last_name": "Smith",
        "address1": "123 Fake Street",
        "phone": "555-555-5555",
        "city": "Fakecity",
        "province": "Ontario",
        "country": "Canada",
        "zip": "K2P 1L4"
    }
}
# edit_an_order(1870932901991, order_edit_data)