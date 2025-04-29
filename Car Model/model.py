from ursina import *

app = Ursina()

window.borderless = False  # So you can resize the window easily

# Load a car model (for now, just a simple cube)
player = Entity(model='cube', color=color.red, scale=(1, 0.5, 2), collider='box')

# Make a simple ground (the racetrack will be built on this later)
ground = Entity(model='plane', texture='white_cube', texture_scale=(50, 50), scale=(100, 1, 100), collider='box')

camera.position = (0, 20, -30)
camera.rotation_x = 30

speed = 5
turn_speed = 60

def update():
    global speed
    if held_keys['w']:
        player.position += player.forward * time.dt * speed
    if held_keys['s']:
        player.position -= player.forward * time.dt * speed
    if held_keys['a']:
        player.rotation_y += turn_speed * time.dt
    if held_keys['d']:
        player.rotation_y -= turn_speed * time.dt

app.run()

# Create walls around the track
walls = []
for z in range(-50, 51, 10):
    walls.append(Entity(model='cube', color=color.gray, scale=(1, 5, 10), position=(5, 2.5, z), collider='box'))
    walls.append(Entity(model='cube', color=color.gray, scale=(1, 5, 10), position=(-5, 2.5, z), collider='box'))

# Add a speed boost pad
boost_pad = Entity(model='cube', color=color.azure, scale=(3, 0.1, 3), position=(0, 0.05, 20), collider='box')

# Boost logic
boosting = False

def update():
    global boosting
    if held_keys['w']:
        player.position += player.forward * time.dt * (speed * (2 if boosting else 1))
    if held_keys['s']:
        player.position -= player.forward * time.dt * speed
    if held_keys['a']:
        player.rotation_y += turn_speed * time.dt
    if held_keys['d']:
        player.rotation_y -= turn_speed * time.dt

    # Boost if player touches the boost_pad
    if player.intersects(boost_pad).hit:
        boosting = True
    else:
        boosting = False


Sky()
