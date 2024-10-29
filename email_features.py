import re
from typing import Dict, List

def extract_features(email_content: str) -> Dict[str, float]:
    features = {}
    
    # Lowercase the content
    email_content = email_content.lower()
    
    # URL related features
    features['url_count'] = len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', email_content))
    features['ip_url_count'] = len(re.findall(r'http[s]?://\d+\.\d+\.\d+\.\d+', email_content))
    
    # Language features
    urgent_words = ['urgent', 'immediate', 'action required', 'account suspended', 'verify', 'suspended']
    features['urgent_count'] = sum(1 for word in urgent_words if word in email_content)
    
    # Special character features
    features['special_char_ratio'] = len(re.findall(r'[^a-zA-Z0-9\s]', email_content)) / len(email_content) if email_content else 0
    
    # Subject line features
    subject_line = email_content.split('\n')[0] if '\n' in email_content else email_content
    features['subject_caps_ratio'] = sum(1 for c in subject_line if c.isupper()) / len(subject_line) if subject_line else 0
    
    return features