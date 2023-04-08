import json
from bs4 import BeautifulSoup
import requests
from random import randint
from time import sleep


class ZillowSearch:
    def __init__(self,url, ctr):
        self.url = url
        # zillows requires user and language for the requests header
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/108.0.0.0 Safari/537.36 '
        self.accept_language = 'en-US,en;q=0.9'

        #Create soup of home page
        self.soup = self.create_soup(self.url)

        # Create a dictionary of features
        self.all_data = {
            "Full_address": [],
            "Area":[],
            "Apartment_Name":[],
            "sqft": [],
            "Beds": [],
            "Baths":[],
            "Price":[],
            }

        self.ctr=ctr

        #Extract features
        self.required_list_data()

    def create_soup(self,url):
        headers = {
            'User-Agent': self.user_agent,
            'Accept-Language': self.accept_language,
        }
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')


    def get_apartment_info(self, building_info):
        key_list_1 = list(building_info.keys())
        if 'pageProps' in key_list_1:
            key_prop_1 = "pageProps"
            find_result = building_info[key_prop_1]["initialReduxState"]["gdp"]["building"]
        else:
            key_prop_1 = "props"
            key_list_2 = list(building_info[key_prop_1].keys())
            if ('pageProps' in key_list_2) and ('initialReduxState' not in key_list_2):
                key_prop_2 = "pageProps"
                find_result = building_info[key_prop_1][key_prop_2]["initialReduxState"]["gdp"]["building"]
            else:
                find_result = building_info[key_prop_1]["initialReduxState"]["gdp"]["building"]
        return find_result

    def required_list_data(self):
        # Add delay to avoid server to be overloaded while scraping
        sleep(randint(1, 10))

        #soup of current page
        soup = self.soup

        # GET url of each building
        data = json.loads(soup.select_one("script[data-zrr-shared-data-key]").contents[0].strip("!<>-"))

        # Loop through each option of current page for buildings with multiple apartments
        for i in data["cat1"]['searchResults']['listResults']:

            #Get Link Information.
            link = i['detailUrl']
            if 'https' not in link: # If Link incomplete
                inner_soup = self.create_soup("https://www.zillow.com/" + link)
            else:
                inner_soup = self.create_soup(link)

            #Scrap building info
            main_soup =inner_soup.find('script', id='__NEXT_DATA__')

            if main_soup is not None:

                zillow_info = json.loads(main_soup.contents[0].strip("!<>-"))
                try:
                    apartment_info = self.get_apartment_info(zillow_info)

                    # Get values
                    for apartment in apartment_info["floorPlans"]:
                        self.all_data["Area"].append(apartment_info["breadcrumbs"][4]["text"])
                        self.all_data["Full_address"].append(apartment_info["fullAddress"])
                        self.ctr += 1
                        if apartment['units'] is None:
                            self.all_data["Price"].append(apartment["maxPrice"])
                        else:
                            self.all_data["Price"].append(apartment['units'][0]['price'])
                        self.all_data["Apartment_Name"].append(apartment["name"])
                        self.all_data["sqft"].append(apartment["sqft"])
                        self.all_data["Beds"].append(apartment["beds"])
                        self.all_data["Baths"].append(apartment["baths"])
                except:
                    pass


