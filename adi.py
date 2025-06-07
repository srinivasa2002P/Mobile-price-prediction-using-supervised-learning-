from flask import Flask, render_template, request, jsonify
import random
import smtplib
import ssl
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Temporary storage for OTPs (Use a database in production)
otp_storage = {}

# Email sender credentials (Replace with your actual credentials)
EMAIL_ADDRESS = "jsrinivasaadi@gmail.com"
EMAIL_PASSWORD = "uxzn dltp qikt zpvx"  # Use an App Password if using Gmail

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'message': 'Email is required!', 'success': False}), 400

    # Generate a 6-digit OTP
    otp = str(random.randint(100000, 999999))
    otp_storage[email] = otp  # Store OTP temporarily

    # Email content
    subject = "Your OTP for Mobile Price Prediction"
    body = f"Your OTP is: {otp}. It is valid for 5 minutes."
    message = f"Subject: {subject}\n\n{body}"

    try:
        # Sending the OTP via email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, email, message)

        return jsonify({'message': 'OTP sent successfully!', 'success': True})
    
    except Exception as e:
        print("Error:", e)
        return jsonify({'message': 'Error sending OTP!', 'success': False}), 500

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    entered_otp = data.get('otp')

    if not email or not entered_otp:
        return jsonify({'message': 'Email and OTP are required!', 'success': False}), 400

    # Check if the OTP is correct
    if email in otp_storage and otp_storage[email] == entered_otp:
        del otp_storage[email]  # Remove OTP after verification
        return jsonify({'message': 'OTP verified successfully!', 'success': True})
    else:
        return jsonify({'message': 'Invalid OTP!', 'success': False}), 400

if __name__ == '__main__':
    app.run(debug=True)
