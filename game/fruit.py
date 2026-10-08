import math


class Fruit:
    def __init__(
        self,
        x,
        y,
        vx,
        vy,
        gravity,
        radius=28,
        kind="fruit"
    ):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.gravity = gravity
        self.radius = radius
        self.kind = kind
        self.sliced = False

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

    def contains_point(self, x, y):
        return math.hypot(
            self.x - x,
            self.y - y
        ) <= self.radius

    def intersects_segment(self, start_pos, end_pos):
        """
        Check whether the line segment between two mouse
        positions intersects the circular fruit.
        """

        x1, y1 = start_pos
        x2, y2 = end_pos

        # Mouse movement vector
        dx = x2 - x1
        dy = y2 - y1

        # If there was no movement, check the current point
        if dx == 0 and dy == 0:
            return self.contains_point(x2, y2)

        # Vector from the first mouse position
        # to the center of the fruit
        fx = self.x - x1
        fy = self.y - y1

        # Project the fruit center onto the mouse movement
        t = (fx * dx + fy * dy) / (dx * dx + dy * dy)

        # Keep projection within the actual line segment
        t = max(0.0, min(1.0, t))

        # Closest point on the mouse path
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        # Distance from fruit center to mouse path
        distance = math.hypot(
            self.x - closest_x,
            self.y - closest_y
        )

        return distance <= self.radius

    def off_screen(self, height):
        return self.y - self.radius > height