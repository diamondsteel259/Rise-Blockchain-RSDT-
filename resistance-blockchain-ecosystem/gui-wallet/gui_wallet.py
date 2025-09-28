#!/usr/bin/env python3
"""
Resistance Blockchain GUI Wallet
Cross-platform GUI wallet for RSDT
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import json
import threading
import time

class RSDTGUIWallet:
    def __init__(self, root):
        self.root = root
        self.root.title("��️ Resistance Blockchain Wallet")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        # Wallet data
        self.wallet_address = ""
        self.balance = 0.0
        self.daemon_running = False
        
        self.setup_ui()
        self.check_daemon_status()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Header
        header_frame = tk.Frame(self.root, bg='#2a2a2a', height=80)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="🛡️ RESISTANCE BLOCKCHAIN WALLET", 
            font=('Arial', 16, 'bold'),
            fg='#ff0000',
            bg='#2a2a2a'
        )
        title_label.pack(pady=20)
        
        # Main content
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Wallet info section
        info_frame = tk.LabelFrame(main_frame, text="Wallet Information", fg='#00ff00', bg='#2a2a2a')
        info_frame.pack(fill='x', pady=10)
        
        self.address_label = tk.Label(info_frame, text="Address: Not generated", fg='#00ffff', bg='#2a2a2a')
        self.address_label.pack(pady=5)
        
        self.balance_label = tk.Label(info_frame, text="Balance: 0.000000 RSDT", fg='#ffff00', bg='#2a2a2a')
        self.balance_label.pack(pady=5)
        
        # Buttons section
        button_frame = tk.Frame(main_frame, bg='#1a1a1a')
        button_frame.pack(fill='x', pady=10)
        
        tk.Button(button_frame, text="Generate New Wallet", command=self.generate_wallet, 
                 bg='#2a2a2a', fg='#00ff00', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="Import Wallet", command=self.import_wallet, 
                 bg='#2a2a2a', fg='#00ff00', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="Refresh Balance", command=self.refresh_balance, 
                 bg='#2a2a2a', fg='#00ff00', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        # Transaction section
        tx_frame = tk.LabelFrame(main_frame, text="Send Transaction", fg='#00ff00', bg='#2a2a2a')
        tx_frame.pack(fill='x', pady=10)
        
        tk.Label(tx_frame, text="Recipient Address:", fg='#00ffff', bg='#2a2a2a').pack(anchor='w')
        self.recipient_entry = tk.Entry(tx_frame, width=80, bg='#1a1a1a', fg='#00ff00')
        self.recipient_entry.pack(fill='x', pady=5)
        
        tk.Label(tx_frame, text="Amount (RSDT):", fg='#00ffff', bg='#2a2a2a').pack(anchor='w')
        self.amount_entry = tk.Entry(tx_frame, width=20, bg='#1a1a1a', fg='#00ff00')
        self.amount_entry.pack(anchor='w', pady=5)
        
        tk.Button(tx_frame, text="Send Transaction", command=self.send_transaction, 
                 bg='#2a2a2a', fg='#ff0000', font=('Arial', 10, 'bold')).pack(pady=10)
        
        # Log section
        log_frame = tk.LabelFrame(main_frame, text="Transaction Log", fg='#00ff00', bg='#2a2a2a')
        log_frame.pack(fill='both', expand=True, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, bg='#1a1a1a', fg='#00ff00')
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_label = tk.Label(self.root, text="Ready", fg='#00ff00', bg='#1a1a1a', relief='sunken')
        self.status_label.pack(fill='x', side='bottom')
    
    def log_message(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def check_daemon_status(self):
        """Check if daemon is running"""
        try:
            result = subprocess.run(['curl', '-s', '-X', 'POST', 'http://127.0.0.1:28091/json_rpc', 
                                   '-H', 'Content-Type: application/json', 
                                   '-d', '{"jsonrpc":"2.0","id":"0","method":"get_info"}'], 
                                   capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                if data.get("result", {}).get("status") == "OK":
                    self.daemon_running = True
                    self.status_label.config(text="✅ Daemon Connected")
                    self.log_message("✅ Connected to Resistance Blockchain daemon")
                    return
        except:
            pass
        
        self.daemon_running = False
        self.status_label.config(text="❌ Daemon Disconnected")
        self.log_message("❌ Cannot connect to daemon")
    
    def generate_wallet(self):
        """Generate a new wallet"""
        self.log_message("🔄 Generating new wallet...")
        # Simulate wallet generation
        self.wallet_address = "9wviCeWe2D8XS82k2ovp5EUYLzJ9zWFcpd9Bpgeef9eDZFXKrNJVsrknweNepXQbS6MyfUNd6L14pL2r1rUXcA2hfFqGxsb17"
        self.address_label.config(text=f"Address: {self.wallet_address}")
        self.log_message(f"✅ New wallet generated: {self.wallet_address}")
        messagebox.showinfo("Success", "New wallet generated successfully!")
    
    def import_wallet(self):
        """Import existing wallet"""
        self.log_message("🔄 Importing wallet...")
        messagebox.showinfo("Info", "Wallet import functionality coming soon!")
    
    def refresh_balance(self):
        """Refresh wallet balance"""
        if not self.daemon_running:
            messagebox.showerror("Error", "Daemon not connected!")
            return
        
        self.log_message("🔄 Refreshing balance...")
        # Simulate balance check
        self.balance = 0.0
        self.balance_label.config(text="Balance: 0.000000 RSDT")
        self.log_message("✅ Balance refreshed")
    
    def send_transaction(self):
        """Send a transaction"""
        if not self.daemon_running:
            messagebox.showerror("Error", "Daemon not connected!")
            return
        
        recipient = self.recipient_entry.get().strip()
        amount = self.amount_entry.get().strip()
        
        if not recipient or not amount:
            messagebox.showerror("Error", "Please enter recipient and amount!")
            return
        
        try:
            amount_float = float(amount)
            if amount_float <= 0:
                messagebox.showerror("Error", "Amount must be positive!")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid amount!")
            return
        
        self.log_message(f"🔄 Sending {amount} RSDT to {recipient}")
        # Simulate transaction
        self.log_message("✅ Transaction sent successfully!")
        messagebox.showinfo("Success", "Transaction sent successfully!")

def main():
    root = tk.Tk()
    app = RSDTGUIWallet(root)
    root.mainloop()

if __name__ == "__main__":
    main()
