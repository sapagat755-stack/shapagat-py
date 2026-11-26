import random
import sys
import pygame

# Инициализация Pygame
pygame.init()

# Константы экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Цвета (RGB)
WHITE = (255, 255, 255)
BLACK = (20, 20, 30)
BLUE = (0, 150, 255)
RED = (255, 75, 75)
GREEN = (75, 255, 125)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Кибер-Курьер: Зарядка ядра")
clock = pygame.time.Clock()

# Шрифты
font_large = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 24)


class Player(pygame.sprite.Sprite):

  def __init__(self):
    super().__init__()
    self.image = pygame.Surface((40, 40))
    self.image.fill(BLUE)
    self.rect = self.image.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    )
    self.speed = 5

  def update(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
      self.rect.x -= self.speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
      self.rect.x += self.speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
      self.rect.y -= self.speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
      self.rect.y += self.speed

    # Удержание игрока в пределах окна
    self.rect.clamp_ip(screen.get_rect())


class Capsule(pygame.sprite.Sprite):

  def __init__(self):
    super().__init__()
    self.image = pygame.Surface((20, 20))
    self.image.fill(GREEN)
    self.rect = self.image.get_rect(
        x=random.randint(50, SCREEN_WIDTH - 70),
        y=random.randint(50, SCREEN_HEIGHT - 70),
    )


class Virus(pygame.sprite.Sprite):

  def __init__(self):
    super().__init__()
    self.image = pygame.Surface((30, 30))
    self.image.fill(RED)
    self.rect = self.image.get_rect(
        x=random.choice([50, SCREEN_WIDTH - 80]),
        y=random.randint(50, SCREEN_HEIGHT - 80),
    )
    self.dx = random.choice([-3, 3])
    self.dy = random.choice([-3, 3])

  def update(self):
    self.rect.x += self.dx
    self.rect.y += self.dy

    # Отскок от стен
    if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
      self.dx *= -1
    if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
      self.dy *= -1


def main():
  player = Player()
  all_sprites = pygame.sprite.Group(player)
  capsules = pygame.sprite.Group()
  viruses = pygame.sprite.Group()

  # Создание первой капсулы
  for _ in range(1):
    cap = Capsule()
    capsules.add(cap)
    all_sprites.add(cap)

  # Создание вирусов-препятствий
  for _ in range(3):
    virus = Virus()
    viruses.add(virus)
    all_sprites.add(virus)

  score = 0
  target_score = 10
  lives = 3
  game_over = False
  win = False

  running = True
  while running:
    clock.tick(FPS)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.KEYDOWN and (game_over or win):
        if event.key == pygame.K_r:
          return main()  # Перезапуск игры

    if not game_over and not win:
      player.update()
      viruses.update()

      # Логика сбора капсул
      collected = pygame.sprite.spritecollide(player, capsules, True)
      for cap in collected:
        score += 1
        if score >= target_score:
          win = True
        else:
          # Появление новой капсулы после сбора
          new_cap = Capsule()
          capsules.add(new_cap)
          all_sprites.add(new_cap)

      # Проверка столкновения с вирусами
      if pygame.sprite.spritecollide(player, viruses, False):
        lives -= 1
        player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        if lives <= 0:
          game_over = True

    # Отрисовка элементов
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Вывод интерфейса
    score_text = font_small.render(
        f"Энергия собрана: {score} / {target_score}", True, WHITE
    )
    lives_text = font_small.render(f"Жизни: {lives}", True, RED)
    screen.blit(score_text, (20, 20))
    screen.blit(lives_text, (20, 50))

    # Окна победы / поражения
    if win:
      win_surf = font_large.render("ПОБЕДА! Нажмите 'R' для новой игры", True, GREEN)
      screen.blit(
          win_surf,
          win_surf.get_rect(
              center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
          ),
      )
    elif game_over:
      lose_surf = font_large.render(
          "СИСТЕМА ЗАРАЖЕНА. Нажмите 'R' для сброса", True, RED
      )
      screen.blit(
          lose_surf,
          lose_surf.get_rect(
              center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
          ),
      )

    pygame.display.flip()

  pygame.quit()
  sys.exit()


if __name__ == "__main__":
  main()