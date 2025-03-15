import webview
import subprocess
import datetime
import time
import os
from threading import Thread
from openai import OpenAI
import shutil
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class API:
    
    def __init__(self):
        self.selected_path = None
        self.json_file = "frontend/directory_paths.json"
        self.saved_paths = self.load_paths()
        self.key = os.urandom(32)
        

#==========================================WEB-VULN TOOLS CODE STARTS HERE==========================================> 
#NMAP PORT SCAN STARTS HERE    
    def portScan(self,ip,port,options):
        
        self.show_loader("Scanning Ports...")
        
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
        
        self.show_loader("Enumerating Subdomains...")
        
        cmd = ["amass enum -d", domain]

        if options:
            cmd += options
            
        
        timestamp = datetime.datetime.now().strftime("%d-%m-%y-%H.%M.%S")
        filename = f"dnsenum-{domain}-{timestamp}.txt"
        
        cmd_str = ' '.join(cmd) + f" > {filename}"
        print(cmd_str)
        
        scanprocess = subprocess.Popen(cmd_str, shell=True)
        scanprocess.wait()
        
        self.close_loader()
        
        if os.path.exists(filename):
            print(f"scan for {domain} is completed") 
            
            with open(filename, 'r') as file:
                scan_result = file.read()
                self.result("Amass", scan_result)
            self.move_file(filename)
        else:
            print("scan failed") 
#DNS ENUMERATION CODE ENDS HERE

#DNS RECON CODE STARTS HERE
    def dnsRecon(self,domain):
        
        self.show_loader("Performing DNS Recon...")
        
        cmd = ["whois", domain]
        
        timestamp = datetime.datetime.now().strftime("%d-%m-%y-%H.%M.%S")
        filename = f"dnsrecon-{domain}-{timestamp}.txt"
        
        cmd_str = ' '.join(cmd) + f" > {filename}"
        print(cmd_str)
        
        scanprocess = subprocess.Popen(cmd_str, shell=True)
        scanprocess.wait()
        
        self.close_loader()
        
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
            self.move_file(filename)
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
        
        self.show_loader("Scanning for Web Vulnerabilities...")
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
                
                self.close_loader()
            
            # Check if the file exists and is not empty
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                print(f"Scan for {domain} is completed. Results saved in {filename}.")
                
                # Optionally read the results for further processing
                with open(filename, 'r') as file:
                    scan_result = file.read()
                    self.result("nmap", scan_result)  # Adjust the second argument as needed
                self.move_file(filename)
            else:
                print("Scan failed or produced no output.")
        except Exception as e:
            print(f"An error occurred: {e}")
#WEB-VULN SCAN CODE ENDS HERE



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
            self.show_loader("Downloading Website...")
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
            self.close_loader()

       
        download_website(url)
        self.move_file(foldername)
     
    def wordlistgen(self,filename,word,minlength,maxlength):
        
        self.show_loader("Generating Wordlist...")
        
        minstrlen = str(minlength)
        maxstrlen = str(maxlength)
        filename = f"{filename}.txt"
        cmd = ["crunch",minstrlen,maxstrlen,word,"-o",filename]
        
        cmd_str = ' '.join(cmd)
        print(cmd_str)
        
        self.scanprocess = subprocess.Popen(cmd_str, shell=True)
        self.scanprocess.wait()
        
        self.close_loader()
        
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
        self.show_loader("Searching for Usernames...")
        
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
        self.show_loader("Checking Email...")
        
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
            self.save_to_json()  # Save only the new path
            self.create_a_file()
            return self.selected_path
        return None

    def get_saved_file(self):
        return self.saved_paths["path"]
    
    def AESencrypt(self):
        if not self.selected_path:
            print("No file selected!")
            return
        input_file = self.selected_path
        output_file = "encrypted_" + os.path.basename(input_file)
        
        iv = os.urandom(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        
        with open(input_file, "rb") as f:
            plaintext = f.read()
            
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        
        with open(output_file, "wb") as f:
            f.write(iv + ciphertext)
            
        print(f"File encrypted and saved as {output_file}")
    
    def AESdecrypt(self):
        if not self.selected_path:
            print("No file selected!")
            return
        
        encrypted_file = "encrypted_" + os.path.basename(self.selected_path)
        decrypted_file = "decrypted_" + os.path.basename(self.selected_path)
        
        with open(encrypted_file, "rb") as f:
            iv = f.read(16)
            ciphertext = f.read()
            
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        
        with open(decrypted_file, "wb") as f:
            f.write(plaintext)
            
        print(f"File decrypted and saved as {decrypted_file}")    
    
        
        


#==================================================ENCRYPTION TOOLS CODE ENDS HERE============================================>

#==================================================NO TOOLS CODE BELOW THIS==============================================>
# NO TOOLS CODE STARTS HERE
#LOADER CODE STARTS HERE
    def show_loader(self,msg):
        # Display a loader screen in a separate thread
        def loader():
            self.loader_window = webview.create_window(
                "Loading...",
                html=f"""
                <!DOCTYPE html>
                <html lang="en">

                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Loading...</title>
                    <style>
                        
                        body {{
                            font-family: Arial, sans-serif;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            margin: 0;
                            background-color: #1e1e1e;
                            color: #ffffff;
                        }}

                        
                        .loader {{
                            border: 10px solid #f3f3f3; /* Light gray border */
                            border-top: 10px solid #3498db; /* Blue border on top */
                            border-radius: 50%;
                            width: 100px;
                            height: 100px;
                            animation: spin 1s linear infinite; /* Smooth spinning */
                        }}

                        /* Spinning animation */
                        @keyframes spin {{
                            0% {{
                                transform: rotate(0deg);
                            }}
                            100% {{
                                transform: rotate(360deg);
                            }}
                        }}

                        /* Text below the loader */
                        .scan-text {{
                            margin-top: 20px;
                            font-size: 20px;
                            font-weight: bold;
                            text-align: center;
                        }}
                    </style>
                </head>

                <body>
                    <div class="loader"></div>
                    <p class="scan-text"></p>
                    <h1>{msg}</h1>
                </body>

                </html>

                """,
                width=400,
                height=300,
                resizable=False,
            )
            webview.start(debug=False)

        Thread(target=loader, daemon=True).start()

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
        with open("frontend/directory_paths.json", 'r') as path_file:
            path = json.load(path_file)
            print(path)
            
        shutil.move(source, path["path"])
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
        
    #     file_path = os.path.join(self.selected_path, "test.txt")
    #     try:
    #         with open(file_path, "w") as f:
    #             f.write("Hello World!")
    #         return f"File created at {file_path}"
    #     except Exception as e:
    #         return f"Error: {e}"
      
# SAVE FILE CODE ENDS HERE


if __name__ == '__main__':
   api = API()
   window = webview.create_window('Project MONOLITH', 'frontend/web-pen.html', js_api=api,
                              width=1200,
                              height=710,
                              resizable= False,
                              
 )
   webview.start(debug=False)
