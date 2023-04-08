import json
import pickle
import numpy as np

__neighborhoods = None
__data_columns = None
__model = None


def get_estimator_price(neighborhood,sqft,beds,baths):
    try:
        neighborhood_index = __data_columns.index(neighborhood.lower())
    except:
        neighborhood_index= -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = beds
    x[2] = baths
    if neighborhood_index >= 0:
        x[neighborhood_index] = 1

    return round(__model.predict([x])[0],2)

def get_neighborhood_names():
    return __neighborhoods

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __neighborhoods

    with open("./artifacts/columns.json","r") as f:
        __data_columns = json.load(f)["data_columns"]
        __neighborhoods =__data_columns[3:]

    global __model
    with open("./artifacts/san_diego_home_prices_model.pickle","rb") as f:
        __model = pickle.load(f)

    print("loading saved artifacts...done")
