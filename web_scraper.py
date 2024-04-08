import requests
import pandas as pd

url = "https://shopee.ph/api/v2/item/get_ratings"
shop_id = "1066504758"
item_id = "25562461389"
limit = 1
offset = 0
reviews = []

session = requests.Session()
session.headers.update({"Cookie": "_gcl_au=xxxx; SPC_IA=-1; SPC_EC=-; SPC_F=xxxx; SPC_U=-; SPC_T_ID=xxxx; SPC_T_IV=xxxx; SPC_SI=xxxx; _ga=xxxx; _gid=xxxx; cto_lwid=xxxx; _fbp=xxxx; _hjid=xxxx; SPC_SIxxxx=xxxx"})


# create an empty 'model_name' column in the DataFrame 'df'

while True:
    params = {
        "itemid": item_id,
        "shopid": shop_id,
        "offset": offset,
        "limit": limit,
        "filter": "0",
        "flag": "0",
        "sort": "0",
        "append": "0",
        "before_bundle": "",
        "language": "en",
    }

    response = session.get(url, params=params).json()
    if response["error"]:
        print(f"Error: {response['error']}")
        break
    elif response["data"]["ratings"]:
        print(offset)
        print (response["data"]["ratings"])

        for rating in response["data"]["ratings"]:
            # extract 'model_name' from 'product_items' column and store it in the 'model_name' column of the DataFrame 'df'
            model_name = rating.get('product_items')[0].get('model_name')
            rating['model_name'] = model_name
            reviews.append(rating)
            offset += limit

            # time.sleep(1)  # introduce a delay  of 1 second between requests
    else:
        break

df = pd.DataFrame(reviews)

print(f"Retrieved {len(reviews)} reviews.")
# extract 'skin suitability' and 'absorption' from 'comment' column
#df[['skin_suitability', 'absorption']] = df['comment'].str.extract('Skin Suitability:(.*?)\\nAbsorption:(.*?)\\n', expand=True)

# select columns to keep in the final CSV file
df = df[['orderid', 'itemid', 'userid', 'shopid', 'comment', 'rating_star']]
# df = df.to_string(index=False)

print(df.columns)

# save the DataFrame as a CSV file
df.to_csv('ShopeeScrap4.csv', index=False)