import requests
import csv
from datetime import datetime

def shopee(url):
    shop_id = url.split('/')[-1]    
    url = f'https://shopee.ph/api/v4/shop/get_shop_detail?sort_sold_out=0&shop_id={shop_id}'
    req = requests.get(url)
    data_shop = req.json()
    print(data_shop)
    global user_id
    if 'data' in data_shop:
        shop_id = data_shop['data']['shopid']
    else:
        print("Error: 'data' key not found in shop details.")
    if 'data' in data_shop:
        user_id = data_shop['data']['userid']
    else:
        print("Error: 'data' key not found in shop details.")
    # Handle the missing data gracefully, perhaps by exiting or retrying        
    count = 0
    result = []
    while True:
        try:
            count += 6
            url = f'https://shopee.ph/api/v4/seller_operation/get_shop_ratings?limit=6&offset={count}&shop_id={shop_id}&user_id={user_id}'
            req = requests.get(url)
            data_req = req.json()            
            for value in data_req['data']:
                data_result = {
                    'Name': value['author_username'],
                    'Product': value['product_items'][0]['name'],
                    'Review': value['comment'],
                    'Rating': value['rating_star'],
                    'Transaction Date': datetime.utcfromtimestamp(value['ctime']).strftime('%Y-%m-%d %H:%M')
                }
                result.append(data_result)
        except KeyError:        
            break
        
    # save to csv    
    keys = result[0].keys()
    with open(f'shoope_rating_{shop_id}.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(result)        


if __name__ == '__main__':    
    #silakan ganti url_shope jika ingin mengambil data review dan rating dari toko lain
    url_shop = 'https://shopee.ph/thrifted.lgn'
    shopee(url_shop)