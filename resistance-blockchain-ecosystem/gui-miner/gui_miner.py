#!/usr/bin/env python3
"""
Resistance Blockchain GUI Miner
Cross-platform GUI miner for RSDT
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import json
import threading
import time
import psutil

class RSDTGUIMiner:
    def __init__(self, root):
        self.root = root
        self.root.title("⛏️ Resistance Blockchain Miner")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a1a')
        
        # Mining data
        self.mining = False
        self.hashrate = 0.0
        self.blocks_found = 0
        self.mining_thread = None
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
            text="⛏️ RESISTANCE BLOCKCHAIN MINER", 
            font=('Arial', 16, 'bold'),
            fg='#ff0000',
            bg='#2a2a2a'
        )
        title_label.pack(pady=20)
        
        # Main content
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Mining stats section
        stats_frame = tk.LabelFrame(main_frame, text="Mining Statistics", fg='#00ff00', bg='#2a2a2a')
        stats_frame.pack(fill='x', pady=10)
        
        stats_grid = tk.Frame(stats_frame, bg='#2a2a2a')
        stats_grid.pack(fill='x', padx=10, pady=10)
        
        tk.Label(stats_grid, text="Hashrate:", fg='#00ffff', bg='#2a2a2a').grid(row=0, column=0, sticky='w')
        self.hashrate_label = tk.Label(stats_grid, text="0.00 H/s", fg='#ffff00', bg='#2a2a2a')
        self.hashrate_label.grid(row=0, column=1, sticky='w', padx=10)
        
        tk.Label(stats_grid, text="Blocks Found:", fg='#00ffff', bg='#2a2a2a').grid(row=0, column=2, sticky='w')
        self.blocks_label = tk.Label(stats_grid, text="0", fg='#ffff00', bg='#2a2a2a')
        self.blocks_label.grid(row=0, column=3, sticky='w', padx=10)
        
        tk.Label(stats_grid, text="CPU Usage:", fg='#00ffff', bg='#2a2a2a').grid(row=1, column=0, sticky='w')
        self.cpu_label = tk.Label(stats_grid, text="0%", fg='#ffff00', bg='#2a2a2a')
        self.cpu_label.grid(row=1, column=1, sticky='w', padx=10)
        
        tk.Label(stats_grid, text="Mining Status:", fg='#00ffff', bg='#2a2a2a').grid(row=1, column=2, sticky='w')
        self.status_label = tk.Label(stats_grid, text="Stopped", fg='#ff0000', bg='#2a2a2a')
        self.status_label.grid(row=1, column=3, sticky='w', padx=10)
        
        # Mining configuration
        config_frame = tk.LabelFrame(main_frame, text="Mining Configuration", fg='#00ff00', bg='#2a2a2a')
        config_frame.pack(fill='x', pady=10)
        
        config_grid = tk.Frame(config_frame, bg='#2a2a2a')
        config_grid.pack(fill='x', padx=10, pady=10)
        
        tk.Label(config_grid, text="Mining Address:", fg='#00ffff', bg='#2a2a2a').grid(row=0, column=0, sticky='w')
        self.address_entry = tk.Entry(config_grid, width=60, bg='#1a1a1a', fg='#00ff00')
        self.address_entry.grid(row=0, column=1, columnspan=2, sticky='ew', padx=5)
        self.address_entry.insert(0, "9wviCeWe2D8XS82k2ovp5EUYLzJ9zWFcpd9Bpgeef9eDZFXKrNJVsrknweNepXQbS6MyfUNd6L14pL2r1rUXcA2hfFqGxsb17")
        
        tk.Label(config_grid, text="Threads:", fg='#00ffff', bg='#2a2a2a').grid(row=1, column=0, sticky='w')
        self.threads_var = tk.StringVar(value=str(psutil.cpu_count()))
        self.threads_entry = tk.Entry(config_grid, width=10, bg='#1a1a1a', fg='#00ff00', textvariable=self.threads_var)
        self.threads_entry.grid(row=1, column=1, sticky='w', padx=5)
        
        # Mining buttons
        button_frame = tk.Frame(main_frame, bg='#1a1a1a')
        button_frame.pack(fill='x', pady=10)
        
        self.start_button = tk.Button(button_frame, text="Start Mining", command=self.start_mining, 
                                     bg='#2a2a2a', fg='#00ff00', font=('Arial', 12, 'bold'))
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = tk.Button(button_frame, text="Stop Mining", command=self.stop_mining, 
                                    bg='#2a2a2a', fg='#ff0000', font=('Arial', 12, 'bold'), state='disabled')
        self.stop_button.pack(side='left', padx=5)
        
        # Log section
        log_frame = tk.LabelFrame(main_frame, text="Mining Log", fg='#00ff00', bg='#2a2a2a')
        log_frame.pack(fill='both', expand=True, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, bg='#1a1a1a', fg='#00ff00')
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", fg='#00ff00', bg='#1a1a1a', relief='sunken')
        self.status_bar.pack(fill='x', side='bottom')
        
        # Start monitoring
        self.monitor_system()
    
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
                    self.status_bar.config(text="✅ Daemon Connected")
                    self.log_message("✅ Connected to Resistance Blockchain daemon")
                    return
        except:
            pass
        
        self.daemon_running = False
        self.status_bar.config(text="❌ Daemon Disconnected")
        self.log_message("❌ Cannot connect to daemon")
    
    def monitor_system(self):
        """Monitor system resources"""
        if self.mining:
            cpu_percent = psutil.cpu_percent()
            self.cpu_label.config(text=f"{cpu_percent}%")
        
        # Schedule next update
        self.root.after(1000, self.monitor_system)
    
    def simulate_mining(self):
        """Simulate mining process"""
        self.log_message("⛏️ Starting mining simulation...")
        
        while self.mining:
            # Simulate hashrate calculation
            self.hashrate = 1000 + (time.time() % 1000)
            self.hashrate_label.config(text=f"{self.hashrate:.2f} H/s")
            
            # Simulate finding a block (very rare)
            if int(time.time()) % 100 == 0:  # 1% chance every second
                self.blocks_found += 1
                self.blocks_label.config(text=str(self.blocks_found))
                self.log_message(f"🎉 Block found! Total: {self.blocks_found}")
            
            time.sleep(1)
        
        self.log_message("⛏️ Mining stopped")
    
    def start_mining(self):
        """Start mining"""
        if not self.daemon_running:
            messagebox.showerror("Error", "Daemon not connected!")
            return
        
        address = self.address_entry.get().strip()
        if not address:
            messagebox.showerror("Error", "Please enter mining address!")
            return
        
        try:
            threads = int(self.threads_var.get())
            if threads <= 0:
                messagebox.showerror("Error", "Threads must be positive!")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid thread count!")
            return
        
        self.mining = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.status_label.config(text="Mining", fg='#00ff00')
        
        self.mining_thread = threading.Thread(target=self.simulate_mining)
        self.mining_thread.daemon = True
        self.mining_thread.start()
        
        self.log_message(f"⛏️ Mining started with {threads} threads")
        self.log_message(f"📍 Mining to address: {address}")
    
    def stop_mining(self):
        """Stop mining"""
        self.mining = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_label.config(text="Stopped", fg='#ff0000')
        
        self.log_message("⛏️ Mining stopped by user")

def main():
    root = tk.Tk()
    app = RSDTGUIMiner(root)
    root.mainloop()

if __name__ == "__main__":
    main()
