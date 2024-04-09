
import pygame

class Timer:
    def __init__(self, TIMER_DUR):
        self.TIMER_DURATION = TIMER_DUR # the start time
        self.duration = self.TIMER_DURATION # count as time counts down

    def start_timer(self):
        self.start_time = pygame.time.get_ticks()

    def update(self):
        # Get the elapsed time since the timer started
        elapsed_time = pygame.time.get_ticks() - self.start_time
        # Calculate the remaining time
        self.duration = max(self.TIMER_DURATION - elapsed_time // 1000, 0)

    def has_expired(self):
        return self.duration <= 0

    def reset(self):
        self.start_time = pygame.time.get_ticks()
        self.duration = self.TIMER_DURATION