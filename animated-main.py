import webview
import subprocess
import datetime
import time
import os
import threading
from openai import OpenAI
import shutil
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import re

class API:
    
    def __init__(self):
        self.selected_path = None
        self.json_file = "frontend/directory_paths.json"
        self.saved_paths = self.load_paths()
        self.key = os.urandom(32)
        
        self.private_key_path = self.saved_paths.get("private_key_path", "private_key.pem")
        self.public_key_path = self.saved_paths.get("public_key_path", "public_key.pem")

#==========================================WEB-VULN TOOLS CODE STARTS HERE==========================================> 
#NMAP PORT SCAN STARTS HERE    
    def portScan(self,ip,port,options):
        
        self.show_loader()
        
        cmd = ["nmap", ip]
        if port:
            cmd += ["-p", port]
        if options:
            cmd += options
        
        timestamp = datetime.datetime.now().strftime("%d-%m-%y-%H.%M.%S")
        filename = f"portscan-{ip}-{timestamp}.txt"
        
        cmd_str = ' '.join(cmd) + f" > {filename}"
        print(cmd_str)
        
        self.scanprocess = subprocess.Popen(cmd_str, shell=True)
        self.scanprocess.wait()
        
        self.close_loader()
        
        if os.path.exists(filename):
            print(f"scan for {ip} is completed") 
            
            # self.save_file_ai(filename,"nmap")
            
            with open(filename, 'r') as file:
                scan_result = file.read()
                self.result("Nmap", scan_result)
            self.move_file(filename)
        else:
            print("scan failed")
#NMAP PORT SCAN ENDS HERE

#DNS ENUMERATION CODE STARTS HERE
    def dnsEnum(self,domain,options):
        cmd = ["amass enum -d", domain]

        if options:
            cmd += options
            
        
        timestamp = datetime.datetime.now().strftime("%d-%m-%y-%H.%M.%S")
        filename = f"dnsenum-{domain}-{timestamp}.txt"
        
        cmd_str = ' '.join(cmd) + f" > {filename}"
        print(cmd_str)
        
        scanprocess = subprocess.Popen(cmd_str, shell=True)
        scanprocess.wait()
        
        if os.path.exists(filename):
            print(f"scan for {domain} is completed") 
            
            with open(filename, 'r') as file:
                scan_result = file.read()
                self.result("Amass", scan_result)
        else:
            print("scan failed") 
#DNS ENUMERATION CODE ENDS HERE

#DNS RECON CODE STARTS HERE
    def dnsRecon(self,domain):
        cmd = ["whois", domain]
        
        timestamp = datetime.datetime.now().strftime("%d-%m-%y-%H.%M.%S")
        filename = f"dnsrecon-{domain}-{timestamp}.txt"
        
        cmd_str = ' '.join(cmd) + f" > {filename}"
        print(cmd_str)
        
        scanprocess = subprocess.Popen(cmd_str, shell=True)
        scanprocess.wait()
        
        if os.path.exists(filename):
            print(f"scan for {domain} is completed") 
            
            target_phrase = "DNSSEC"  # Change this to the phrase where deletion starts

            with open(filename, "r") as file:
                lines = file.readlines()

            # Find the index where the target phrase appears
            for i, line in enumerate(lines):
                if target_phrase in line:
                    lines = lines[:i]  # Keep only lines before the phrase
                    break  # Stop scanning once found

            with open(filename, "w") as file:
                file.writelines(lines)
            
            
            with open(filename, 'r') as file:
                scan_result = file.read()
                self.result("whois", scan_result)
        else:
            print("scan failed") 
#DNS RECON CODE ENDS HERE

#SAVE FILE CODE STARTS HERE
    def save_file_ai(self, filename,tool):
        with open(filename, 'r') as file:
            scan_result = file.read()
        
        client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="",
        )

        completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
        },
        extra_body={},
        model="qwen/qwen-vl-plus:free",
        messages=[
            {
            "role": "user",
            "content": scan_result + "read the output and summarize it and provide a report in a structured format"
            
            }
        ]
        )
        print("ai response",completion)
        ai_response = completion.choices[0].message.content

        with open(filename, "w") as file:
            file.write(ai_response)
            
        self.result(tool, ai_response)
# SAVE FILE CODE ENDS HERE

#WEB-VULN SCAN CODE STARTS HERE
    def webvuln(self, domain):
        # Construct the Nmap command
        cmd = ["nmap", "-sV", "--script=vuln", domain]
        
        # Generate timestamped filename
        timestamp = datetime.datetime.now().strftime("%d-%m-%y-%H.%M.%S")
        sanitized_domain = domain.replace("https://", "_").replace("http://", "_").replace("/", "_").replace(":", "_")
        filename = f"{sanitized_domain}-{timestamp}.txt"
        
        # Execute the command and write output to a file
        try:
            with open(filename, 'w') as file:
                self.scanprocess = subprocess.Popen(cmd, stdout=file, stderr=subprocess.PIPE)
                self.scanprocess.wait()
            
            # Check if the file exists and is not empty
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                print(f"Scan for {domain} is completed. Results saved in {filename}.")
                
                # Optionally read the results for further processing
                with open(filename, 'r') as file:
                    scan_result = file.read()
                    self.result("nmap", scan_result)  # Adjust the second argument as needed
            else:
                print("Scan failed or produced no output.")
        except Exception as e:
            print(f"An error occurred: {e}")
#WEB-VULN SCAN CODE ENDS HERE

    def dirEnum(self,url,options):
        self.show_loader("Enumerating Directories...")
        
        safe_url = re.sub(r"[^\w\d-]", "_", url)
        
        cmd = ["gobuster", "dir", "-u", url, "-w" , options]
        
        timestamp = datetime.datetime.now().strftime("%d-%m-%y-%H.%M.%S")
        filename = f"direnum-{safe_url}-{timestamp}.txt"
        
        cmd_str = ' '.join(cmd) + f" > {filename}"
        print(cmd_str)
        
        scanprocess = subprocess.Popen(cmd_str, shell=True)
        scanprocess.wait()
        
        self.close_loader()
        
        if os.path.exists(filename):
            print(f"scan for {url} is completed")
            
            with open(filename, 'r') as file:
                scan_result = file.read()
                self.result("Gobuster", scan_result)
            self.move_file(filename)
        else:
            print("scan failed")


#==================================================WEB-VULN TOOLS CODE ENDS HERE========================================>

#==================================================MISC TOOLS CODE STARTS HERE==========================================>
    def webDown(self, url, foldername):
        def download_asset(url, folder):
            """Download and save an asset (image, CSS, JS)"""
            try:
                response = requests.get(url, stream=True)
                filename = os.path.join(folder, os.path.basename(urlparse(url).path))
                
                if not filename.endswith(('.jpg', '.png', '.css', '.js', '.jpeg', '.gif', '.webp')):
                    return  # Skip non-essential files
                
                with open(filename, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Downloaded: {filename}")
            except Exception as e:
                print(f"Failed to download {url}: {e}")

        # Function to download a webpage
        def download_website(url, save_folder=foldername):
            """Download a website including assets using requests and BeautifulSoup"""
            os.makedirs(save_folder, exist_ok=True)

            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch page: {response.status_code}")
                return

            soup = BeautifulSoup(response.text, "html.parser")

            # Save HTML file
            html_path = os.path.join(save_folder, "index.html")
            with open(html_path, "w", encoding="utf-8") as file:
                file.write(soup.prettify())
            print(f"Saved HTML: {html_path}")

            # Download assets
            for tag in soup.find_all(["img", "link", "script"]):
                src = tag.get("src") or tag.get("href")
                if src:
                    asset_url = urljoin(url, src)
                    download_asset(asset_url, save_folder)

            print("Website download complete.")

       
        download_website(url)
        self.move_file(foldername)
     
    def wordlistgen(self,filename,word,minlength,maxlength):
        minstrlen = str(minlength)
        maxstrlen = str(maxlength)
        filename = f"{filename}.txt"
        cmd = ["crunch",minstrlen,maxstrlen,word,"-o",filename]
        
        cmd_str = ' '.join(cmd)
        print(cmd_str)
        
        self.scanprocess = subprocess.Popen(cmd_str, shell=True)
        self.scanprocess.wait()
        
        if os.path.exists(filename):
            print(f"wordlist generated")
            with open(filename, 'r') as file:
                scan_result = file.read()
                self.result("Crunch", scan_result)
            self.move_file(filename)
        else:
            print("scan failed")  
#==================================================MISC TOOLS CODE ENDS HERE============================================>

#==================================================OSINT TOOLS CODE STARTS HERE==========================================>
    def usernamesearch(self,username):
        self.show_loader()
        
        cmd = ["sherlock USERNAMES", username]
        
        # timestamp = datetime.datetime.now().strftime("%d-%m-%y-%H.%M.%S")
        # filename = f"username-{username}-{timestamp}.txt"
        
        cmd_str = ' '.join(cmd)
        print(cmd_str)
        
        self.scanprocess = subprocess.Popen(cmd_str, shell=True)
        self.scanprocess.wait()
        
        self.close_loader()
        filename = f"{username}.txt"
        if os.path.exists(filename):
            print(f"scan for {username} is completed")

            with open(filename, 'r') as file:
                scan_result = file.read()
                self.result("Sherlock", scan_result)
            self.move_file(filename)
        else:
            print("scan failed")
        
    def emailchecker(self,email):
        self.show_loader()
        
        cmd = ["holehe",email, "| grep +"]
        
        timestamp = datetime.datetime.now().strftime("%d-%m-%y-%H.%M.%S")
        filename = f"emailchecker-{email}-{timestamp}.txt"
        
        cmd_str = ' '.join(cmd) + f" > {filename}"
        print(cmd_str)
        
        self.scanprocess = subprocess.Popen(cmd_str, shell=True)
        self.scanprocess.wait()
        
        self.close_loader()
        
        if os.path.exists(filename):
            print(f"scan for {email} is completed") 
            
            with open(filename, 'r') as file:
                scan_result = file.read()
                self.result("EmailChecker", scan_result)
            self.move_file(filename)
        else:
            print("scan failed")


#==================================================OSINT TOOLS CODE ENDS HERE============================================>

#==================================================ENCRYPTION TOOLS CODE STARTS HERE============================================>

    def choose_file(self):
        directory = webview.windows[0].create_file_dialog(
            webview.OPEN_DIALOG
        )
        
        if directory:
            self.selected_path = directory[0]
            return self.selected_path
        return None

    def get_saved_file(self):
        return self.saved_paths["path"]
    
    def get_saved_file2(self):
        return self.saved_paths["path2"]
    
#AES ENCRYPTION CODE STARTS HERE

    def AESencrypt(self):
        if not self.selected_path:
            print("No file selected!")
            return
        input_file = self.selected_path
        output_file = "AES_encrypted_" + os.path.basename(input_file)
        
        iv = os.urandom(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        
        with open(input_file, "rb") as f:
            plaintext = f.read()
            
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        
        with open(output_file, "wb") as f:
            f.write(iv + ciphertext)
            
        print(f"File encrypted and saved as {output_file}")
        self.move_file(output_file)
    
    def AESdecrypt(self):
        if not self.selected_path:
            print("No file selected!")
            return

        encrypted_file = self.selected_path
        original_filename = os.path.basename(self.selected_path)
        
        if original_filename.startswith("encrypted_"):
            original_filename = original_filename[len("encrypted_"):]
            
        decrypted_file = "AES_decrypted_" + original_filename

        with open(encrypted_file, "rb") as f:
            encrypted_data = f.read()

        iv = encrypted_data[:16]  # First 16 bytes are IV
        ciphertext = encrypted_data[16:]  # Rest is ciphertext

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        try:
            plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        except ValueError:
            print("Decryption failed: Incorrect padding or corrupted data")
            return

        with open(decrypted_file, "wb") as f:
            f.write(plaintext)

        print(f"File decrypted and saved as {decrypted_file}") 
        self.move_file(decrypted_file)
    
#AES ENCRYPTION CODE ENDS HERE

#RSA ENCRYPTION CODE STARTS HERE

    def generate_key(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        with open(self.private_key_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        public_key = private_key.public_key()
        with open(self.public_key_path, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        self.move_file(self.private_key_path)
        self.move_file(self.public_key_path)
        print("RSA keys generated and saved")
    
    def RSAencrypt(self):
        
        if not self.selected_path:
            print("No file selected!")
            return
        
        input_file = self.selected_path
        output_file = "RSA_encrypted_" + os.path.basename(input_file)
            
            
        with open(self.public_key_path, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())

        aes_key = os.urandom(32)  # 256-bit key
        
        encrypted_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        iv = os.urandom(12)  # 96-bit IV
        cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv))
        encryptor = cipher.encryptor()

        with open(input_file, "rb") as f:
            plaintext = f.read()

        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        with open(output_file, "wb") as f:
            f.write(encrypted_key + iv + encryptor.tag + ciphertext)
        print(f"File encrypted and saved as {output_file}")

        self.move_file(output_file)

    def RSAdecrypt(self):
        
        if not self.selected_path:
            print("No file selected!")
            return
        
        encrypted_file = self.selected_path
        original_filename = os.path.basename(self.selected_path)
        
        if original_filename.startswith("RSA_encrypted_"):
            original_filename = original_filename[len("RSA_encrypted_"):]
            
        decrypted_file = "RSA_decrypted_" + original_filename
        
        with open(self.private_key_path, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)

        with open(encrypted_file, "rb") as f:
            encrypted_key = f.read(256)  # RSA 2048-bit key size
            iv = f.read(12)  # AES-GCM IV
            tag = f.read(16)  # AES-GCM tag
            ciphertext = f.read()

        aes_key = private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv, tag))
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        with open(decrypted_file, "wb") as f:
            f.write(plaintext)
        
        self.move_file(decrypted_file)
        print(f"File decrypted and saved as {decrypted_file}")

#RSA ENCRYPTION CODE ENDS HERE
        


#==================================================ENCRYPTION TOOLS CODE ENDS HERE============================================>




#==================================================NO TOOLS CODE BELOW THIS==============================================>
# NO TOOLS CODE STARTS HERE
#LOADER CODE STARTS HERE
    def show_loader(self):
        # Display a loader screen in a separate thread
        def loader():
            self.loader_window = webview.create_window(
                "Loading...",
                html="""
                <!DOCTYPE html>
                <html lang="en">

                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Loading...</title>
                    <style>
                        /* Overall page styles */
                        body {
                            font-family: Arial, sans-serif;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            margin: 0;
                            background-color: #1e1e1e;
                            color: #ffffff;
                        }

                        /* Loader animation */
                        .loader {
                            border: 10px solid #f3f3f3; /* Light gray border */
                            border-top: 10px solid #3498db; /* Blue border on top */
                            border-radius: 50%;
                            width: 100px;
                            height: 100px;
                            animation: spin 1s linear infinite; /* Smooth spinning */
                        }

                        /* Spinning animation */
                        @keyframes spin {
                            0% {
                                transform: rotate(0deg);
                            }
                            100% {
                                transform: rotate(360deg);
                            }
                        }

                        /* Text below the loader */
                        .scan-text {
                            margin-top: 20px;
                            font-size: 20px;
                            font-weight: bold;
                            text-align: center;
                        }
                    </style>
                </head>

                <body>
                    <div class="loader"></div>
                    <p class="scan-text">Scanning in progress...</p>
                </body>

                </html>

                """,
                width=400,
                height=300,
                resizable=False,
            )
            webview.start(debug=False)

        threading.Thread(target=loader, daemon=True).start()

    def close_loader(self):
        if self.loader_window:
            self.loader_window.destroy()
            self.loader_window = None
#LOADER CODE ENDS HERE

# RESULT WINDOW POPUP CODE STARTS HERE
    def result(self,tool,results):
        
        if tool == "Nmap":
            tool = "port scan"
        elif tool == "amass":
            tool = "subdomain enumeration"
        elif tool == "whois":
            tool = "DNS recon"
        elif tool == "nikto":
            tool = "web vuln scan"
        elif tool == "sherlock":
            tool = "username search"
        elif tool == "Crunch":
            tool = "wordlist generation"
        else:
            pass
        webview.create_window(tool, html=f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><pre>{tool}</pre></title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #2e2e2e;
            color: #ffffff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
        }}
        h1 {{
            color: #66ff66;
            font-size: 24px;
            margin-bottom: 20px;
        }}
        .container {{
            background-color: #333333;
            padding: 20px;
            border-radius: 8px;
            max-width: 90%;
            width: 700px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
            overflow-y: auto;
        }}
        pre {{
            background-color: #1e1e1e;
            color: #f1f1f1;
            padding: 15px;
            border-radius: 5px;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: "Courier New", monospace;
            max-height: 500px;
            overflow-y: auto;
            margin: 0;
        }}
        .footer {{
            margin-top: 20px;
            font-size: 12px;
            color: #999;
                }}
            </style>
        </head>
        <body>
            <h1>{tool}</h1>
            <div class="container">
                <pre>{results}</pre>
            </div>
            <div class="footer">
                <p>Scan completed at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </body>
        </html>
        """, height=700, width=1000)    
# RESULT WINDOW POPUP CODE ENDS HERE
    def terminate_scan(self):
        self.scanprocess.terminate()
        self.close_loader()
        print("terminated")

    def move_file(self,source):
        shutil.move(source, "outputfiles")
        print("file moved")

# SAVE FILE CODE STARTS HERE

    def load_paths(self):
        try:
            if os.path.exists(self.json_file):
                with open(self.json_file, 'r') as f:
                    return json.load(f)
            return {"path": None}  # Store only one path
        except json.JSONDecodeError:
            return {"path": None}

    def save_to_json(self):
        if self.selected_path:
            self.saved_paths["path"] = self.selected_path  # Overwrite old path
            self.saved_paths["private_key_path"] = f"{self.selected_path}/private_key.pem"
            self.saved_paths["public_key_path"] = f"{self.selected_path}/public_key.pem"
            
            with open(self.json_file, 'w') as f:
                json.dump(self.saved_paths, f, indent=4)
            
            return True
        return False

    def choose_directory(self):
        directory = webview.windows[0].create_file_dialog(
            webview.FOLDER_DIALOG
        )
        
        if directory:
            self.selected_path = directory[0]
            self.save_to_json()  # Save only the new path
            self.create_a_file()
            return self.selected_path
        return None

    def get_saved_paths(self):
        return self.saved_paths["path"]
    
    def create_a_file(self):
        if not self.selected_path:
            return "No directory selected!"
      
# SAVE FILE CODE ENDS HERE

def load_main_page(window):
    time.sleep(5)  # Wait for 5 seconds (startup animation duration)
    window.load_url('frontend/web-pen.html')  # Load the main page

# Create the main function
def main():
    # Create a PyWebView window for the startup animation
    window = webview.create_window("Project Monolith", "frontend/anima.html", width=1200, height=710, resizable=False,js_api=API())
    
    # Start a separate thread to load the main page after a delay
    threading.Thread(target=load_main_page, args=(window,)).start()
    
    # Start the PyWebView application
    webview.start()

if __name__ == '__main__':
    main()

    
# if __name__ == '__main__':
#    api = API()
#    window = webview.create_window('Project MONOLITH', 'frontend/web-pen.html', js_api=api,
#                               width=1200,
#                               height=710,
#                               resizable= False,
                              
#  )
#    webview.start(debug=False)
