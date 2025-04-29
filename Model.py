from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    Point3, Vec3, Geom, GeomNode, GeomVertexFormat, GeomVertexData, GeomTriangles,
    GeomVertexWriter, NodePath, AmbientLight, DirectionalLight, Material, TextureStage, Texture
)
from panda3d.core import LPoint3f
from direct.task import Task
from math import sin, cos, radians
import random


class MyGame(ShowBase):
    def __init__(self):
        super().__init__()

        self.disableMouse()  # We'll handle camera manually

        # Create the world
        self.ground = self.make_ground()
        self.ground.reparentTo(self.render)

        # Create player
        self.player = self.make_cube(color=(0.2, 0.8, 1.0, 1))
        self.player.reparentTo(self.render)
        self.player.setPos(0, 10, 1)

        # Add some trees
        for _ in range(15):
            self.make_tree(random.randint(-40, 40), random.randint(-40, 40))

        # Lighting
        self.add_lighting()

        # Key controls
        self.key_map = {"left": False, "right": False, "forward": False, "backward": False}
        self.accept("arrow_left", self.update_key, ["left", True])
        self.accept("arrow_left-up", self.update_key, ["left", False])
        self.accept("arrow_right", self.update_key, ["right", True])
        self.accept("arrow_right-up", self.update_key, ["right", False])
        self.accept("arrow_up", self.update_key, ["forward", True])
        self.accept("arrow_up-up", self.update_key, ["forward", False])
        self.accept("arrow_down", self.update_key, ["backward", True])
        self.accept("arrow_down-up", self.update_key, ["backward", False])

        # Movement task
        self.taskMgr.add(self.move, "moveTask")

        # Camera follow task
        self.taskMgr.add(self.follow_camera, "cameraTask")

    def update_key(self, key, value):
        self.key_map[key] = value

    def move(self, task):
        dt = globalClock.getDt()
        move_speed = 10

        if self.key_map["left"]:
            self.player.setH(self.player.getH() + 300 * dt)
        if self.key_map["right"]:
            self.player.setH(self.player.getH() - 300 * dt)
        if self.key_map["forward"]:
            self.player.setY(self.player, move_speed * dt)
        if self.key_map["backward"]:
            self.player.setY(self.player, -move_speed * dt)

        return Task.cont

    def follow_camera(self, task):
        # Smooth follow the player
        player_pos = self.player.getPos()
        cam_target = LPoint3f(player_pos.x, player_pos.y - 20, player_pos.z + 10)
        self.camera.setPos(cam_target)
        self.camera.lookAt(self.player)

        return Task.cont

    def make_cube(self, color=(1, 1, 1, 1)):
        format = GeomVertexFormat.getV3n3()
        vdata = GeomVertexData('cube', format, Geom.UHStatic)

        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')

        points = [
            (-1, -1, -1), (1, -1, -1),
            (1, 1, -1), (-1, 1, -1),
            (-1, -1, 1), (1, -1, 1),
            (1, 1, 1), (-1, 1, 1)
        ]

        faces = [
            (0, 1, 2, 3),  # Bottom
            (4, 5, 6, 7),  # Top
            (0, 1, 5, 4),  # Front
            (2, 3, 7, 6),  # Back
            (0, 3, 7, 4),  # Left
            (1, 2, 6, 5)   # Right
        ]

        for p in points:
            vertex.addData3(*p)
            normal.addData3(Vec3(p).normalized())

        triangles = GeomTriangles(Geom.UHStatic)
        for face in faces:
            triangles.addVertices(face[0], face[1], face[2])
            triangles.addVertices(face[2], face[3], face[0])

        cube = Geom(vdata)
        cube.addPrimitive(triangles)
        node = GeomNode('cube')
        node.addGeom(cube)
        cube_np = NodePath(node)

        material = Material()
        material.setDiffuse(color)
        cube_np.setMaterial(material)
        return cube_np

    def make_ground(self):
        cm = self.loader.loadModel("models/plane")  # Simple flat plane model
        cm.setScale(50)
        cm.setColor(0.3, 0.8, 0.3, 1)  # Greenish color
        cm.setPos(0, 0, 0)

        return cm

    def make_tree(self, x, y):
        # Tree trunk
        trunk = self.loader.loadModel("models/box")
        trunk.setScale(0.5, 0.5, 2)
        trunk.setColor(0.55, 0.27, 0.07, 1)
        trunk.setPos(x, y, 1)
        trunk.reparentTo(self.render)

        # Tree leaves
        leaves = self.loader.loadModel("models/sphere")
        leaves.setScale(2)
        leaves.setColor(0.0, 0.6, 0.0, 1)
        leaves.setPos(x, y, 4)
        leaves.reparentTo(self.render)

    def add_lighting(self):
        ambient = AmbientLight('ambient')
        ambient.setColor((0.5, 0.5, 0.5, 1))
        ambientNP = self.render.attachNewNode(ambient)
        self.render.setLight(ambientNP)

        directional = DirectionalLight('directional')
        directional.setColor((1, 1, 1, 1))
        directionalNP = self.render.attachNewNode(directional)
        directionalNP.setHpr(0, -60, 0)
        self.render.setLight(directionalNP)


game = MyGame()
game.run()
