'''
Useful articles for this project:
   * https://www.maa.org/press/periodicals/loci/joma/the-sir-model-for-spread-of-disease-the-differential-equation-model

'''
import numpy as np
import pygame

# Initial Parameters
alpha = 0.002   # Infection Rate
beta = 0.1      # Recovery Rate
gamma = 0.005   # Birth / death rate

population = 1000
inital_infected = 10
at_risk = population - inital_infected
initial_recovered = 0

# Define the differential Equations for the SIR model
def atRiskDt(atRisk, infected, alpha=alpha, pop=population):
    return (-alpha * atRisk * infected) / pop

def recoveredDt(infected, beta=beta):
    return beta * infected

def infectedDt(atRisk, infected, alpha=alpha, pop=population):
    return ((alpha * atRisk * infected) / pop) - (beta * infected)


# Simulation Parameters
tMax = 500
h = 0.01 # Step size
steps = np.arange(0, tMax, h)

susceptible = np.zeros(len(steps))
infected = np.zeros(len(steps))
recovered = np.zeros(len(steps))

susceptible[0] = at_risk
infected[0] = inital_infected
recovered[0] = initial_recovered


# Creating an Entity class
class Entity(pygame.sprite.Sprite):
    def __init__(self, surface, pos, colorCode):
        super().__init__()
        self.color = (0, 255, 0)
        self.image = pygame.Surface((5, 5))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=pos)
        self.size = 5
        self.surface = surface
        self.pos = pos
        self.xPos = pos[0]
        self.yPos = pos[1]
        self.colorCode = colorCode
        

    def draw(self):
        if self.colorCode == 'infected':
            self.image.fill((255, 0, 0))
        elif self.colorCode == 'atRisk':
            self.image.fill((0, 255, 0))
        elif self.colorCode == 'recovered':
            self.image.fill((0, 0, 255))

    def update(self):
        global h
        if self.colorCode == 'infected':
            if np.random.rand() < beta * h:
                self.colorCode = 'recovered'
                self.draw()
            
            if np.random.rand() < gamma * h:
                self.kill()
                infected[-1] -= 1 # might need fixed

        if self.colorCode == 'atRisk':
            if np.random.rand() < alpha * h:
                self.colorCode = 'infected'
                susceptible[-1] -= 1
                infected[-1] += 1
                self.draw()

def main():
    # Window management
    window_width = 800
    window_height = 600
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Epidemic Predator-Prey Model')

    # Frame count
    FPS = 60

    # Extra space to display a potential GUI
    BUFFER_SPACE = 250

    # Creating the sprite groups
    totalPop = pygame.sprite.Group()
    atRiskPop = pygame.sprite.Group()
    infectedPop = pygame.sprite.Group()
    recoveredPop = pygame.sprite.Group()

    # Color codes for the Entity object (makes them more standardized to set them as variables)
    status_infected = 'infected'
    status_atRisk = 'atRisk'
    status_recovered = 'recovered'

    # Instantiating the sprite groups with the initial entity values
    for i in range(population):
        if i < inital_infected:
            entity = Entity(screen, (np.random.randint(window_width - BUFFER_SPACE), np.random.randint(window_height)), status_infected)
            infectedPop.add(entity)
            infected[0] += 1

        else:
            entity = Entity(screen, (np.random.randint(window_width - BUFFER_SPACE), np.random.randint(window_height)), status_atRisk)
            atRiskPop.add(entity)
            totalPop.add(entity)

    # Setting up the clock
    clock = pygame.time.Clock()
    done = False
    s = len(steps)

    # Main Loop
    while not done:
        for step in range(s):
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

            # Updating the population
            totalPop.update()

            screen.fill((255, 255, 255)) 
            totalPop.draw(screen)     
            pygame.display.update()

            # Update the differential equations using Euler's method
            susceptible[step] = susceptible[step-1] + atRiskDt(susceptible[step-1], infected[step-1]) * h
            infected[step] = infected[step-1] + infectedDt(susceptible[step-1], infected[step-1]) * h
            recovered[step] = recovered[step-1] + recoveredDt(infected[step-1]) * h

            # Updating the amount of recovered entities in the population
            for j in range(int(recovered[step] - recovered[step-1])):
                entity = Entity(screen, (np.random.randint(window_width - BUFFER_SPACE), np.random.randint(window_height)), status_recovered)
                recoveredPop.add(entity)
                totalPop.add(entity)

            # Update the number of infected individuals
            infected[-1] = len(infectedPop)

            # clock.tick(FPS)
            entity.update()

        print("Done!!!!!")
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                        
        # Making sure that the screen doesn't keep updating
        s = 0
        

if __name__ == '__main__':
    # Initiating pygame
    pygame.init()
    main()  