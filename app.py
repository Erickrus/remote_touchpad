from flask import Flask, send_file
from flask_socketio import SocketIO
import threading
import pyautogui
pyautogui.FAILSAFE = False
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

W_mac, H_mac = pyautogui.size()
last_touch_x = None
last_touch_y = None
W_div = None
H_div = None

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('message')
def handle_message(data):
    global last_touch_x, last_touch_y, W_div, H_div
    if data['type'] == 'touchstart':
        # Initialize last touch position on touch start
        last_touch_x = data['x']
        last_touch_y = data['y']
        W_div = data['W_div']
        H_div = data['H_div']
    elif data['type'] == 'touchmove':
        current_touch_x = data['x']
        current_touch_y = data['y']
        if last_touch_x is not None and last_touch_y is not None:
            # Calculate relative touch delta
            delta_touch_x = current_touch_x - last_touch_x
            delta_touch_y = current_touch_y - last_touch_y
            # Scale deltas based on screen and touchpad resolution
            scale_x = W_mac / W_div if W_div else 1
            scale_y = H_mac / H_div if H_div else 1
            delta_mouse_x = int(delta_touch_x * 0.37)
            delta_mouse_y = int(delta_touch_y * 0.37)
            # delta_mouse_x = delta_touch_x #* scale_x
            # delta_mouse_y = delta_touch_y #* scale_y
            # Move mouse relatively
            pyautogui.moveRel(delta_mouse_x, delta_mouse_y)
        # Inside the touchmove handler
        elif data['type'] == 'touchmove':
            current_touch_x = data['x']
            current_touch_y = data['y']
            if last_touch_x is not None and last_touch_y is not None:
                delta_touch_x = current_touch_x - last_touch_x
                delta_touch_y = current_touch_y - last_touch_y
                # Adjust sensitivity (e.g., 0.5 for less movement)
                sensitivity = 0.5
                scale_x = (W_mac / W_div) * sensitivity if W_div else sensitivity
                scale_y = (H_mac / H_div) * sensitivity if H_div else sensitivity
                delta_mouse_x = delta_touch_x * scale_x
                delta_mouse_y = delta_touch_y * scale_y
                pyautogui.moveRel(delta_mouse_x, delta_mouse_y)
            last_touch_x = current_touch_x
            last_touch_y = current_touch_y

        # Update last touch position
        last_touch_x = current_touch_x
        last_touch_y = current_touch_y
    elif data['type'] == 'touchend':
        # Reset last touch position on touch end
        last_touch_x = None
        last_touch_y = None
    elif data['type'] == 'click':
        pyautogui.click()
    elif data['type'] == 'rightclick':
        pyautogui.rightClick()

@app.route('/')
def serve_control_page():
    return send_file('index.html')

def start_socketio_server():
    socketio.run(app, host='0.0.0.0', port=5000)

def start_http_server():
    app.run(host='0.0.0.0', port=8080, threaded=True)

if __name__ == '__main__':
    # https://www.idownloadblog.com/2022/12/01/how-to-share-mac-wi-fi-internet/#Share-a-Macs-Wi-Fi-to-iPhone-or-iPad-over-a-USB-cable-or-Bluetooth
    socketio_thread = threading.Thread(target=start_socketio_server)
    socketio_thread.daemon = True
    socketio_thread.start()

    start_http_server()