from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from pythreejs import *
import asyncio
import numpy as np
from IPython.display import display

# Create 3D scene
scene = Scene(children=[], background='white')
camera = PerspectiveCamera(position=[0, 0, 5], fov=50)
renderer = Renderer(camera=camera, scene=scene, controls=[OrbitControls(controlling=camera)], width=800, height=600)

# Create left and right eye spheres
left_eye = Mesh(geometry=SphereGeometry(radius=0.1), material=MeshStandardMaterial(color='blue'), position=[-0.2, 0, 0])
right_eye = Mesh(geometry=SphereGeometry(radius=0.1), material=MeshStandardMaterial(color='green'), position=[0.2, 0, 0])

# Add lights to the scene
light = PointLight(position=[10, 10, 10], intensity=1.5)
scene.children = [left_eye, right_eye, light]

def update_eye_position(left_gaze, right_gaze):
    # Normalize the gaze data and apply it to the eye position
    left_gaze = np.array(left_gaze) / np.linalg.norm(left_gaze) * 0.5
    right_gaze = np.array(right_gaze) / np.linalg.norm(right_gaze) * 0.5
    left_eye.position = [-0.2 + left_gaze[0], left_gaze[1], left_gaze[2]]
    right_eye.position = [0.2 + right_gaze[0], right_gaze[1], right_gaze[2]]
    renderer.render()

# OSC message handler
def osc_handler(addr, *args):
    if addr == "/eye/left":
        left_gaze = args[:3]
    elif addr == "/eye/right":
        right_gaze = args[:3]
    else:
        return
    update_eye_position(left_gaze, right_gaze)

# Set up OSC dispatcher and server
dispatcher = Dispatcher()
dispatcher.map("/eye/left", osc_handler)
dispatcher.map("/eye/right", osc_handler)

ip = "0.0.0.0"  # Listen on all interfaces
port = 9000     # Replace with the port your EyeTrackApp is streaming to

server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)

# Run the server
async def run_osc_server():
    print(f"Serving OSC on {ip}:{port}")
    server.serve_forever()

# Display the 3D visualization
display(renderer)

# Start the OSC server
asyncio.run(run_osc_server())
