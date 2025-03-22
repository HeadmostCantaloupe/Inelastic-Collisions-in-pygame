import pygame
import random
import math

pygame.init()

# Set up the screen
width = 800
height = 400
clock = pygame.time.Clock()
clack_sound = pygame.mixer.Sound("clack.wav")
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("INELASTIC COLLISIONS")

class Particle:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.position = pygame.math.Vector2(self.x, self.y)
        self.velocity = pygame.math.Vector2(random.randint(-5, 5), random.randint(-5, 5))
        self.top_speed = 2
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.accel = pygame.math.Vector2(0.01, 0.01)
        self.mass = mass
        self.r = math.sqrt(self.mass) * 10

    def show(self):
        pygame.draw.circle(screen, self.color, (self.position.x, self.position.y), self.r)

    def update(self):
        self.velocity = self.velocity + self.accel
        self.position = self.position + self.velocity
        self.accel = self.accel * 0
        if self.velocity.magnitude() > self.top_speed:
            self.velocity = self.velocity.normalize() * self.top_speed

    def checkEdges(self): 
        if self.position.x > width - self.r:
            self.position.x = width - self.r
            self.velocity.x *= -1

        if self.position.x < 0 + self.r:
            self.position.x = self.r
            self.velocity.x *= -1

        if self.position.y > height - self.r:
            self.position.y = height - self.r
            self.velocity.y *= -1

        if self.position.y < 0 + self.r:
            self.position.y = self.r
            self.velocity.y *= -1

    def collide(self, other):
        distance = self.position.distance_to(other.position)
        overlap = self.r + other.r - distance  # Calculate overlap

        if distance < self.r + other.r:  # Particles overlap
            # Separate particles to resolve overlap
            direction = (other.position - self.position).normalize()
            self.position -= direction * (overlap * (other.mass / (self.mass + other.mass)))
            other.position += direction * (overlap * (self.mass / (self.mass + other.mass)))

            # Calculate collision response
            mass_mult = self.mass * other.mass
            mass_sum = self.mass + other.mass
            vel_diff = pygame.math.Vector2(other.velocity.x - self.velocity.x, other.velocity.y - self.velocity.y)
            impact = other.position - self.position

            if impact.length() <= 0:
                return False
            normal = impact.normalize()

            cr = 0.5  # Coefficient of restitution
            j = ((mass_mult) / mass_sum) * (1 + cr) * vel_diff.dot(normal)

            self.velocity += (j / self.mass) * normal
            other.velocity -= (j / other.mass) * normal
            clack_sound.play()

particles = []
running = True

# Create particles only once, outside the game loop
for i in range(8):
    new_particle = Particle(random.randrange(0, width), random.randrange(0, height), random.randrange(1, 20))
    particles.append(new_particle)

# Set up text
font = pygame.font.Font(None, 30)
text_1 = font.render("Press space to clear all", True, (0, 0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            buttons = pygame.mouse.get_pressed()
            if buttons[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                new_particle = Particle(mouse_x, mouse_y, random.randrange(1, 20))
                particles.append(new_particle)

        # Delete all particles if the space bar is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                particles.clear()

    # Give the screen a background
    screen.fill((255, 255, 255))

    # Update the display and handle particles in the array
    for i in range(0, len(particles)):
        particles[i].show()
        particles[i].update()
        particles[i].checkEdges()

        for j in range(i + 1, len(particles)):
            particles[i].collide(particles[j])

    # Render the text
    screen.blit(text_1, (0, 0))
    
    # Update the display
    pygame.display.update()
    pygame.display.flip()

    clock.tick(60)  # Limit the frame rate to 60 FPS

pygame.quit()
