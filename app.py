from flask import Flask,request,session
from twilio.rest import Client
import random
import settings
app = Flask(__name__)
app.secret_key = "OTP"
@app.route("/")
def index():
    return "Hello World"
@app.route("/getotp",methods=["POST","GET"])
def getotp():
    number = request.form["number"]
    # print("Number = ",number)
    print(type(number))
    val = getotpAPi(number)
    if val == "True":
        return val

@app.route("/validateotp",methods=["POST"])
def validate():
    otp = request.form['otp']
    if 'response' in session:
        s= session['response']
        session.pop('response',None)
        if s == otp:
            return "Autheticated"
        else:
            return "Not Authenticated"
    else:
        return "Session Expires"
def generateOTP():
    return random.randrange(1000,9999)
def getotpAPi(number):
    # print("Receive Number = ",number)
    acc_sid = settings.ACC_SID
    auth_token = settings.ACC_AUTH_TOKEN
    client = Client(acc_sid,auth_token)
    otp = generateOTP()
    session['response'] = str(otp)
    body = "Your OTP is " +str(otp)
    session['response'] = str(otp)
    message = client.messages.create(
        from_ = "+14158516954",
        body = body,
        to = number
    )
    if message.sid:
        return "True"
    else:
        "False"
if __name__ == "__main__":
    app.run(debug=True)
