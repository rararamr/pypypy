import requests
import pandas as pd
import sys

def shopee(shop_id):
    user_id = 0  # Assuming user ID is not relevant for shop ratings
    count = 0
    result = []
    while True:
        try:
            count += 6
            url = f'https://shopee.ph/api/v4/seller_operation/get_shop_ratings?limit=6&offset={count}&shop_id={shop_id}&user_id={user_id}'
            req = requests.get(url)
            data_req = req.json()

            for value in data_req.get('data', []):  # Handle potential missing 'data' key
                data_result = {
                    'nama pengguna': value['author_username'],
                    'produk': value['product_items'][0]['name'],
                    'review': value['comment'],
                    'rating': value['rating_star'],
                }
                result.append(data_result)
        except KeyError:
            break

    # Create Pandas DataFrame
    df = pd.DataFrame(result)

    # Save DataFrame to CSV
    df.to_csv(f'shoope_rating_{shop_id}.csv', index=False)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        shop_id = sys.argv[1]  # Get shop ID from first command-line argument
    else:
        shop_id = input("Enter Shopee shop ID: ")  # Prompt for ID if not provided

    shopee(shop_id)
