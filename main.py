import webview
import subprocess
import datetime
import time
import os


class API:
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
        #subprocess.run(['gnome-terminal', '--', 'bash', '-c', cmd_str]) 
        scanprocess = subprocess.Popen(cmd_str, shell=True)

        scanprocess.wait()
        
        if os.path.exists(filename):
            print(f"scan for {ip} is completed") 
            
            with open(filename, 'r') as file:
                scan_result = file.read()
    # output of scan result code starts here
                self.result("Nmap", scan_result)

    # output result for the scan html code ends here
        else:
            print("scan failed")
         
    
    def result(self,tool,results):
        webview.create_window("Port Scan Result", html=f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Port Scan Result</title>
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
    <h1>Port Scan Result</h1>
    <div class="container">
        <pre>{results}</pre>
    </div>
    <div class="footer">
        <p>Scan completed at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
</body>
</html>
""", height=700, width=1000)
         
   
      
      
         

if __name__ == '__main__':
   api = API()
   window = webview.create_window('Project MONOLITH', 'frontend/web-pen.html', js_api=api,
                              width=1200,
                              height=710,
                              resizable= False
                            )
   webview.start(debug=False)
