from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Configure template and static folders
app.template_folder = os.path.abspath('.')
app.static_folder = os.path.abspath('.')

@app.route('/')
def home():
    """Serve the main index page"""
    return send_from_directory('root', 'index.html')

@app.route('/index.html')
def index():
    """Serve the index page (alternative route)"""
    return send_from_directory('root', 'index.html')

@app.route('/about/team.html')
def team():
    """Serve the team page"""
    return send_from_directory('about', 'team.html')

@app.route('/about/mission.html')
def mission():
    """Serve the mission page"""
    return send_from_directory('about', 'mission.html')

@app.route('/misc/other.html')
def other():
    """Serve the other page"""
    return send_from_directory('root/misc', 'other.html')

# Generic route to serve any HTML file in the root directory
@app.route('/<path:filename>')
def serve_file(filename):
    """Serve files from root directory"""
    if filename.endswith('.html'):
        return send_from_directory('root', filename)
    else:
        # For other file types (CSS, JS, images, etc.)
        return send_from_directory('.', filename)

if __name__ == '__main__':
    print("Starting Flask web server...")
    print("Available routes:")
    print("- http://127.0.0.1:5000/ (Home page)")
    print("- http://127.0.0.1:5000/about/team.html (Team page)")
    print("- http://127.0.0.1:5000/about/mission.html (Mission page)")
    print("- http://127.0.0.1:5000/misc/other.html (Other page)")
    print("\nPress Ctrl+C to stop the server")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
