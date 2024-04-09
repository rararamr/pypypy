import requests
import pandas as pd
import sys

def shopee(url):
    shop_name = url.split('/')[-1]
    url = f'https://shopee.ph/api/v2/shop/get_shop_detail?sort_sold_out=0&username={shop_name}'
    req = requests.get(url)
    data_shop = req.json()
    try:
        shop_id = 67683510
        user_id = 0-67684967
    except KeyError:
        print("Missing 'data' or 'shopid' keys in response.")

    result = []
    count = 0
    while True:
        try:
            count += 6
            url = f'https://shopee.ph/api/v4/seller_operation/get_shop_ratings?limit=6&offset={count}&shop_id={shop_id}&user_id={user_id}'
            req = requests.get(url)
            data_req = req.json()

            for value in data_req['data']:
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
    df.to_csv(f'shoope_rating_{shop_name}.csv', index=False)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        url_shop = sys.argv[1]  # Get URL from first command-line argument
    else:
        url_shop = input("Enter Shopee shop URL: ")  # Prompt for URL if not provided

    shopee(url_shop)
