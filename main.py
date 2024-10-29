from email_features import extract_features
from model import PhishingDetector
from train_data import get_training_data

def train_model() -> PhishingDetector:
    # Get training data
    phishing_emails, legitimate_emails = get_training_data()
    
    # Prepare features and labels
    features_list = []
    labels = []
    
    # Process phishing emails
    for email in phishing_emails:
        features_list.append(extract_features(email))
        labels.append(1)  # 1 for phishing
    
    # Process legitimate emails
    for email in legitimate_emails:
        features_list.append(extract_features(email))
        labels.append(0)  # 0 for legitimate
    
    # Train the model
    model = PhishingDetector()
    model.train(features_list, labels)
    
    return model

def analyze_email(email_content: str, model: PhishingDetector) -> tuple:
    # Extract features from the email
    features = extract_features(email_content)
    
    # Get prediction
    is_phishing = model.classify(features)
    confidence = model.predict(features)
    
    return is_phishing, confidence

def main():
    print("Training phishing detection model...")
    model = train_model()
    
    print("\nEmail Phishing Detection System")
    print("===============================")
    print("Enter your email content (press Ctrl+D or Ctrl+Z when finished):")
    
    # Read multi-line input
    email_lines = []
    try:
        while True:
            line = input()
            email_lines.append(line)
    except EOFError:
        email_content = '\n'.join(email_lines)
    
    # Analyze the email
    is_phishing, confidence = analyze_email(email_content, model)
    
    # Display results
    print("\nAnalysis Results:")
    print("----------------")
    print(f"Verdict: {'PHISHING' if is_phishing else 'LEGITIMATE'}")
    print(f"Confidence: {confidence:.2%}")
    
    if is_phishing:
        print("\nWarning Signs:")
        features = extract_features(email_content)
        if features['url_count'] > 0:
            print("- Contains suspicious URLs")
        if features['urgent_count'] > 0:
            print("- Uses urgent language")
        if features['special_char_ratio'] > 0.1:
            print("- Unusual number of special characters")
        if features['subject_caps_ratio'] > 0.5:
            print("- Excessive use of capital letters")

if __name__ == "__main__":
    main()