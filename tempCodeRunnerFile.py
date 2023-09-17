def draw_text(surf, text, size, x, y,c=(0,0,0)):
    font = pygame.font.Font("tinypixel.otf", size)
    text_surface = font.render(text, True,c)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)