# pip install -U flask flask-cors
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from email_features import extract_features
from model import PhishingDetector
from train_data import get_training_data

app = Flask(__name__)
cors = CORS(app)

# Initialize and train the model at startup
def initialize_model():
    phishing_emails, legitimate_emails = get_training_data()
    features_list = []
    labels = []
    
    for email in phishing_emails:
        features_list.append(extract_features(email))
        labels.append(1)
    
    for email in legitimate_emails:
        features_list.append(extract_features(email))
        labels.append(0)
    
    model = PhishingDetector()
    model.train(features_list, labels)
    return model

model = initialize_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    email_content = request.json.get('email_content', '')
    
    if not email_content:
        return jsonify({'error': 'No email content provided'}), 400
    
    features = extract_features(email_content)
    is_phishing = model.classify(features)
    confidence = model.predict(features)
    
    warnings = []
    if is_phishing:
        if features['url_count'] > 0:
            warnings.append('Contains suspicious URLs')
        if features['urgent_count'] > 0:
            warnings.append('Uses urgent language')
        if features['special_char_ratio'] > 0.1:
            warnings.append('Unusual number of special characters')
        if features['subject_caps_ratio'] > 0.5:
            warnings.append('Excessive use of capital letters')
    
    return jsonify({
        'is_phishing': is_phishing,
        'confidence': f'{confidence:.2%}',
        'warnings': warnings
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)