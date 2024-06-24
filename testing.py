import http.server
import socketserver
import os
import webbrowser
import threading

# Set the port for the web server
PORT = 8000

# Change the current working directory to the directory containing your HTML file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create a request handler
Handler = http.server.SimpleHTTPRequestHandler

# Function to open the web browser
def open_browser():
    webbrowser.open_new_tab(f'http://localhost:{PORT}/animation.html')

# Create a socket server with the specified handler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    print(f"Opening http://localhost:{PORT}/animation.html in your web browser")
    
    # Start the browser in a new thread
    threading.Timer(1.25, open_browser).start()
    
    # Start the server
    httpd.serve_forever()