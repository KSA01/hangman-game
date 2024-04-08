# ui.py

import pygame
import time

pygame.init()
info = pygame.display.Info()

text_list = []

# Time in seconds before removing elements from the list
REMOVE_DELAY = 3

SCREEN_WIDTH = info.current_w - 120 #1200
SCREEN_HEIGHT = info.current_h - 150 #800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CREAM = (255, 253, 208)
GRAY = (70, 70, 70)
BUTTON_COLOR = (80, 80, 80)
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_TEXT_COLOR = (255, 255, 255)
INPUT_BOX_COLOR = (200, 200, 200)
INPUT_BOX_TEXT_COLOR = (0, 0, 0)

center_x = SCREEN_WIDTH // 2

def draw_button(screen, rect, text, font, hover):
    pygame.draw.rect(screen, BUTTON_HOVER_COLOR if hover else BUTTON_COLOR, rect)
    text_surface = font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def draw_input_box(screen, rect, text, font):
    pygame.draw.rect(screen, INPUT_BOX_COLOR, rect)
    text_surface = font.render(text, True, INPUT_BOX_TEXT_COLOR)
    text_rect = text_surface.get_rect(midleft=(rect.left + 10, rect.centery))
    screen.blit(text_surface, text_rect)

def draw_text_box(screen, rect, text, font):
    pygame.draw.rect(screen, WHITE, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def draw_chat(screen, text_list, font):
    screen_h = screen.get_height()
    screen_w = screen.get_width()
    rect_height = screen_h - (len(text_list) * 40)
    rect_width = screen_w / 4
    rect_x = (screen_w - 70) - rect_width
    rect_y = rect_height - 100
    rect_top_left = (rect_x, rect_y)
    rect2_top_left = (rect_x-20, rect_y-20)
    rect = pygame.Rect(rect_top_left, (rect_width, rect_height))
    rect2 = pygame.Rect(rect2_top_left, (rect_width+40, rect_height))
    pygame.draw.rect(screen, GRAY, rect2)
    y = rect.top

    for text in text_list:
        text_surface = font.render(text, True, CREAM)
        text_rect = text_surface.get_rect(midtop=(rect.centerx, y))
        screen.blit(text_surface, text_rect)
        y += text_rect.height + 20

def draw_list_text(screen, rect, list, font):
    rect = rect
    x = rect.left

    for text in list:
        text_surface = font.render(text, True, CREAM)
        text_rect = text_surface.get_rect(midtop=(x, rect.centery))
        screen.blit(text_surface, text_rect)
        x += text_rect.width + 10

def draw_multiline_text_box(screen, rect, header, data_list, font_h, font):
    pygame.draw.rect(screen, WHITE, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    # Render and draw the shadow of the header
    header_surface_shadow = font_h.render(header, True, BLACK)  # Choose a suitable gray color for the shadow
    header_rect_shadow = header_surface_shadow.get_rect(midtop=(rect.centerx + 2, rect.top - 48))  # Adjust position for the shadow
    screen.blit(header_surface_shadow, header_rect_shadow)

    # Render and draw the header
    header_surface = font_h.render(header, True, (255, 150, 255))
    header_rect = header_surface.get_rect(midtop=(rect.centerx, rect.top - 50))
    screen.blit(header_surface, header_rect)

    # Calculate the height of each line
    line_height = font.get_linesize()

    # Render and draw each line of data below the header
    y = header_rect.bottom + 10
    for data in data_list:
        data_surface = font.render(data, True, BLACK)
        data_rect = data_surface.get_rect(midtop=(rect.centerx, y + 20))
        screen.blit(data_surface, data_rect)
        y += line_height + 5  # Add a small gap between lines
