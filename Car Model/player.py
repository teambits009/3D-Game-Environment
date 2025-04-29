from ursina import *
import random

app = Ursina()

window.borderless = False
Sky()

# Load real 3D models
player = Entity(model='models/car.obj', texture='white_cube', scale=0.5, collider='box', position=(0, 0.5, -40))

ground = Entity(model='plane', texture='white_cube', texture_scale=(50,50), scale=(100,1,100), collider='box')

# Racing track
track = []
for i in range(10):
    track.append(Entity(model='cube', color=color.dark_gray, scale=(10, 0.1, 10), position=(0, 0.05, i*10 - 50), collider='box'))

# Walls
walls = []
for i in range(-5, 6):
    walls.append(Entity(model='cube', color=color.gray, scale=(1, 5, 10), position=(5, 2.5, i*10), collider='box'))
    walls.append(Entity(model='cube', color=color.gray, scale=(1, 5, 10), position=(-5, 2.5, i*10), collider='box'))

# Boost pads
boost_pads = []
for z in [-20, 0, 20, 40]:
    boost_pads.append(Entity(model='cube', color=color.azure, scale=(3, 0.1, 3), position=(0, 0.05, z), collider='box'))

# Trees using real 3D models
trees = []
for _ in range(20):
    trees.append(Entity(model='models/tree.obj', texture='white_cube', scale=1, position=(random.choice([-8, 8]), 2.5, random.randint(-50, 50))))

# AI planes (also real 3D models)
ai_planes = []
for _ in range(3):
    ai_plane = Entity(model='models/ai_plane.obj', texture='white_cube', scale=0.5, position=(random.uniform(-3,3), 0.5, random.randint(-30,30)), collider='box')
    ai_planes.append(ai_plane)

# Camera setup
camera.parent = player
camera.position = (0, 5, -15)
camera.rotation_x = 20

# Movement variables
speed = 5
turn_speed = 80
boosting = False

def update():
    global boosting

    # Player controls
    move_speed = speed * (2 if boosting else 1)
    if held_keys['w']:
        player.position += player.forward * time.dt * move_speed
    if held_keys['s']:
        player.position -= player.forward * time.dt * move_speed
    if held_keys['a']:
        player.rotation_y += turn_speed * time.dt
    if held_keys['d']:
        player.rotation_y -= turn_speed * time.dt

    # Boost pad collision
    boosting = any(player.intersects(pad).hit for pad in boost_pads)

    # Move AI planes forward automatically
    for ai in ai_planes:
        ai.position += ai.forward * time.dt * (speed * 0.8)
        if ai.z > 60:
            ai.z = -50
            ai.x = random.uniform(-3, 3)

app.run()
