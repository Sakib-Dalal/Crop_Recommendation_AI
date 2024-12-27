from flask import Flask, jsonify, request
from joblib import load
import requests
import json
import os
from dotenv import load_dotenv
import random

app = Flask(__name__)
load_dotenv()

LLM_URL = "http://localhost:11434/api/generate"
headers = {
    "Content-Type": "application/json"
}

# sklearn model 
model = load("../../Model/crop_recommendation_model.joblib")

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': "OK ✅"
    })

def model_predict(data):
    prediction = model.predict(data)
    return prediction

def llm_get(crop):
    data = {
        "model": "llama3.2:1b",
        "prompt": f"How to grow {crop} in detail. Help the farmer to answer this question. write only 1 paragraph",
        "stream": False
    }
    try:
        llm_res = requests.post(LLM_URL, headers=headers, data=json.dumps(data))
        llm_res.raise_for_status()  # Raise an error for HTTP 4xx/5xx
        return llm_res.json()  # Return the parsed JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to LLM: {e}")
        return {"error": "Failed to connect to LLM service"}
    
def get_image(text):
    # https://pixabay.com/api/docs/
    if "beans" in text:
        text = text.replace("beans", "+beans")

    url_image_gen = "https://pixabay.com/api/"
    params = {
        "key": os.environ.get('IMAGE_FIND_API_KEY'), # Get API Key from pixabay.com
        "q": text,
        "image_type": "photo",
        "orientation": "horizontal",
        "per_page": "3",
        "pretty": "true"
    }

    image_res = requests.get(url_image_gen, params=params)
    print(image_res.json())
    num = [0, 1]
    r_num = random.choice(num)
    return image_res.json()["hits"][r_num]["largeImageURL"]


@app.route('/submit', methods=['POST'])
def handle_post():
    if request.is_json:
        # Parse JSON data sent from Node.js server
        data = request.get_json()
        print("Data received from Node.js server:", data)
        
        # Process the data
        nitrogen = data.get('Nitrogen', 'Unknown')
        phosphorus = data.get('Phosphorus', 'Unknown')
        potassium = data.get('Potassium', 'Unknown')
        temperature = data.get('Temperature', 'Unknown')
        humidity = data.get('Humidity', 'Unknown')
        ph = data.get('Ph', 'Unknown')
        rainfall = data.get('Rainfall', 'Unknown')

        # Create a response
        response = {
            "Nitrogen": nitrogen,
            "Phosphorus": phosphorus,
            "Potassium": potassium,
            "Temperature": temperature,
            "Humidity": humidity,
            "Ph": ph,
            "Rainfall": rainfall,
            "Message": "Data processed successfully"
        }

        data = [[float(nitrogen), float(phosphorus), float(potassium), float(temperature), float(humidity), float(ph), float(rainfall)]]

        crop =  model_predict(data)[0]
        llm_output = llm_get(crop)

        print(crop)
        print(llm_output["response"])

        try:
            image_url = get_image(text=crop)
        except:
            image_url = "https://static.vecteezy.com/system/resources/previews/012/181/008/original/document-data-file-not-found-concept-illustration-flat-design-eps10-modern-graphic-element-for-landing-page-empty-state-ui-infographic-icon-etc-vector.jpg"

        prediction = {"prediction": crop, "llm_message": llm_output["response"], "crop_image": image_url}
        print(prediction)
        
        return jsonify(prediction), 200
    else:
        return jsonify({"message": "Request body must be JSON", "status": "error"}), 400

if __name__ == "__main__":
    app.run(debug=True)



