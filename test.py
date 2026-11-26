import random
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("КПП 2026")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 32, bold=True)

ROLES = ["ИНЖЕНЕР", "ОХРАННИК", "УЧЕНЫЙ", "ГОСТЬ"]

def generate_visitor():
    return {
        "role": random.choice(ROLES),
        "year": random.choice([2025, 2026, 2027]),
        "access_level": random.randint(1, 5),
    }

def is_visitor_valid(visitor):
    # Черный список: гостей пропускать запрещено в любом случае
    if visitor["role"] == "ГОСТЬ":
        return False

    if visitor["year"] != 2026:
        return False
    if visitor["access_level"] < 2:
        return False

    return True

allow_button_rect = pygame.Rect(180, 420, 180, 60)
deny_button_rect = pygame.Rect(440, 420, 180, 60)

mistakes = 0
score = 0
game_over = False
current_visitor = generate_visitor()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Рестарт игры по нажатию R при проигрыше
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                mistakes = 0
                score = 0
                game_over = False
                current_visitor = generate_visitor()

        # Кнопки работают только пока game_over == False
        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if allow_button_rect.collidepoint(event.pos):
                if is_visitor_valid(current_visitor):
                    score += 1
                else:
                    mistakes += 1
                current_visitor = generate_visitor()

            elif deny_button_rect.collidepoint(event.pos):
                if not is_visitor_valid(current_visitor):
                    score += 1
                else:
                    mistakes += 1
                current_visitor = generate_visitor()

            if mistakes >= 3:
                game_over = True

    screen.fill((30, 30, 40))

    # Интерфейс статистики
    stats_text = font.render(f"Очки: {score}   Выговоры: {mistakes}/3", True, (255, 255, 255))
    screen.blit(stats_text, (30, 20))

    # Карточка посетителя
    pygame.draw.rect(screen, (50, 50, 70), (200, 100, 400, 250), border_radius=10)
    role_text = font.render(f"Должность: {current_visitor['role']}", True, (255, 255, 255))
    year_text = font.render(f"Год пропуска: {current_visitor['year']}", True, (255, 255, 255))
    access_text = font.render(f"Код доступа: {current_visitor['access_level']}", True, (255, 255, 255))

    screen.blit(role_text, (230, 140))
    screen.blit(year_text, (230, 200))
    screen.blit(access_text, (230, 260))

    # Кнопки
    pygame.draw.rect(screen, (40, 160, 80), allow_button_rect, border_radius=8)
    pygame.draw.rect(screen, (180, 50, 50), deny_button_rect, border_radius=8)

    allow_label = font.render("ПУСТИТЬ", True, (255, 255, 255))
    deny_label = font.render("ОТКАЗАТЬ", True, (255, 255, 255))
    screen.blit(allow_label, allow_label.get_rect(center=allow_button_rect.center))
    screen.blit(deny_label, deny_label.get_rect(center=deny_button_rect.center))

    # Экран увольнения
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(190)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        game_over_text = big_font.render(
            "ВЫ УВОЛЕНЫ! Нажмите R для новой смены", True, (255, 60, 60)
        )
        screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()