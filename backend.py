# MDM System - Backend (Python Flask) - Firebase Integrated

from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://your-firebase-db.firebaseio.com"})

app = Flask(__name__)

@app.route('/lock_device', methods=['POST'])
def lock_device():
    data = request.json
    ref = db.reference(f"/lock/{data.get('device_id')}")
    ref.set({"status": "lock"})
    return jsonify({"status": "Lock command sent"}), 200

if __name__ == '__main__':
    app.run(debug=True)
