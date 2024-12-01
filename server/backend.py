from plaid_manager import PlaidManager
from flask import *

from flask_cors import CORS


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
    plaid_manager = PlaidManager()
    access_token = plaid_manager.create_access_token(data["publicToken"])
    plaid_manager.update_transactions(access_token)
    return "ok"

    

if __name__=="__main__":
    app.run(debug=True)