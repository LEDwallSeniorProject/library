from matrix_library import shapes as s, canvas as c
import time
import random
from evdev import InputDevice, categorize, ecodes

gamepad = InputDevice("/dev/input/event2")

canvas = c.Canvas()
circle = s.Circle(10, (64, 96), (0, 255, 0))
particles = []


def distance(x1, y1, x2, y2):
    """Compute the distance between two points."""
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


class Particle(s.Circle):
    def __init__(self, radius, center, color, velocity_x, velocity_y):
        super().__init__(radius, center, color)
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def hits(self, other: "Particle"):
        if self == other:
            return False
        return self.radius + other.radius >= distance(
            self.center[0], self.center[1], other.center[0], other.center[1]
        )

    def exit_prog():
        print("quit")
        canvas.delete()
        sys.exit()

    def bounce(self, other: "Particle"):
        if not self.hits(other):
            return

        m1 = self.radius**2
        m2 = other.radius**2
        m1_m2 = m1 + m2

        dx = self.center[0] - other.center[0]
        dy = self.center[1] - other.center[1]
        dist_sq = dx**2 + dy**2
        dvx = self.velocity_x - other.velocity_x
        dvy = self.velocity_y - other.velocity_y

        dot_product_2 = 2 * (dx * dvx + dy * dvy) / dist_sq
        dv1_scale = m2 / m1_m2 * dot_product_2
        dv2_scale = m1 / m1_m2 * dot_product_2

        self.velocity_x -= dv1_scale * dx
        self.velocity_y -= dv1_scale * dy
        other.velocity_x += dv2_scale * dx
        other.velocity_y += dv2_scale * dy

        dist = dist_sq**0.5
        dist_x_norm = dx / dist
        dist_y_norm = dy / dist
        intrusion_dist = (self.radius + other.radius - dist) / 2 + 1e-6

        self.translate(intrusion_dist * dist_x_norm, intrusion_dist * dist_y_norm)
        other.translate(-intrusion_dist * dist_x_norm, -intrusion_dist * dist_y_norm)


particle = Particle(8, (32, 96), (0, 255, 0), 3, 2)
particles.append(particle)
particle = Particle(10, (96, 96), (0, 0, 255), -3, 2)
particles.append(particle)
particle = Particle(12, (64, 96), (255, 0, 0), 2, -3)
particles.append(particle)
particle = Particle(6, (64, 75), (255, 255, 0), -2, -3)
particles.append(particle)

counter = 0
while counter <= 200:

    if gamepad.active_keys() == [24]:
        exit_prog()

    # Calculate the new position of the particles
    for particle in particles:
        if (
            particle.center[1] + particle.radius >= 128
            or particle.center[1] - particle.radius <= 0
        ):
            particle.velocity_y *= -1

        if (
            particle.center[0] + particle.radius >= 128
            or particle.center[0] - particle.radius <= 0
        ):
            particle.velocity_x *= -1

        particle.translate(particle.velocity_x, particle.velocity_y)

    for i in range(len(particles)):
        for j in range(i):
            if i != j:
                particles[i].bounce(particles[j])

    # Draw the particles
    canvas.clear()
    for particle in particles:
        canvas.add(particle)
    canvas.draw()

    counter += 1
