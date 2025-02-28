===== AndroidManifest.xml =====
<uses-permission android:name="android.permission.BIND_DEVICE_ADMIN" />
<uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />

<receiver
    android:name=".AdminReceiver"
    android:permission="android.permission.BIND_DEVICE_ADMIN">
    <meta-data
        android:name="android.app.device_admin"
        android:resource="@xml/device_admin" />
</receiver>

===== device_admin.xml =====
<?xml version="1.0" encoding="utf-8"?>
<device-admin xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-policies>
        <limit-password />
        <watch-login />
        <reset-password />
        <force-lock />
        <wipe-data />
    </uses-policies>
</device-admin>

===== AdminReceiver.java =====
package com.example.financeapp;

import android.app.admin.DeviceAdminReceiver;
import android.content.Context;
import android.content.Intent;
import android.widget.Toast;

public class AdminReceiver extends DeviceAdminReceiver {
    @Override
    public void onEnabled(Context context, Intent intent) {
        Toast.makeText(context, "Finance Lock Enabled", Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onDisabled(Context context, Intent intent) {
        Toast.makeText(context, "Finance Lock Disabled! Admin Access Required.", Toast.LENGTH_LONG).show();
    }
}

===== MainActivity.java =====
package com.example.financeapp;

import android.app.admin.DevicePolicyManager;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private DevicePolicyManager devicePolicyManager;
    private ComponentName adminReceiver;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        devicePolicyManager = (DevicePolicyManager) getSystemService(Context.DEVICE_POLICY_SERVICE);
        adminReceiver = new ComponentName(this, AdminReceiver.class);

        Button btnActivateAdmin = findViewById(R.id.btnActivateAdmin);
        btnActivateAdmin.setOnClickListener(v -> activateAdmin());

        checkAdminPermission();
    }

    private void activateAdmin() {
        Intent intent = new Intent(DevicePolicyManager.ACTION_ADD_DEVICE_ADMIN);
        intent.putExtra(DevicePolicyManager.EXTRA_DEVICE_ADMIN, adminReceiver);
        intent.putExtra(DevicePolicyManager.EXTRA_ADD_EXPLANATION, "Activate Finance Lock for security.");
        startActivity(intent);
    }

    private void checkAdminPermission() {
        if (!devicePolicyManager.isAdminActive(adminReceiver)) {
            Toast.makeText(this, "Finance Lock Not Activated! Enable Now.", Toast.LENGTH_LONG).show();
        }
    }
}

===== Additional Features =====
- Prevents Uninstall Without Admin Permission
- Restricts Factory Reset
- Remote Lock via Admin Panel
- Alerts Admin on SIM Change
- Future Enhancements: AI Security, Geofencing Lock, Remote Admin Control
