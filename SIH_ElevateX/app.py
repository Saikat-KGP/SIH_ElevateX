from flask import Flask, render_template, request
import pickle
import numpy as np

from model import GeoSpatialQuerySystem

app = Flask(__name__)
model = pickle.load(open('modelsih.pkl', 'rb'))
@app.route('/')
def man():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    sentence = request.form['sentence']
    # data2 = request.form['b']
  
    place_names = GeoSpatialQuerySystem().identify_place_names(sentence)
    # prediction = model.predict(place_names)
    return render_template('home.html', prediction_text='IDENTIFIED PLACE NAMES ARE...  {}'.format(place_names), place_names=place_names)

if __name__ == "__main__":
    app.run(debug=True)

  #api_key = "YOUR_API_KEY"    

  #url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(place_names, api_key)
  #response = requests.get(url)

 
 # latitude = response.json()['results'][0]['geometry']['location']['lat']
  #longitude = response.json()['results'][0]['geometry']['location']['lng']

  
#  google_maps_url = "https://www.google.com/maps/search/?api=1&query={}+{}".format(latitude, longitude)

  #return render_template('home.html', prediction_text='IDENTIFIED PLACE NAMES ARE...  {}'.format(place_names), google_maps_url=google_maps_url)
