# remote_touchpad

`remote_touchpad` is a python application that allows you to control your Mac's mouse cursor using touch events from a mobile device. It uses Flask for serving a web interface and Flask-SocketIO for real-time communication between the mobile device and the Mac. The project enables remote mouse control, making it useful for presentations, remote desktop scenarios, or accessibility purposes.

## Installation
### Clone the repository:
```bash

git clone https://github.com/Erickrus/remote_touchpad.git
cd remote_touchpad
```

### Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### Install dependencies:
Ensure you have Python 3.x installed.

Install required packages from requirements.txt:
```bash

pip install -r requirements.txt
```

### Grant permissions (macOS):
Go to System Settings > Privacy & Security > Accessibility and enable access for your terminal or IDE.

Enable screen recording permissions if prompted.

## Usage
### Start the server
Start the application:
```bash
python app.py
```

The HTTP server runs on http://localhost:8080 (serves the control page).

### Access the control page
On your mobile device, connect to the same network as your Mac.

Open a web browser and navigate to http://<your-mac-ip>:8080 (replace <your-mac-ip> with your Mac's IP address).

### Control the mouse
Use touch events on your mobile device:
- Touch and drag: Moves the mouse cursor.
- Tap: Performs a left click.
- Long press or right-click gesture: Performs a right click (if implemented in the client-side JavaScript).

The mouse movements are scaled based on your Mac's screen resolution and the mobile device's touchpad dimensions.

### Stop the server
Press Ctrl+C in the terminal to stop the server.

