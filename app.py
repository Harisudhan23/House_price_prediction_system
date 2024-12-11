from flask import Flask, render_template, request, jsonify
import joblib

app = Flask(__name__)

# Load the trained model
model = joblib.load('D:/ENtrans/house_price.pkl')

# List of required fields
REQUIRED_FIELDS = [
    'longitude', 'latitude', 'housing_median_age', 'total_rooms',
    'total_bedrooms', 'population', 'households', 'median_income',
    'ocean_proximity_INLAND', 'ocean_proximity_ISLAND',
    'ocean_proximity_NEAR BAY', 'ocean_proximity_NEAR OCEAN'
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("Received Data:", data)

        # Check for missing fields
        missing_fields = [field for field in REQUIRED_FIELDS if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

        # Extract features
        features = [
            data['longitude'], data['latitude'], data['housing_median_age'],
            data['total_rooms'], data['total_bedrooms'], data['population'],
            data['households'], data['median_income'], data['ocean_proximity_INLAND'],
            data['ocean_proximity_ISLAND'], data['ocean_proximity_NEAR BAY'],
            data['ocean_proximity_NEAR OCEAN']
        ]

        # Make prediction
        prediction = model.predict([features])

        return jsonify({'predicted_price': prediction[0]})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
