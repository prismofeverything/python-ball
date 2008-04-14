from interface.gl import *


def rotate_glye(self, dt):
    

def make_torus(radius, inner_radius, slices, inner_slices):
    def mt():
        vertices = []
        normals = []

        u_step = 2 * pi / (slices - 1)
        v_step = 2 * pi / (inner_slices - 1)
        w_step = 2 * pi / 5
        u = 0.
        w = 0.
        for i in range(slices):
            cos_u = cos(u)
            sin_u = sin(u)
            v = 0.
            for j in range(inner_slices):
                cos_v = cos(v)
                sin_v = sin(v)

                d = (radius + inner_radius * cos_v)
                x = d * cos_u
                y = d * sin_u
                z = inner_radius * sin_v

                nx = cos_u * cos_v
                ny = sin_u * cos_v
                nz = sin_v

                vertices.extend([x, y, z])
                normals.extend([nx, ny, nz])

                v += v_step
            u += u_step
            w += w_step

        # Create ctypes arrays of the lists
        vertices = (GLfloat * len(vertices))(*vertices)
        normals = (GLfloat * len(normals))(*normals)

        # Create a list of triangle indices.
        indices = []
        for i in range(slices - 1):
            for j in range(inner_slices - 1):
                p = i * inner_slices + j
                indices.extend([p, p + inner_slices, p + inner_slices + 1])
                indices.extend([p, p + 1, p + inner_slices + 1])
        indices = (GLuint * len(indices))(*indices)

        # Compile a display list
        dlist = glGenLists(1)
        glNewList(dlist, GL_COMPILE)

        glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, vertices)
        glNormalPointer(GL_FLOAT, 0, normals)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, indices)
        glPopClientAttrib()

        glEndList()

        return dlist

    return mt

class TorusGlontrol(Glontrol):
    def __init__(self):
        Glontrol.__init__(self, 'torus')
        
        self.shift = [0.0 for i in range(9)]
        self.numpad = [65429, 65431, 65434, 65430, 65437, 65432, 65436, 65433, 65435]

    def on_update(self, dt):
        sign = 0.1
        if 65438 in self.w.keys:
            sign = -0.1

        for symbol in self.w.keys:
            if symbol in self.numpad:
                self.shift[self.numpad.index(symbol)] += sign
            self.w.activeGlye().shift(self.shift)
                
#             if symbol == key.NUM_ADD:
#                 self.w.activeGlye().translate(0, 0, 0.1)
#             if symbol == key.NUM_SUBTRACT:
#                 self.w.activeGlye().translate(0, 0, -0.1)
#             if symbol == key.UP:
#                 self.w.activeGlye().translate(0, 0.1, 0)
#             if symbol == key.DOWN:
#                 self.w.activeGlye().translate(0, -0.1, 0)
#             if symbol == key.LEFT:
#                 self.w.activeGlye().translate(-0.1, 0, 0)
#             if symbol == key.RIGHT:
#                 self.w.activeGlye().translate(0.1, 0, 0)

#             if symbol == key.NUM_UP:
#                 self.w.activeGlye().rotate(-3, 0, 0)
#             if symbol == key.NUM_DOWN:
#                 self.w.activeGlye().rotate(3, 0, 0)
#             if symbol == key.NUM_LEFT:
#                 self.w.activeGlye().rotate(0, -3, 0)
#             if symbol == key.NUM_RIGHT:
#                 self.w.activeGlye().rotate(0, 3, 0)
#             if symbol == key.NUM_DIVIDE:
#                 self.w.activeGlye().rotate(0, 0, -3)
#             if symbol == key.NUM_MULTIPLY:
#                 self.w.activeGlye().rotate(0, 0, 3)

    def on_key_press(self, symbol, mods):
        if symbol == key.SPACE:
            self.w.cycle()

def main():
    ww = Glindow()
    ww.activeGlye().tz = -8
    
    glye = Glye(rotate_glye)
    glye.tz = -4

    glights = [Glight(GL_LIGHT0, vec(.5, .5, 1, 0), vec(.5, .5, 1, 1), vec(1, 1, 1, 1)),
               Glight(GL_LIGHT1, vec(1, 0, .5, 0), vec(.5, .5, .5, 1), vec(1, 1, 1, 1))]

    glob = Glob(make_torus(1, 0.3, 50, 30), vec(0.4, 0.5, 0.7, 1), vec(1, 1, 1, 1), 50)
    glontrol = TorusGlontrol()

    ww.addGlye(glye)
    ww.glorld.glights = glights
    ww.glorld.globs.append(glob)

    ww.addGlontrol(glontrol)
    glontrol.attach(ww)

    ww.start()


if __name__=='__main__':
    main()



