import webview

# Create the PyWebView window
window = webview.create_window('Project FRANXX', 'web-pen.html',
                               width=1200,
                               height=700,
                               resizable= False
                            )

# Start a thread to load the main page after 5 seconds


# Start the PyWebView event loop
webview.start()
