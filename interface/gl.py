from math import pi, sin, cos, tan

from pyglet.gl import *
from pyglet import clock
from pyglet import window
from pyglet import font
from pyglet.window import key

from utility.matrix import *

def vec(*args):
    return (GLfloat * len(args))(*args)

def export(matrix):
    return vec(*matrix.matrix)

def hold_glye(self, dt):
    pass

class Glight:
    def __init__(self, glid, pos, spec, diff):
        self.glid = glid
        self.pos = pos
        self.spec = spec
        self.diff = diff

        glEnable(self.glid)
        glLightfv(self.glid, GL_POSITION, self.pos)
        glLightfv(self.glid, GL_SPECULAR, self.spec)
        glLightfv(self.glid, GL_DIFFUSE, self.diff)

    def draw(self, dt):
        pass


class Glye: 
    def __init__(self, transform):
        self.transform = transform
        self.matrix = identity(4)

    def transform(self, matrix):
        self.matrix *= matrix

    def draw(self, dt):
        self.transform(self, dt)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glMultMatrixf(export(self.matrix))
#         glRotatef(self.rx, 1, 0, 0)
#         glRotatef(self.ry, 0, 1, 0)
#         glRotatef(self.rz, 0, 0, 1)
#         glTranslatef(self.tx, self.ty, self.tz)

#     def translate(self, x, y, z):
#         self.tx += x
#         self.ty += y
#         self.tz += z

#     def rotate(self, x, y, z):
#         self.rx += x
#         self.ry += y
#         self.rz += z
#         self.rx %= 360
#         self.ry %= 360
#         self.rz %= 360
    

class Glob:
    def __init__(self, vertices, amb_diff, spec, shiny):
        self.dlist = vertices()

        self.amb_diff = amb_diff
        self.spec = spec
        self.shiny = shiny

    def setVertices(self):
        pass

    def draw(self, dt):
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.amb_diff)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, self.spec)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, self.shiny)

        glCallList(self.dlist)

class Glorld:
    def __init__(self):
        self.globs = []
        self.glights = []
        
    def draw(self, dt):
        for glob in self.globs:
            glob.draw(dt)

class Glontrol:
    def __init__(self, name, glindow=None, parent=None):
        self.name = name

        self.w = glindow
        if self.w != None:
            self.w.push_handlers(self)
            self.w.glontrol = self

        self.parent = parent
        self.children = []

    def attach(self, glindow):
        self.w = glindow
        self.w.push_handlers(self)
        self.w.glontrol = self

    def detach(self, glindow):
        self.w = None
        self.w.pop_handlers()
        self.w.glontrol = parent

    def addChild(self, child):
        child.parent = self
        self.children.append(child)

    def on_update(self, dt):
        pass

class StaticGlontrol(Glontrol):
    def __init__(self):
        Glontrol.__init__(self, 'static')

    def attach(self, glindow):
        self.w = glindow
        self.w.glontrol = self

    def detach(self, glindow):
        self.w = None
        self.w.pop_handlers()

class WindowGlontrol(Glontrol):
    def __init__(self):
        Glontrol.__init__(self, 'window')

    def on_key_press(self, symbol, mods):
        self.w.mods = mods
        if not symbol in self.w.keys:
            self.w.keys.append(symbol)

    def on_key_release(self, symbol, mods):
        self.w.mods = mods
        if symbol in self.w.keys:
            self.w.keys.remove(symbol)

class GlontTree:
    def __init__(self):
        self.families = {}

    def glont(self, family, size):
        if not self.families.has_key(family):
            self.families[family] = {}
        if not self.families[family].has_key(size):
            self.families[family][size] = font.load(family, size)

        return self.families[family][size]

class Timer:
    def __init__(self, rate, func):
        self.rate = rate
        self.func = func
        self.clock = 0.0
        self.before = time.time()

    def __call__(self, elapsed):
        self.forward(elapsed)

    def forward(self, elapsed):
        self.clock += elapsed
        if self.clock > self.rate:
            self.clock = 0.0
            self.func()

class Gleceptor:
    def __init__(self):
        pass

    def signal(channel, signal):
        pass


class GlobalGlontrol(Glontrol):
    def __init__(self):
        Glontrol.__init__(self, 'interface')

        self.receptors = {}
        self.mouseDown = False

        for key in ['close',
                    'update',
                    'timer',
                    'key_press',
                    'key_release',
                    'mouse_press',
                    'mouse_release',
                    'mouse_motion',
                    'mouse_drag']:
            self.receptors[key] = []

        def update(up, dt): self.send('timer', dt)
        self.addReceptor('update', update)

    def send(self, channel, *signal):
        for receptor in self.receptors[key]:
            receptor.signal(channel, signal)

    def on_close(self): self.send('close')
    def on_update(self, dt): self.send('update', dt)
    def on_key_press(self, sym, mods): self.send('key_press', sym, mods)
    def on_key_release(self, sym, mods): self.send('key_release', sym, mods)
    def on_mouse_press(self, x, y, b, mods): self.send('mouse_press', x, y, but, mods)
    def on_mouse_release(self, dt): self.send('mouse_release', x, y, but, mods)
    def on_mouse_motion(self, dt): self.send('mouse_motion', x, y, dx, dy)
    def on_mouse_drag(self, dt): self.send('mouse_drag', x, y, dx, dy, but, mods)

    def addReceptor(self, channel, receptor):
        self.receptors[channel].append(receptor)

    def removeReceptor(self, channel, receptor):
        self.receptors[channel].remove(receptor)

    def addTimer(self, rate, func):
        timer = Timer(rate, func)
        self.receptors['timer'].append(timer)

        return timer


class Glindow(window.Window):
    def __init__(self):
        try:
            config = Config(sample_buffers=1, samples=4, 
                            depth_size=16, double_buffer=True,)
            window.Window.__init__(self, resizable=True, config=config)
        except window.NoSuchConfigException:
            window.Window.__init__(self, resizable=True, config=config)

        self.keys = []
        self.mods = 0

        glClearColor(1, 1, 1, 1)
        glColor3f(1, 0, 0)
        glEnable(GL_DEPTH_TEST)

        glEnable(GL_LIGHTING)

        self.glyes = [Glye(hold_glye)]
        self.activeglye = 0

        self.glorld = Glorld()
        self.root_glontrol = WindowGlontrol()
        self.root_glontrol.attach(self)

    def addGlye(self, glye):
        self.glyes.append(glye)
        self.activeglye = len(self.glyes) - 1

    def addGlontrol(self, glontrol):
        self.root_glontrol.addChild(glontrol)

    def activeGlye(self):
        return self.glyes[self.activeglye]

    def view(self, index):
        self.activeglye = index % len(self.glyes)

    def cycle(self):
        self.activeglye = (self.activeglye + 1) % len(self.glyes)

    def draw(self, dt):
        self.activeGlye().draw(dt)
        self.glorld.draw(dt)

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60., width / float(height), .1, 1000.)
        glMatrixMode(GL_MODELVIEW)

    def start(self):
        while not self.has_exit:
            self.dt = clock.tick()
            self.dispatch_events()
            self.glontrol.on_update(self.dt)

            self.draw(self.dt)
            self.flip()




