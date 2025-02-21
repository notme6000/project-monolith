import webview
import subprocess
import datetime
import time
import os
from threading import Thread
from openai import OpenAI
import threading
import shutil


class API:

    
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
        filename = f"{domain}-{timestamp}.txt"
        
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
            
            # self.save_file_ai(filename,"whois")
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
        print("terminated")
    
    def move_file(self,source):
        shutil.move(source, "outputfiles")
        print("file moved")
        

# SAVE FILE CODE STARTS HERE
   
      
# SAVE FILE CODE ENDS HERE

def load_main_page(window):
    time.sleep(5)  # Wait for 5 seconds (startup animation duration)
    window.load_url('frontend/web-pen.html')  # Load the main page

# Create the main function
def main():
    api=API()
    # Create a PyWebView window for the startup animation
    window = webview.create_window("Project Monolith", "frontend/anima.html", width=1200, height=710, resizable=False,js_api=api)
    
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
