import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
SIDEBAR_WIDTH = 200
MAIN_WIDTH = WIDTH - SIDEBAR_WIDTH

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)


class SortingVisualizer:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sorting Algorithm Visualizer")

        self.array_size = 50
        self.min_val = 10
        self.max_val = HEIGHT - 50
        self.array = self.generate_array()

        self.sorting = False
        self.paused = False
        self.algorithm = "bubble_sort"
        self.delay = 50  # milliseconds
        self.comparing_indices = []
        self.swapping_indices = []
        self.current_step = 0

        # Button dimensions
        self.button_width = 180
        self.button_height = 30

        # Buttons
        self.buttons = {
            "bubble_sort": pygame.Rect(WIDTH - 190, 20, self.button_width, self.button_height),
            "insertion_sort": pygame.Rect(WIDTH - 190, 60, self.button_width, self.button_height),
            "selection_sort": pygame.Rect(WIDTH - 190, 100, self.button_width, self.button_height),
            "bogo_sort": pygame.Rect(WIDTH - 190, 140, self.button_width, self.button_height),
            "randomize": pygame.Rect(WIDTH - 190, 200, self.button_width, self.button_height),
            "start": pygame.Rect(WIDTH - 190, 240, self.button_width, self.button_height),
            "pause": pygame.Rect(WIDTH - 190, 280, self.button_width, self.button_height),
            "reset": pygame.Rect(WIDTH - 190, 320, self.button_width, self.button_height),
            "exit": pygame.Rect(WIDTH - 190, 360, self.button_width, self.button_height),
            "speed_up": pygame.Rect(WIDTH - 190, 400, 85, self.button_height),
            "speed_down": pygame.Rect(WIDTH - 95, 400, 85, self.button_height),
            "size_up": pygame.Rect(WIDTH - 190, 440, 85, self.button_height),
            "size_down": pygame.Rect(WIDTH - 95, 440, 85, self.button_height)
        }

    def generate_array(self):
        return [random.randint(self.min_val, self.max_val) for _ in range(self.array_size)]

    def draw(self):
        self.screen.fill(BLACK)

        # Draw array bars
        bar_width = (MAIN_WIDTH - 20) // self.array_size
        for i, val in enumerate(self.array):
            color = WHITE
            if i in self.comparing_indices:
                color = RED
            if i in self.swapping_indices:
                color = GREEN

            x = i * bar_width + 10
            pygame.draw.rect(self.screen, color, (x, HEIGHT - val, bar_width - 1, val))

        # Draw sidebar
        pygame.draw.rect(self.screen, GRAY, (MAIN_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT))

        # Draw buttons
        font = pygame.font.SysFont(None, 24)
        for name, rect in self.buttons.items():
            pygame.draw.rect(self.screen, WHITE, rect)
            text = font.render(name.replace("_", " ").title(), True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

        # Draw current speed and size
        speed_text = font.render(f"Delay: {self.delay}ms", True, WHITE)
        size_text = font.render(f"Elements: {self.array_size}", True, WHITE)
        self.screen.blit(speed_text, (WIDTH - 190, 480))
        self.screen.blit(size_text, (WIDTH - 190, 500))

        pygame.display.flip()

    def bubble_sort(self):
        n = len(self.array)
        if self.current_step < n:
            for j in range(0, n - self.current_step - 1):
                if not self.sorting:
                    return
                while self.paused:
                    self.draw()
                    pygame.time.delay(30)

                self.comparing_indices = [j, j + 1]
                self.draw()
                pygame.time.delay(self.delay)

                if self.array[j] > self.array[j + 1]:
                    self.swapping_indices = [j, j + 1]
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                    self.draw()
                    pygame.time.delay(self.delay)

                self.comparing_indices = []
                self.swapping_indices = []
            self.current_step += 1

    def insertion_sort(self):
        if self.current_step < len(self.array):
            key = self.array[self.current_step]
            j = self.current_step - 1
            while j >= 0 and self.array[j] > key:
                if not self.sorting:
                    return
                while self.paused:
                    self.draw()
                    pygame.time.delay(30)

                self.comparing_indices = [j, j + 1]
                self.draw()
                pygame.time.delay(self.delay)

                self.swapping_indices = [j, j + 1]
                self.array[j + 1] = self.array[j]
                j -= 1
                self.draw()
                pygame.time.delay(self.delay)

                self.comparing_indices = []
                self.swapping_indices = []
            self.array[j + 1] = key
            self.current_step += 1

    def selection_sort(self):
        if self.current_step < len(self.array):
            min_idx = self.current_step
            for j in range(self.current_step + 1, len(self.array)):
                if not self.sorting:
                    return
                while self.paused:
                    self.draw()
                    pygame.time.delay(30)

                self.comparing_indices = [min_idx, j]
                self.draw()
                pygame.time.delay(self.delay)

                if self.array[j] < self.array[min_idx]:
                    min_idx = j

                self.comparing_indices = []

            self.swapping_indices = [self.current_step, min_idx]
            self.array[self.current_step], self.array[min_idx] = self.array[min_idx], self.array[self.current_step]
            self.draw()
            pygame.time.delay(self.delay)
            self.swapping_indices = []
            self.current_step += 1

    def bogo_sort(self):
        def is_sorted():
            return all(self.array[i] <= self.array[i + 1] for i in range(len(self.array) - 1))

        if not is_sorted():
            if not self.sorting:
                return
            while self.paused:
                self.draw()
                pygame.time.delay(30)

            self.comparing_indices = list(range(len(self.array)))
            self.draw()
            pygame.time.delay(self.delay)

            random.shuffle(self.array)
            self.swapping_indices = list(range(len(self.array)))
            self.draw()
            pygame.time.delay(self.delay)

            self.comparing_indices = []
            self.swapping_indices = []

    def run(self):
        sorting_algorithms = {
            "bubble_sort": self.bubble_sort,
            "insertion_sort": self.insertion_sort,
            "selection_sort": self.selection_sort,
            "bogo_sort": self.bogo_sort
        }

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    for name, rect in self.buttons.items():
                        if rect.collidepoint(mouse_pos):
                            if name in sorting_algorithms:
                                self.algorithm = name
                                self.current_step = 0  # Reset step for new sort
                                self.sorting = True  # Start sorting
                            elif name == "randomize":
                                self.array = self.generate_array()
                                self.current_step = 0  # Reset step for new array
                            elif name == "start":
                                self.sorting = True
                                self.current_step = 0  # Reset step for new sort
                            elif name == "pause":
                                self.paused = not self.paused
                            elif name == "reset":
                                self.array = self.generate_array()
                                self.sorting = False
                                self.paused = False
                                self.current_step = 0  # Reset step for new array
                            elif name == "exit":
                                pygame.quit()
                                sys.exit()
                            elif name == "speed_up":
                                self.delay = max(1, self.delay - 10)
                            elif name == "speed_down":
                                self.delay = min(200, self.delay + 10)
                            elif name == "size_up":
                                if self.array_size < 100:  # Limit to 100 elements
                                    self.array_size += 5
                                    self.array = self.generate_array()
                                    self.current_step = 0  # Reset step for new array
                            elif name == "size_down":
                                if self.array_size > 5:  # Limit to 5 elements
                                    self.array_size -= 5
                                    self.array = self.generate_array()
                                    self.current_step = 0  # Reset step for new array

            if self.sorting:
                sorting_algorithms[self.algorithm]()

            self.draw()
            pygame.time.delay(30)


if __name__ == "__main__":
    visualizer = SortingVisualizer()
    visualizer.run()