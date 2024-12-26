from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': "OK ✅"
    })


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

        return jsonify(response), 200
    else:
        return jsonify({"message": "Request body must be JSON", "status": "error"}), 400

if __name__ == "__main__":
    app.run(debug=True)