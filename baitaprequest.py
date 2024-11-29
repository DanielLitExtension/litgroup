import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

base_url = "https://litdaniel.myshopify.com/admin/api/2024-10/"
access_token = os.getenv('ACCESS_TOKEN')

def get_headers():
    return {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json",
    }

def handle_response(response, success_message, failure_message):
    if response.status_code in [200, 201]:
        print(success_message)
        return response.json()
    else:
        print(f"{failure_message}. Status code: {response.status_code}")
        print("Logs:", response.text)
        return None

def get_products():
    response = requests.get(f"{base_url}/products.json", headers=get_headers())
    return handle_response(response, "Products retrieved", "Failed to retrieve products")

def get_custom_collections():
    response = requests.get(f"{base_url}/custom_collections.json", headers=get_headers())
    return handle_response(response, "Custom collections retrieved", "Failed to retrieve custom collections")

def get_customers():
    response = requests.get(f"{base_url}/customers.json", headers=get_headers())
    return handle_response(response, "Customers retrieved", "Failed to retrieve customers")

def get_orders():
    response = requests.get(f"{base_url}/orders.json", headers=get_headers())
    return handle_response(response, "Orders retrieved", "Failed to retrieve orders")

def create_smart_collection():
    products = get_products()
    product_id = products['products'][0]['id']    
    if product_id:
        payload = {
            "smart_collection": {
            "title": 'Smart Collection',
            "collects": [{"product_id": product_id}],
            "rules": [
                {
                    "column": "vendor",
                    "relation": "equals",
                    "value": "litdaniel"
                }
                ]
            }
        }    
        response = requests.post(f'{base_url}/smart_collections.json', headers=get_headers(), json=payload)
        return handle_response(response, "Create smart collection success", "Create smart collection failed")
    else:
        print("No products found")
        return None        


def create_custom_collection():
    products = get_products()
    product_id = products['products'][0]['id']
    if product_id:
        payload = {
            "custom_collection": {
                "title": "Custom Collection",
                "collects": [{"product_id": product_id}],
            },
        }
        response = requests.post(f"{base_url}/custom_collections.json", headers=get_headers(), json=payload)
        return handle_response(response, "Create custom collection success", "Create custom collection failed")
    else:
        print("No products found")
        return None

def create_product_no_option():
    payload = {
        "product": {
            "title": "Product no option",
            "status": "draft",
        },
    }
    response = requests.post(f"{base_url}/products.json", headers=get_headers(), json=payload)
    return handle_response(response, "Create product no option success", "Create product no option failed")

def create_product_have_option():
    payload = {
        "product": {
            "title": "Product have option",
            "variants": [
                {
                    "option1": "Red",
                    "option2": "Medium",
                    "option3": "Fabric",
                    "price": "1999999",
                },
                {
                    "option1": "white",
                    "option2": "Medium",
                    "option3": "Silk",
                    "price": "2999999",
                },
            ],
            "options": [
                {
                    "name": "Color",
                    "values": ["Red","white", "Yellow"],
                },
                {
                    "name": "Size",
                    "values": ["Small","Medium", "Large"],
                },
                {
                    "name": "Material",
                    "values": ["Fabric","Silk"],
                },               
            ],
        },
    }
    response = requests.post(f"{base_url}/products.json", headers=get_headers(), json=payload,)
    return handle_response(response, "Create product have option success", "Create product have option failed")


def create_customer():
    payload = {
        "customer": {
            "first_name": "Daniel",
            "last_name": "Nguyen",
            "phone": "0358071495",
            "email": "daniel3@litextension.com",
            "verified_email": True,
            "addresses": [
                {
                    "address": "Bac Tu Liem, Ha Noi",
                    "country": "vn",
                },
            ],
            "password": "12345678",
            "password_confirmation": "12345678",
        },
    }

    response = requests.post(f"{base_url}/customers.json", headers=get_headers(), json=payload)
    return handle_response(response, "Create customer success", "Create customer failed")

def create_order():
    products = get_products()
    customers = get_customers()
    
    product_id = products['products'][0]
    customer_id = customers['customers'][0]['id']
    
    payload = {
        "order": {
            "line_items": [
                {
                    "title": "Order",
                    "variant_id": product_id["variants"][0]["id"],
                    "price": product_id["variants"][0]["price"],
                },
            ],
            "customer": {"id": customer_id},
            "financial_status": "paid",
        },
    }

    response = requests.post(f"{base_url}/orders.json", headers=get_headers(), json=payload)
    return handle_response(response, "Create order success", "Create order failed")



def enable_inventory_tracking(variant_id):
    payload = {
        "variant": {
            "inventory_management": "shopify", 
            "inventory_policy": "continue",
            "inventory_quantity": 0  
        }
    }
    
    response = requests.put(
        f"{base_url}variants/{variant_id}.json", 
        headers=get_headers(), 
        json=payload
    )
    
    return handle_response(response, "Inventory tracking enabled successfully", "Failed to enable inventory tracking")

def update_product_inventory(product_id, variant_id, new_quantity):
    variant_response = requests.get(f"{base_url}variants/{variant_id}.json", headers=get_headers())
    variant_data = handle_response(variant_response, "Variant retrieved", "Failed to retrieve variant")

    print("variant Data:", variant_data)

    if not variant_data or not variant_data.get('variant'):
        print("Failed to retrieve variant data")
        return None
    
    variant = variant_data['variant']

    print("bariant_id:", variant['id'])
    print("inventory_item_id:", variant.get('inventory_item_id'))
    print("inventory_management:", variant.get('inventory_management'))
    print("inventory_policy:", variant.get('inventory_policy'))
    
    enable_inventory_tracking(variant_id)
    locations_response = requests.get(f"{base_url}locations.json", headers=get_headers())
    locations_data = handle_response(locations_response, "Locations retrieved", "Failed to retrieve locations")
    
    if not locations_data or not locations_data.get('locations'):
        print("No locations found")
        return None

    location_id = locations_data['locations'][0]['id']
    inventory_item_id = variant['inventory_item_id']
    
    payload = {
        "location_id": location_id,
        "inventory_item_id": inventory_item_id,
        "available": new_quantity
    }
    
    response = requests.post(f"{base_url}inventory_levels/set.json", headers=get_headers(), json=payload)
    return handle_response(response, "Product inventory updated successfully", "Failed to update product inventory")

def update_product_price(product_id, variant_prices):

    product_response = requests.get(f"{base_url}products/{product_id}.json", headers=get_headers())
    product_data = handle_response(product_response, "Product retrieved", "Failed to retrieve product")
    
    if not product_data or not product_data.get('product'):
        print("Failed to retrieve product data")
        return None
    payload = {
        "product": {
            "variants": [
                {
                    "id": variant["id"], 
                    "price": variant_prices.get(variant["id"], variant["price"])
                } 
                for variant in product_data['product']['variants']
            ]
        }
    }
    
    response = requests.put(f"{base_url}products/{product_id}.json", headers=get_headers(), json=payload)
    return handle_response(response, "Product price updated successfully for specified variants", "Failed to update product price")
def upload_product_image(product_id, image_url):
    payload = {
        "image": {
            "src": image_url
        }
    }
    
    response = requests.post(f"{base_url}products/{product_id}/images.json", headers=get_headers(), json=payload)
    
    return handle_response(response, "Product image uploaded successfully", "Failed to upload product image")


def update_recently_created_products():
    products = get_products()
    new_quantity = 100
    sample_image_url = "https://media-cdn-v2.laodong.vn/Storage/NewsPortal/2020/6/30/816260/Cho-1.jpg"
    
    if products and products.get('products') and len(products['products']) >= 2:
        recent_products = products['products'][-2:]
        
        for product in recent_products:
            product_id = product['id']
            
            if product['variants']:
                variant_prices = {}
                for variant in product['variants']:
                    new_price = input(f"Enter input {variant['id']}: ")
                    variant_prices[variant['id']] = new_price
                
                update_product_price(product_id, variant_prices)
                variant_id = product['variants'][0]['id']
                upload_product_image(product_id, sample_image_url)                
                update_product_inventory(product_id, variant_id, new_quantity)
            
        print("Updated price, image, and inventory for two most recent products")
    else:
        print("Not enough products to update")

def delete_resource(resource_type, resource_id):
    response = requests.delete(f"{base_url}/{resource_type}/{resource_id}.json", headers=get_headers())
    return handle_response(response, f"Delete {resource_type[:-1]} success", f"Delete {resource_type[:-1]} failed")

def main():
    create_product_have_option()
    create_product_no_option()
    create_custom_collection()
    create_smart_collection()    
    create_customer()
    create_order()
    update_recently_created_products()

    # resources_to_delete = {
    #     'custom_collections': get_custom_collections,
    #     'orders': get_orders,
    #     'customers': get_customers,
    #     'products': get_products
    # }

    # for resource_type, get_func in resources_to_delete.items():
    #     resources = get_func()
    #     if resources and resources.get(resource_type):
    #         for resource in resources[resource_type]:
    #             delete_resource(resource_type, resource['id'])

if __name__ == "__main__":
    main()