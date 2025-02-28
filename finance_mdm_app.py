===== AndroidManifest.xml =====
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />

===== activity_main.xml =====
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp"
    android:background="#f4f4f4">

    <TextView android:id="@+id/tvLoanDetails" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Loan Details" android:textSize="22sp" android:textStyle="bold" android:gravity="center"/>
    <TextView android:id="@+id/tvLoanAmount" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Loan Amount: ₹0" android:textSize="18sp"/>
    <TextView android:id="@+id/tvInterestRate" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Interest Rate: 0%" android:textSize="18sp"/>
    <TextView android:id="@+id/tvTenure" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Tenure: 0 months" android:textSize="18sp"/>
    <TextView android:id="@+id/tvEmiAmount" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="EMI: ₹0" android:textSize="18sp" android:textColor="#009688" android:textStyle="bold"/>
    <Button android:id="@+id/btnViewEMI" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="View EMI Schedule" android:backgroundTint="#009688" android:textColor="#fff"/>
    <Button android:id="@+id/btnPayEMI" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Pay EMI Now" android:backgroundTint="#FF5722" android:textColor="#fff"/>
</LinearLayout>

===== MainActivity.java =====
package com.example.financeapp;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.FirebaseFirestore;

public class MainActivity extends AppCompatActivity {
    FirebaseFirestore db;
    FirebaseAuth auth;
    TextView tvLoanAmount, tvInterestRate, tvTenure, tvEmiAmount;
    Button btnViewEMI, btnPayEMI;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        auth = FirebaseAuth.getInstance();
        db = FirebaseFirestore.getInstance();

        tvLoanAmount = findViewById(R.id.tvLoanAmount);
        tvInterestRate = findViewById(R.id.tvInterestRate);
        tvTenure = findViewById(R.id.tvTenure);
        tvEmiAmount = findViewById(R.id.tvEmiAmount);
        btnViewEMI = findViewById(R.id.btnViewEMI);
        btnPayEMI = findViewById(R.id.btnPayEMI);

        fetchLoanDetails();

        btnViewEMI.setOnClickListener(v -> startActivity(new Intent(MainActivity.this, EmiScheduleActivity.class)));
        btnPayEMI.setOnClickListener(v -> startActivity(new Intent(MainActivity.this, PaymentActivity.class)));
    }

    private void fetchLoanDetails() {
        String userId = auth.getCurrentUser().getUid();
        db.collection("loans").document(userId).get()
                .addOnSuccessListener(documentSnapshot -> {
                    if (documentSnapshot.exists()) {
                        tvLoanAmount.setText("Loan Amount: ₹" + documentSnapshot.getString("loanAmount"));
                        tvInterestRate.setText("Interest Rate: " + documentSnapshot.getString("interestRate") + "%");
                        tvTenure.setText("Tenure: " + documentSnapshot.getString("tenure") + " months");
                        tvEmiAmount.setText("EMI: ₹" + documentSnapshot.getString("emiAmount"));
                    }
                });
    }
}

===== PaymentActivity.java =====
package com.example.financeapp;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

public class PaymentActivity extends AppCompatActivity {
    Button btnPayNow;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_payment);

        btnPayNow = findViewById(R.id.btnPayNow);
        btnPayNow.setOnClickListener(v -> Toast.makeText(PaymentActivity.this, "Redirecting to Payment Gateway...", Toast.LENGTH_SHORT).show());
    }
}

===== Fraud Detection API (Python Flask) =====
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/fraud-detection', methods=['POST'])
def fraud_detection():
    data = request.json
    loan_amount = int(data["loanAmount"])
    if loan_amount > 1000000:
        return jsonify({"status": "Fraud Detected"})
    return jsonify({"status": "Safe Transaction"})

if __name__ == '__main__':
    app.run(debug=True)
