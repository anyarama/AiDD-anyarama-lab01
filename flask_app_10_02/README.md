# Flask Web App

This is a simple Flask web application that serves HTML pages.

## Setup Instructions

1. **Install Flask** (if not already installed):
   ```bash
   pip install flask
   ```
   
   Or install from requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python app.py
   ```

3. **Access the website**:
   Open your web browser and navigate to:
   - Home page: http://127.0.0.1:5000/
   - Team page: http://127.0.0.1:5000/about/team.html
   - Mission page: http://127.0.0.1:5000/about/mission.html
   - Other page: http://127.0.0.1:5000/misc/other.html

## File Structure

```
flask_app_10_02/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── root/              # HTML files for the root directory
│   ├── index.html     # Home page
│   └── misc/
│       └── other.html # Other page
└── about/             # HTML files for the about section
    ├── team.html      # Team page
    └── mission.html   # Mission page
```

## Features

- Serves static HTML files
- Maintains the original directory structure for navigation
- Debug mode enabled for development
- All relative links in HTML files work correctly

## Stopping the Server

Press `Ctrl+C` in the terminal to stop the Flask development server.
