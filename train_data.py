def get_training_data():
    phishing_emails = [
        """URGENT: Your account has been suspended
        Dear valued customer,
        Your account has been temporarily suspended. Click here to verify:
        http://suspicious-site.com/verify
        Act immediately to prevent account closure.""",
        
        """Account Security Alert!!!
        We detected unusual activity. Verify now:
        http://192.168.1.1/secure
        Your account will be terminated in 24 hours!!!""",
    ]
    
    legitimate_emails = [
        """Team meeting reminder
        Hi everyone,
        Just a reminder about our weekly team meeting tomorrow at 10 AM.
        Best regards,
        John""",
        
        """Project update
        Hello team,
        The latest project deliverables have been uploaded to our secure server.
        Please review when you have a chance.
        Thanks""",
    ]
    
    return phishing_emails, legitimate_emails