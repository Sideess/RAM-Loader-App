import pygame
import sys

# Инициализация Pygame
pygame.init()
pygame.font.init()

# Константы окна
WIDTH, HEIGHT = 800, 500
FPS = 60

# Цветовая палитра
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
LIGHT_GRAY = (230, 230, 230)
BLUE = (50, 150, 255)
RED = (220, 50, 50)
GREEN = (50, 200, 50)

# Шрифты
FONT_MAIN = pygame.font.SysFont("Arial", 22)
FONT_SMALL = pygame.font.SysFont("Arial", 16)
FONT_BOLD = pygame.font.SysFont("Arial", 24, bold=True)


class Entry:
    """Задача №1: Текстовое поле для ввода объема файла"""

    def __init__(self, x, y, width, height, text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.active = False
        self.color = DARK_GRAY

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Если кликнули по полю, оно становится активным
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
                # Разрешаем ввод только цифр, так как нам нужно число мегабайт
                if event.unicode.isdigit() and len(self.text) < 5:
                    self.text += event.unicode

    def draw(self, screen):
        # Задний фон поля
        pygame.draw.rect(screen, WHITE, self.rect)
        # Рамка поля
        pygame.draw.rect(screen, self.color, self.rect, 2)
        # Текст внутри поля
        text_surf = FONT_MAIN.render(self.text, True, BLACK)
        screen.blit(text_surf, (self.rect.x + 10, self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

        # Подсказка, если поле пустое
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
        # Эффект наведения мыши
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
    """Задача №2: Класс шкалы памяти ОЗУ"""

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.progress = 0.0  # Прогресс заполнения от 0.0 до 1.0
        self.target_progress = 0.0
        self.fill_speed = 0.0
        self.is_animating = False

    def start_loading(self, file_size):
        """Задача №3: Расчет скорости анимации в зависимости от размера файла"""
        # Базовый объем ОЗУ примем за 1000 Мб для демонстрации.
        # Чем больше файл, тем меньше скорость заполнения (дольше идет анимация)
        # Задаем базовое время: файл в 10 Мб заполнится мгновенно, 500 Мб — за несколько секунд
        duration_frames = (file_size / 500.0) * 5 * FPS  # До 5 секунд для максимального файла
        if duration_frames == 0: duration_frames = 1

        # Определяем, какую часть шкалы займет файл (например, пропорционально размеру)
        # Для наглядности задачи №4 сделаем так, чтобы файл увеличивал шкалу на свою долю
        added_progress = file_size / 500.0
        self.target_progress = min(self.progress + added_progress, 1.0)

        # Скорость изменения прогресса за один кадр
        self.fill_speed = (self.target_progress - self.progress) / duration_frames
        self.is_animating = True

    def update(self):
        """Задача №3: Плавное заполнение слева направо"""
        if self.is_animating:
            if self.progress < self.target_progress:
                self.progress += self.fill_speed
                if self.progress >= self.target_progress:
                    self.progress = self.target_progress
                    self.is_animating = False
            else:
                self.is_animating = False

    def draw(self, screen):
        # Рисуем большой прямоугольный контур (шкалу)
        pygame.draw.rect(screen, DARK_GRAY, self.rect, 3)
        # Рисуем фон шкалы (свободное место)
        # Рисуем фон шкалы (свободное место) вручную с отступом в 3 пикселя со всех сторон
        inner_bg = pygame.Rect(self.rect.x + 3, self.rect.y + 3, self.rect.width - 6, self.rect.height - 6)
        pygame.draw.rect(screen, LIGHT_GRAY, inner_bg)

        # Рисуем сплошной цвет заполнения
        if self.progress > 0:
            fill_width = int((self.rect.width - 6) * self.progress)
            fill_rect = pygame.Rect(self.rect.x + 3, self.rect.y + 3, fill_width, self.rect.height - 6)
            # Если заполнено полностью — красим в красный, иначе в зеленый
            color = RED if self.progress >= 1.0 else GREEN
            pygame.draw.rect(screen, color, fill_rect)

        # Вывод процентов текста поверх шкалы
        text_surf = FONT_SMALL.render(f"Использовано ОЗУ: {int(self.progress * 100)}%", True, BLACK)
        screen.blit(text_surf, (self.rect.x, self.rect.y - 25))


class MessageBox:
    """Задача №4: Кастомное окно предупреждения (showwarning)"""

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

        # Полупрозрачная подложка на весь экран
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))

        # Тело окна предупреждения
        pygame.draw.rect(screen, WHITE, self.rect, border_radius=8)
        pygame.draw.rect(screen, RED, self.rect, 4, border_radius=8)

        # Шапка окна
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y, self.rect.width, 35), border_radius=4)
        title_surf = FONT_BOLD.render(self.title, True, WHITE)
        screen.blit(title_surf, (self.rect.x + 15, self.rect.y + 5))

        # Текст сообщения
        msg_surf = FONT_MAIN.render(self.message, True, BLACK)
        screen.blit(msg_surf, (self.rect.x + 20, self.rect.y + 60))

        # Кнопка ОК
        self.ok_button.draw(screen)


class Application:
    """Главный управляющий класс приложения"""

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Монитор загрузки ОЗУ")
        self.clock = pygame.time.Clock()
        self.running = True

        # Инициализация интерфейса
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

            # Если открыт messagebox, блокируем остальной интерфейс
            if self.message_box.visible:
                if self.message_box.handle_event(event):
                    # При закрытии окна предупреждения можно сбросить шкалу
                    self.memory_bar.progress = 0.0
                    self.memory_bar.target_progress = 0.0
                continue

            # Обработка ввода в текстовое поле
            self.entry.handle_event(event)

            # Обработка нажатия кнопки «Загрузить в ОЗУ»
            if self.btn_load.is_clicked(event):
                if self.memory_bar.is_animating:
                    continue  # Идет процесс загрузки, игнорируем новые клики

                raw_text = self.entry.text
                if not raw_text:
                    self.error_text = "Ошибка: Введите число!"
                    continue

                val = int(raw_text)
                # Проверка диапазона от 10 до 500 Мб
                if 10 <= val <= 500:
                    self.error_text = ""
                    self.memory_bar.start_loading(val)
                else:
                    self.error_text = "Ошибка: Допустимый объем от 10 до 500 Мб!"

    def update(self):
        # Обновление шкалы ОЗУ
        self.memory_bar.update()

        # Задача №4: Проверка достижения 100% (progress == 1.0)
        if self.memory_bar.progress >= 1.0 and not self.memory_bar.is_animating and not self.message_box.visible:
            self.message_box.show()

    def draw(self):
        self.screen.fill(LIGHT_GRAY)

        # Текстовые подписи GUI
        label_entry = FONT_MAIN.render("Объем файла (Мб):", True, BLACK)
        self.screen.blit(label_entry, (50, 50))

        # Отрисовка компонентов
        self.entry.draw(self.screen)
        self.btn_load.draw(self.screen)
        self.memory_bar.draw(self.screen)

        # Отрисовка ошибок валидации (если введен некорректный объем)
        if self.error_text:
            err_surf = FONT_SMALL.render(self.error_text, True, RED)
            self.screen.blit(err_surf, (50, 130))

        # Отрисовка MessageBox поверх всего при активации
        self.message_box.draw(self.screen)

        pygame.display.flip()


if __name__ == "__main__":
    app = Application()
    app.run()