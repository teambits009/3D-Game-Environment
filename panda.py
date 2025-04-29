from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import PointLight, AmbientLight, VBase4, NodePath, LPoint3
from math import sin, cos
import sys

class IllusionGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Disable default mouse camera control to implement custom controls
        self.disableMouse()
        
        # Set up camera
        self.camera.setPos(0, -20, 5)
        self.camera.lookAt(0, 0, 0)
        
        # Instructions text
        self.instructions = OnscreenText(
            text="WASD: Move | Mouse: Look | ESC: Quit",
            pos=(0, -0.9),
            fg=(1, 1, 1, 1),
            align=0,
            scale=0.05
        )
        
        # Create the main cube
        self.cube = self.loader.loadModel("models/box")
        self.cube.reparentTo(self.render)
        self.cube.setScale(2, 2, 2)
        self.cube.setPos(0, 0, 1)
        
        # Create a reflective floor
        self.floor = self.loader.loadModel("models/plane")
        self.floor.reparentTo(self.render)
        self.floor.setScale(20, 20, 1)
        self.floor.setPos(0, 0, 0)
        self.floor.setColor(0.2, 0.2, 0.8, 1)  # Slightly reflective blue tint
        
        # Set up lighting
        self.setup_lights()
        
        # Camera movement variables
        self.move_speed = 10
        self.mouse_sensitivity = 0.2
        self.prev_x = 0
        self.prev_y = 0
        
        # Enable mouse and keyboard input
        self.accept("escape", sys.exit)
        self.accept("w", self.set_key, ["forward", True])
        self.accept("w-up", self.set_key, ["forward", False])
        self.accept("s", self.set_key, ["backward", True])
        self.accept("s-up", self.set_key, ["backward", False])
        self.accept("a", self.set_key, ["left", True])
        self.accept("a-up", self.set_key, ["left", False])
        self.accept("d", self.set_key, ["right", True])
        self.accept("d-up", self.set_key, ["right", False])
        
        # Key map for movement
        self.key_map = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False
        }
        
        # Start tasks
        self.taskMgr.add(self.update, "update")
        self.taskMgr.add(self.animate_cube, "animate_cube")
        
    def setup_lights(self):
        # Point light for dynamic shadows and highlights
        plight = PointLight("plight")
        plight.setColor(VBase4(1, 1, 1, 1))
        self.plight_node = self.render.attachNewNode(plight)
        self.plight_node.setPos(5, -5, 5)
        self.render.setLight(self.plight_node)
        
        # Ambient light for soft illumination
        alight = AmbientLight("alight")
        alight.setColor(VBase4(0.3, 0.3, 0.3, 1))
        self.alight_node = self.render.attachNewNode(alight)
        self.render.setLight(self.alight_node)
        
    def set_key(self, key, value):
        self.key_map[key] = value
        
    def update(self, task):
        dt = globalClock.getDt()
        
        # Handle keyboard movement
        if self.key_map["forward"]:
            self.camera.setY(self.camera, self.move_speed * dt)
        if self.key_map["backward"]:
            self.camera.setY(self.camera, -self.move_speed * dt)
        if self.key_map["left"]:
            self.camera.setX(self.camera, -self.move_speed * dt)
        if self.key_map["right"]:
            self.camera.setX(self.camera, self.move_speed * dt)
        
        # Handle mouse look
        if self.mouseWatcherNode.hasMouse():
            x, y = self.mouseWatcherNode.getMouseX(), self.mouseWatcherNode.getMouseY()
            delta_x = (x - self.prev_x) * 100 * self.mouse_sensitivity
            delta_y = (y - self.prev_y) * 100 * self.mouse_sensitivity
            h, p = self.camera.getH() - delta_x, self.camera.getP() - delta_y
            self.camera.setHpr(h, max(min(p, 90), -90), 0)
            self.prev_x, self.prev_y = x, y
            
        # Update light position based on camera
        cam_pos = self.camera.getPos()
        self.plight_node.setPos(cam_pos + LPoint3(5 * sin(task.time), -5, 5))
        
        return Task.cont
    
    def animate_cube(self, task):
        # Create illusion with rotation and scaling
        t = task.time
        self.cube.setHpr(t * 30, t * 20, t * 10)  # Rotate cube
        scale = 2 + 0.5 * sin(t)  # Pulsating scale
        self.cube.setScale(scale, scale, scale)
        
        # Adjust cube color for visual effect
        self.cube.setColor(0.5 + 0.5 * sin(t), 0.5 + 0.5 * cos(t), 0.8, 1)
        
        return Task.cont

# Run the game
game = IllusionGame()
game.run()