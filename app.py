from flask import Flask, render_template, request, jsonify, session
from flask_mail import Mail, Message
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ✅ Configure Flask-Mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "jsrinivasaadi@gmail.com"  # Replace with your email
app.config["MAIL_PASSWORD"] = "your google app password"  # Replace with your generated app password

mail = Mail(app)

# ✅ Route to render the login page
@app.route("/")
def index():
    return render_template("index.html")

# ✅ Route to send OTP
@app.route("/send-otp", methods=["POST"])
def send_otp():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")

    if not username or not email:
        return jsonify({"message": "Email and Username are required!", "success": False}), 400

    otp = str(random.randint(100000, 999999))  # Generate 6-digit OTP
    session["otp"] = otp  # Store OTP in session

    # ✅ Use correct Imgur direct link here
    image_src = "https://i.imgur.com/NxxhDNQ.jpg"  # Correct link should end with .jpg or .png

    # ✅ Email Content
    subject = "Welcome to Mobile Price Prediction - OTP Verification"
    body = f"""
    <html>
    <body>
        <h2>Welcome, {username}!</h2>
        <p>Your OTP is: <strong>{otp}</strong></p>
        <p>This OTP is valid for 5 minutes.</p>
        <img src="{image_src}" width="200"/>
    </body>
    </html>
    """

    try:
        msg = Message(subject, sender=app.config["MAIL_USERNAME"], recipients=[email])
        msg.html = body
        mail.send(msg)
        return jsonify({"message": "OTP sent successfully!", "success": True})
    except Exception as e:
        return jsonify({"message": f"Error sending OTP: {str(e)}", "success": False}), 500

# ✅ Route to verify OTP
@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    entered_otp = data.get("otp")

    if "otp" in session and session["otp"] == entered_otp:
        return jsonify({"message": "OTP Verified Successfully!", "success": True})
    else:
        return jsonify({"message": "Invalid OTP, please try again!", "success": False}), 400


if __name__ == "__main__":
    app.run(debug=True)
