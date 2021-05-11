from flask import Flask,request,session
from twilio.rest import Client
import random
app = Flask(__name__)
app.secret_key = "OTP"
@app.route("/")
def index():
    return "Hello World"

@app.route('/product/<id>/<token>')
def get_product(id,token):
  return "The product is " + str(id)

@app.route("/getotp/<id>/<token>",methods=["POST","GET"])
def getotp(id,token):
    number = request.form["number"]
    val = getotpAPi(number,str(id),str(token))
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
def getotpAPi(number,ids,token):
    # print("Receive Number = ",number)
    acc_sid = ids
    auth_token = token
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
