import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((0, 0), DOUBLEBUF | OPENGL | FULLSCREEN)
clock = pygame.time.Clock()

# Constants
FPS = 60
WIDTH, HEIGHT = pygame.display.get_surface().get_size()
SCALE = (0.5, 0.5, 0.5)
ROTATION_ANGLE = 0.3

# OpenGL settings
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (WIDTH / HEIGHT), 0.1, 100.0)
glMatrixMode(GL_MODELVIEW)
glTranslatef(0.0, 0.0, -50)  # Move back a bit to fit the simulation

def hsb_to_rgb(hue, saturation, brightness):
    """Convert HSB (Hue, Saturation, Brightness) to RGB."""
    if saturation == 0:
        return (brightness, brightness, brightness)
    
    hue = hue % 360
    c = brightness * saturation
    x = c * (1 - abs((hue / 60) % 2 - 1))
    m = brightness - c

    if 0 <= hue < 60:
        r, g, b = c, x, 0
    elif 60 <= hue < 120:
        r, g, b = x, c, 0
    elif 120 <= hue < 180:
        r, g, b = 0, c, x
    elif 180 <= hue < 240:
        r, g, b = 0, x, c
    elif 240 <= hue < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    return (r + m, g + m, b + m)

class LorenzAttractor:
    def __init__(self, sigma=10, rho=28, beta=8/3, dt=0.01):
        self.x = 0.01
        self.y = 0
        self.z = 0
        self.sigma = sigma
        self.rho = rho
        self.beta = beta
        self.dt = dt
        self.points = []
        self.colors = []

    def update(self):
        dx = self.sigma * (self.y - self.x) * self.dt
        dy = (self.x * (self.rho - self.z) - self.y) * self.dt
        dz = (self.x * self.y - self.beta * self.z) * self.dt
        self.x += dx
        self.y += dy
        self.z += dz

        self.points.append((self.x, self.y, self.z))

        # Create a color with HSB where hue changes over time
        hue = len(self.points) * 0.1 % 360
        saturation = 1.0
        brightness = 1.0
        color = hsb_to_rgb(hue, saturation, brightness)
        self.colors.append(color)

    def draw(self):
        if not self.points:
            return

        # Calculate the centroid of the points
        x_coords, y_coords, z_coords = zip(*self.points)
        centroid = (
            sum(x_coords) / len(x_coords),
            sum(y_coords) / len(y_coords),
            sum(z_coords) / len(z_coords)
        )

        # Draw continuous lines with colors
        glBegin(GL_LINE_STRIP)
        for i, point in enumerate(self.points):
            glColor3fv(self.colors[i])
            # Translate points to center around the centroid
            glVertex3f(point[0] - centroid[0], point[1] - centroid[1], point[2] - centroid[2])
        glEnd()

def main():
    attractor = LorenzAttractor()
    running = True
    angle_y = 0

    while True:
        [exit() for _ in pygame.event.get() if _.type == pygame.KEYDOWN and _.key == pygame.K_ESCAPE]


        attractor.update()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Rotate the model around the y-plane
        glPushMatrix()
        glScalef(*SCALE)  # Scale down the attractor to fit the screen
        glRotatef(angle_y, 0, 1, 0)
        attractor.draw()
        glPopMatrix()

        # Update the angle for rotation
        angle_y += ROTATION_ANGLE

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
