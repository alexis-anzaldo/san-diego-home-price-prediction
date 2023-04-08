from search_zillow import ZillowSearch
import pandas as pd

# search query any place in rent in San Diego CA
zillow_url = "https://www.zillow.com/san-diego-ca/rentals/?searchQueryState" \
             "=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20D" \
             "iego%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.9123537" \
             "4414063%2C%22east%22%3A-116.30560325585938%2C%22south%22%3A32.36" \
             "072020501597%2C%22north%22%3A33.28623992760275%7D%2C%22regionSelect" \
             "ion%22%3A%5B%7B%22regionId%22%3A54296%2C%22regionType%22%3A6%7D%5D" \
             "%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3" \
             "A%7B%22min%22%3A0%7D%2C%22mp%22%3A%7B%22min%22%3A0%7D%2C%22fsba%22" \
             "%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%" \
             "7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22valu" \
             "e%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%2" \
             "2%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D" \
             "%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3At" \
             "rue%7D"

# Get all URLs
url_list = [zillow_url]
for url_num in range(2, 21):
    change_url = f"{zillow_url[:44]}{url_num}_p/{zillow_url[44:88]}22currentPage%22%3A{url_num}%{zillow_url[88:]}"
    url_list.append(change_url)


# Create a dictionary of features
raw_data_list = []

page_ =1
ctr=0

from collections import defaultdict

for url in url_list:
    print(page_)
    z = ZillowSearch(url, ctr)

    ctr=z.ctr
    # Concatenate features of each page
    d = z.all_data
    df=pd.DataFrame.from_dict(z.all_data)
    raw_data_list.append(df)

    page_+=1

# Save Data as CSV
main_df = pd.concat(raw_data_list).to_csv("data/San_Diego_Raw_Data.csv")