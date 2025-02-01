import webview
import threading
import time

# Function to load the main page after a delay
def load_main_page(window):
    time.sleep(5)  # Wait for 5 seconds (startup animation duration)
    window.load_url('frontend/web-pen.html')  # Load the main page

# Create the main function
def main():
    # Create a PyWebView window for the startup animation
    window = webview.create_window("Project Monolith", "anima.html", width=1200, height=710, resizable=False)
    
    # Start a separate thread to load the main page after a delay
    threading.Thread(target=load_main_page, args=(window,)).start()
    
    # Start the PyWebView application
    webview.start()

if __name__ == '__main__':
    main()
