from plaid_manager import PlaidManager
from flask import *
from email_sending import EmailSender
from flask_cors import CORS
import os
from dotenv import load_dotenv


# # Usage example:
# if __name__ == "__main__":
#     plaid_manager = PlaidManager()
#     link_token = plaid_manager.create_link_token("test-user-123")
    
#     if link_token:
#         print(f"Successfully created link token: {link_token}")

app = Flask(__name__)
CORS(app)

@app.route("/api/getlinktoken", methods=["GET"])
def get_link_token():
    plaid_manager = PlaidManager()
    link_token = plaid_manager.create_link_token()  # For testing
    if link_token:
        return jsonify({"link_token": link_token})
    else:
        return jsonify({"error": "Failed to create link token"}), 400

@app.route("/api/sendaccesstoken", methods = ["POST"])
def get_access_token():
    data = request.get_json()
    if not data or "publicToken" not in data:
        return jsonify({"Error":"Send public token."}), 400
    plaid_manager = PlaidManager()
    try:
        access_token = plaid_manager.create_access_token(data["publicToken"])
        if not access_token:
            return jsonify({"Error":"Unable to fetch access token"}), 500
        plaid_manager.update_transactions(access_token)
    except:
        return jsonify({"Error": "Some error ocurred"}), 500
    return {"Success":"Access token acquired."}, 200


@app.route("/api/trig_cron_send", methods=["GET"])
def send_email():
    #TODO:
    """
    need to hit this endpoint periodically, probably need to be triggered by a cron job, will send emails to every user that exists

    """

    plaidthing = PlaidManager()
    output = plaidthing.get_prev_transactions("access-sandbox-7b271418-b0a6-43d5-a2cf-2734fc7b84c0",20)
    load_dotenv()
    emailsender = EmailSender(os.getenv("VERIFIED_SENDING_EMAIL"))
    #TODO:iterate over all users and send, for now just one
    subject, content = emailsender.render_html(output)
    emailsender.send_email("krishivgubba626@gmail.com", subject, content)
    return {"Success":"Email sent successfully"}, 200

    

    

if __name__=="__main__":
    app.run(debug=True)