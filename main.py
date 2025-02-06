import webview
import subprocess
import datetime
import time
import os


class API:

    
# NMAP PORT SCAN STARTS HERE    

    def portScan(self,ip,port,options):
        cmd = ["nmap", ip]
        if port:
            cmd += ["-p", port]
        if options:
            cmd += options
        
        timestamp = datetime.datetime.now().strftime("%d-%m-%y-%H.%M")
        filename = f"{ip}-{timestamp}.txt"
        
        cmd_str = ' '.join(cmd) + f" > {filename}"
        print(cmd_str)
        
        scanprocess = subprocess.Popen(cmd_str, shell=True)
        scanprocess.wait()
        
        if os.path.exists(filename):
            print(f"scan for {ip} is completed") 
            
            with open(filename, 'r') as file:
                scan_result = file.read()
                self.result("Nmap", scan_result)
        else:
            print("scan failed")
         
# NMAP PORT SCAN ENDS HERE

# DNS ENUMERATION CODE STARTS HERE
    def dnsEnum(self,domain,options):
        cmd = ["amass enum -d", domain]

        if options:
            cmd += options
            
        
        timestamp = datetime.datetime.now().strftime("%d-%m-%y-%H.%M")
        filename = f"{domain}-{timestamp}.txt"
        
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
# DNS ENUMERATION CODE ENDS HERE


# RESULT WINDOW POPUP CODE STARTS HERE
    
    def result(self,tool,results):
        
        if tool == "Nmap":
            tool = "port scan"
        elif tool == "amass":
            tool = "subdomain enumeration"
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
      
      
         

if __name__ == '__main__':
   api = API()
   window = webview.create_window('Project MONOLITH', 'frontend/web-pen.html', js_api=api,
                              width=1200,
                              height=710,
                              resizable= False,
 )
   webview.start(debug=False)
