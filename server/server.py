from flask import  Flask, request, jsonify
import util
app = Flask(__name__)



@app.route("/get_neighborhood_names", methods=["GET"])
def get_neighborhood_names():
    response = jsonify({
        "neighborhoods": util.get_neighborhood_names()
    })
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

@app.route("/predict_home_price", methods=["POST"])
def predict_home_price():

    neighborhood = request.form["neighborhood"]
    sqft =float(request.form["sqft"])
    beds = int(request.form["beds"])
    baths = float(request.form["baths"])

    response= jsonify({
        "estimated_price": util.get_estimator_price(neighborhood,sqft,beds,baths)
    })
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

if __name__=="__main__":
    util.load_saved_artifacts()
    app.run()


## TODO: Routine to return the San Diego Neighborhoods
