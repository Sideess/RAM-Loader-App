import pygame
import sys

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 500
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
LIGHT_GRAY = (230, 230, 230)
BLUE = (50, 150, 255)
RED = (220, 50, 50)
GREEN = (50, 200, 50)

FONT_MAIN = pygame.font.SysFont("Arial", 22)
FONT_SMALL = pygame.font.SysFont("Arial", 16)
FONT_BOLD = pygame.font.SysFont("Arial", 24, bold=True)


class Entry:

    def __init__(self, x, y, width, height, text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.active = False
        self.color = DARK_GRAY

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = BLUE
            else:
                self.active = False
                self.color = DARK_GRAY

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if event.unicode.isdigit() and len(self.text) < 5:
                    self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surf = FONT_MAIN.render(self.text, True, BLACK)
        screen.blit(text_surf, (self.rect.x + 10, self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

        if not self.text and not self.active:
            hint_surf = FONT_SMALL.render("10 - 500", True, DARK_GRAY)
            screen.blit(hint_surf, (self.rect.x + 10, self.rect.y + (self.rect.height - hint_surf.get_height()) // 2))


class Button:
    """Задача №1: Кнопка «Загрузить в ОЗУ»"""

    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = GRAY

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.color = LIGHT_GRAY
        else:
            self.color = GRAY

        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        pygame.draw.rect(screen, DARK_GRAY, self.rect, 2, border_radius=5)

        text_surf = FONT_MAIN.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False


class MemoryBar:

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.progress = 0.0
        self.target_progress = 0.0
        self.fill_speed = 0.0
        self.is_animating = False

    def start_loading(self, file_size):

        duration_frames = (file_size / 500.0) * 5 * FPS
        if duration_frames == 0: duration_frames = 1

        added_progress = file_size / 500.0
        self.target_progress = min(self.progress + added_progress, 1.0)

        self.fill_speed = (self.target_progress - self.progress) / duration_frames
        self.is_animating = True

    def update(self):
        if self.is_animating:
            if self.progress < self.target_progress:
                self.progress += self.fill_speed
                if self.progress >= self.target_progress:
                    self.progress = self.target_progress
                    self.is_animating = False
            else:
                self.is_animating = False

    def draw(self, screen):
        pygame.draw.rect(screen, DARK_GRAY, self.rect, 3)
        inner_bg = pygame.Rect(self.rect.x + 3, self.rect.y + 3, self.rect.width - 6, self.rect.height - 6)
        pygame.draw.rect(screen, LIGHT_GRAY, inner_bg)

        if self.progress > 0:
            fill_width = int((self.rect.width - 6) * self.progress)
            fill_rect = pygame.Rect(self.rect.x + 3, self.rect.y + 3, fill_width, self.rect.height - 6)
            color = RED if self.progress >= 1.0 else GREEN
            pygame.draw.rect(screen, color, fill_rect)

        text_surf = FONT_SMALL.render(f"Использовано ОЗУ: {int(self.progress * 100)}%", True, BLACK)
        screen.blit(text_surf, (self.rect.x, self.rect.y - 25))


class MessageBox:

    def __init__(self, title, message):
        self.rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 90, 400, 180)
        self.title = title
        self.message = message
        self.ok_button = Button(self.rect.centerx - 50, self.rect.bottom - 50, 100, 35, "OK")
        self.visible = False

    def show(self):
        self.visible = True

    def handle_event(self, event):
        if self.visible:
            if self.ok_button.is_clicked(event):
                self.visible = False
                return True
        return False

    def draw(self, screen):
        if not self.visible:
            return

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, WHITE, self.rect, border_radius=8)
        pygame.draw.rect(screen, RED, self.rect, 4, border_radius=8)

        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y, self.rect.width, 35), border_radius=4)
        title_surf = FONT_BOLD.render(self.title, True, WHITE)
        screen.blit(title_surf, (self.rect.x + 15, self.rect.y + 5))

        msg_surf = FONT_MAIN.render(self.message, True, BLACK)
        screen.blit(msg_surf, (self.rect.x + 20, self.rect.y + 60))

        self.ok_button.draw(screen)


class Application:

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Монитор загрузки ОЗУ")
        self.clock = pygame.time.Clock()
        self.running = True

        self.entry = Entry(50, 80, 150, 40)
        self.btn_load = Button(220, 80, 200, 40, "Загрузить в ОЗУ")
        self.memory_bar = MemoryBar(50, 220, 700, 50)
        self.message_box = MessageBox("Внимание!", "Недостаточно оперативной памяти!")

        self.error_text = ""

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.message_box.visible:
                if self.message_box.handle_event(event):
                    self.memory_bar.progress = 0.0
                    self.memory_bar.target_progress = 0.0
                continue

            self.entry.handle_event(event)

            if self.btn_load.is_clicked(event):
                if self.memory_bar.is_animating:
                    continue

                raw_text = self.entry.text
                if not raw_text:
                    self.error_text = "Ошибка: Введите число!"
                    continue

                val = int(raw_text)
                if 10 <= val <= 500:
                    self.error_text = ""
                    self.memory_bar.start_loading(val)
                else:
                    self.error_text = "Ошибка: Допустимый объем от 10 до 500 Мб!"

    def update(self):
        self.memory_bar.update()

        if self.memory_bar.progress >= 1.0 and not self.memory_bar.is_animating and not self.message_box.visible:
            self.message_box.show()

    def draw(self):
        self.screen.fill(LIGHT_GRAY)

        label_entry = FONT_MAIN.render("Объем файла (Мб):", True, BLACK)
        self.screen.blit(label_entry, (50, 50))

        self.entry.draw(self.screen)
        self.btn_load.draw(self.screen)
        self.memory_bar.draw(self.screen)

        if self.error_text:
            err_surf = FONT_SMALL.render(self.error_text, True, RED)
            self.screen.blit(err_surf, (50, 130))

        self.message_box.draw(self.screen)

        pygame.display.flip()


if __name__ == "__main__":
    app = Application()
    app.run()