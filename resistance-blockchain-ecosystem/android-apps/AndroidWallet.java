package com.resistance.blockchain.wallet;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Resistance Blockchain Android Wallet
 * Privacy is Resistance | Censorship is Control
 */
public class AndroidWallet extends Activity {
    
    private TextView addressText;
    private TextView balanceText;
    private EditText recipientEdit;
    private EditText amountEdit;
    private Button generateWalletBtn;
    private Button sendTransactionBtn;
    private Button refreshBalanceBtn;
    
    private String walletAddress = "";
    private double balance = 0.0;
    private ExecutorService executor = Executors.newSingleThreadExecutor();
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_wallet);
        
        initializeViews();
        setupListeners();
        updateUI();
    }
    
    private void initializeViews() {
        addressText = findViewById(R.id.addressText);
        balanceText = findViewById(R.id.balanceText);
        recipientEdit = findViewById(R.id.recipientEdit);
        amountEdit = findViewById(R.id.amountEdit);
        generateWalletBtn = findViewById(R.id.generateWalletBtn);
        sendTransactionBtn = findViewById(R.id.sendTransactionBtn);
        refreshBalanceBtn = findViewById(R.id.refreshBalanceBtn);
    }
    
    private void setupListeners() {
        generateWalletBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                generateWallet();
            }
        });
        
        sendTransactionBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendTransaction();
            }
        });
        
        refreshBalanceBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                refreshBalance();
            }
        });
    }
    
    private void generateWallet() {
        executor.execute(new Runnable() {
            @Override
            public void run() {
                // Simulate wallet generation
                walletAddress = "9wviCeWe2D8XS82k2ovp5EUYLzJ9zWFcpd9Bpgeef9eDZFXKrNJVsrknweNepXQbS6MyfUNd6L14pL2r1rUXcA2hfFqGxsb17";
                
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        updateUI();
                        Toast.makeText(AndroidWallet.this, "Wallet generated successfully!", Toast.LENGTH_SHORT).show();
                    }
                });
            }
        });
    }
    
    private void sendTransaction() {
        String recipient = recipientEdit.getText().toString().trim();
        String amountStr = amountEdit.getText().toString().trim();
        
        if (recipient.isEmpty() || amountStr.isEmpty()) {
            Toast.makeText(this, "Please enter recipient and amount!", Toast.LENGTH_SHORT).show();
            return;
        }
        
        try {
            double amount = Double.parseDouble(amountStr);
            if (amount <= 0) {
                Toast.makeText(this, "Amount must be positive!", Toast.LENGTH_SHORT).show();
                return;
            }
            
            // Simulate transaction
            Toast.makeText(this, "Transaction sent successfully!", Toast.LENGTH_SHORT).show();
            recipientEdit.setText("");
            amountEdit.setText("");
            
        } catch (NumberFormatException e) {
            Toast.makeText(this, "Invalid amount!", Toast.LENGTH_SHORT).show();
        }
    }
    
    private void refreshBalance() {
        executor.execute(new Runnable() {
            @Override
            public void run() {
                // Simulate balance refresh
                balance = 0.0;
                
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        updateUI();
                        Toast.makeText(AndroidWallet.this, "Balance refreshed!", Toast.LENGTH_SHORT).show();
                    }
                });
            }
        });
    }
    
    private void updateUI() {
        if (walletAddress.isEmpty()) {
            addressText.setText("Address: Not generated");
        } else {
            addressText.setText("Address: " + walletAddress);
        }
        
        balanceText.setText(String.format("Balance: %.6f RSDT", balance));
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
        executor.shutdown();
    }
}
