"""
Окно выбора персонажа с плитками
"""

import os
import sys
from datetime import datetime

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QScrollArea, QWidget,
    QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont

from locales import get_text


class CharacterSelector(QDialog):
    """Окно выбора персонажа с плитками"""

    COLS = 4

    def __init__(self, parent=None, characters=None, current_lang="en", game_data=None, dark_theme=True,
                 existing_progress=None, current_set_id=None):
        super().__init__(parent)
        self.characters = characters or []
        self.current_lang = current_lang
        self.game_data = game_data
        self.dark_theme = dark_theme
        self.existing_progress = existing_progress or set()
        self.current_set_id = current_set_id
        self.selected_id = None
        self.selected_name = None

        self.current_filter = ""

        self.init_ui()
        self.load_characters()
        self.update_theme()

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] CharacterSelector: {message}")

    def init_ui(self):
        """Настройка интерфейса"""
        self.log("init_ui: started")
        self.setModal(True)
        self.setWindowTitle(get_text("select_character_title", self.current_lang))

        self.setFixedWidth(730)
        self.setMinimumHeight(400)
        self.setMaximumHeight(800)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        self.title = QLabel(get_text("select_character", self.current_lang))
        self.title.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(self.title)

        search_layout = QHBoxLayout()
        search_label = QLabel("🔍")
        search_label.setStyleSheet("font-size: 16px;")
        search_layout.addWidget(search_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(get_text("search_character", self.current_lang))
        self.search_input.textChanged.connect(self.filter_characters)
        search_layout.addWidget(self.search_input)

        main_layout.addLayout(search_layout)

        self.count_label = QLabel()
        self.count_label.setStyleSheet("font-style: italic;")
        self.count_label.setAlignment(Qt.AlignRight)
        main_layout.addWidget(self.count_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setContentsMargins(5, 5, 5, 5)
        self.grid_layout.setSpacing(10)
        self.grid_layout.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

        self.log("init_ui: completed")

    def update_theme(self):
        """Обновляет тему окна"""
        if self.dark_theme:
            self._apply_dark_theme()
        else:
            self._apply_light_theme()

    def _apply_dark_theme(self):
        """Применяет тёмную тему"""
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #e0e0e0;
            }
            QLineEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
            QScrollArea {
                border: none;
                background-color: #1e1e1e;
            }
            QScrollArea > QWidget > QWidget {
                background-color: #1e1e1e;
            }
            QPushButton {
                background-color: #2d2d2d;
                border: 2px solid #444444;
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
                border: 2px solid #4CAF50;
            }
            QPushButton:pressed {
                background-color: #4d4d4d;
            }
        """)

        self.title.setStyleSheet("font-size: 18px; font-weight: bold; color: #e0e0e0;")
        self.count_label.setStyleSheet("color: #999999; font-style: italic;")

    def _apply_light_theme(self):
        """Применяет светлую тему"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333333;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
            QScrollArea {
                border: none;
                background-color: #f0f0f0;
            }
            QScrollArea > QWidget > QWidget {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #ffffff;
                border: 2px solid #cccccc;
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border: 2px solid #4CAF50;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)

        self.title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333333;")
        self.count_label.setStyleSheet("color: #666666; font-style: italic;")

    def get_image_path(self, char_id):
        """Возвращает путь к изображению персонажа"""
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        images_dir = os.path.join(base_dir, "data", "images")

        self.log(f"  images_dir: {images_dir}")

        if not os.path.exists(images_dir):
            self.log(f"  ERROR: images_dir does not exist!")
            return None

        try:
            files = os.listdir(images_dir)
            self.log(f"  found {len(files)} files in images_dir")
            if files:
                self.log(f"  first 5 files: {files[:5]}")
        except Exception as e:
            self.log(f"  ERROR reading directory: {e}")

        extensions = ['.webp', '.png', '.jpg', '.jpeg']

        for ext in extensions:
            filename = f"{char_id}_pic{ext}"
            full_path = os.path.join(images_dir, filename)
            self.log(f"  checking: {full_path}")
            if os.path.exists(full_path):
                self.log(f"  FOUND: {full_path}")
                return full_path

        fallback_path = os.path.join(images_dir, "fallback_pic.webp")
        self.log(f"  checking fallback: {fallback_path}")
        if os.path.exists(fallback_path):
            self.log(f"  USING FALLBACK: {fallback_path}")
            return fallback_path

        self.log(f"  NOT FOUND: no image for '{char_id}'")
        return None

    def load_characters(self, filter_text=""):
        """Загружает плитки персонажей с фильтром"""
        self.log(f"load_characters: filter='{filter_text}'")
        self.current_filter = filter_text

        self.clear_layout(self.grid_layout)

        filter_lower = filter_text.lower()
        filtered = []
        for char_id, name in self.characters:
            if filter_text and filter_lower not in name.lower():
                continue
            filtered.append((char_id, name))

        if not filtered:
            empty_label = QLabel(get_text("no_characters_found", self.current_lang))
            empty_label.setStyleSheet("color: #666666; font-size: 16px;")
            empty_label.setAlignment(Qt.AlignCenter)
            self.grid_layout.addWidget(empty_label, 0, 0, 1, self.COLS)
            self.count_label.setText(get_text("found_count", self.current_lang).format(0))
            return

        filtered.sort(key=lambda x: x[1].lower())

        self.log(f"  using {self.COLS} columns (fixed)")

        for i, (char_id, name) in enumerate(filtered):
            row = i // self.COLS
            col = i % self.COLS

            tile = self.create_tile(char_id, name, self.current_set_id)
            self.grid_layout.addWidget(tile, row, col)

        self.count_label.setText(get_text("found_count", self.current_lang).format(len(filtered)))
        self.log(f"  loaded {len(filtered)} characters")

    def create_tile(self, char_id, name, set_id=None):
        """Создаёт одну плитку персонажа"""
        tile = QPushButton()
        tile.setFixedSize(160, 190)

        has_progress = False
        if set_id and self.existing_progress:
            has_progress = (char_id, set_id) in self.existing_progress

        if self.dark_theme:
            if has_progress:
                tile.setStyleSheet("""
                    QPushButton {
                        background-color: #2a5a2a;
                        border: 3px solid #66BB6A;
                        border-radius: 8px;
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: #3a6a3a;
                        border: 3px solid #81C784;
                    }
                    QPushButton:pressed {
                        background-color: #4a7a4a;
                    }
                """)
            else:
                tile.setStyleSheet("""
                    QPushButton {
                        background-color: #2d2d2d;
                        border: 2px solid #444444;
                        border-radius: 8px;
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: #3d3d3d;
                        border: 2px solid #4CAF50;
                    }
                    QPushButton:pressed {
                        background-color: #4d4d4d;
                    }
                """)
        else:
            if has_progress:
                tile.setStyleSheet("""
                    QPushButton {
                        background-color: #c8e6c9;
                        border: 3px solid #4CAF50;
                        border-radius: 8px;
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: #a5d6a7;
                        border: 3px solid #66BB6A;
                    }
                    QPushButton:pressed {
                        background-color: #81c784;
                    }
                """)
            else:
                tile.setStyleSheet("""
                    QPushButton {
                        background-color: #ffffff;
                        border: 2px solid #cccccc;
                        border-radius: 8px;
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: #f0f0f0;
                        border: 2px solid #4CAF50;
                    }
                    QPushButton:pressed {
                        background-color: #e0e0e0;
                    }
                """)

        layout = QVBoxLayout(tile)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        image_path = self.get_image_path(char_id)
        pixmap = None

        if image_path:
            pixmap = QPixmap()
            if pixmap.load(image_path):
                self.log(f"  loaded image: {image_path}")
                pixmap = pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            else:
                self.log(f"  FAILED to load image: {image_path}")
                pixmap = None

        if pixmap is None:
            self.log(f"  creating fallback for: {char_id}")
            if self.dark_theme:
                bg_color = QColor(60, 60, 60)
                text_color = QColor(200, 200, 200)
            else:
                bg_color = QColor(220, 220, 220)
                text_color = QColor(80, 80, 80)

            pixmap = QPixmap(140, 140)
            pixmap.fill(bg_color)

            painter = QPainter(pixmap)
            painter.setPen(text_color)
            painter.setFont(QFont("Arial", 32, QFont.Bold))

            initials = name[0].upper() if name else "?"
            painter.drawText(pixmap.rect(), Qt.AlignCenter, initials)
            painter.end()

        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignCenter)

        if has_progress:
            font = QFont()
            font.setBold(True)
            name_label.setFont(font)

        if self.dark_theme:
            if has_progress:
                name_label.setStyleSheet("color: #81C784; font-size: 13px; font-weight: bold;")
            else:
                name_label.setStyleSheet("color: #e0e0e0; font-size: 12px; font-weight: bold;")
        else:
            if has_progress:
                name_label.setStyleSheet("color: #2E7D32; font-size: 13px; font-weight: bold;")
            else:
                name_label.setStyleSheet("color: #333333; font-size: 12px; font-weight: bold;")

        name_label.setWordWrap(True)
        layout.addWidget(name_label)

        if has_progress:
            indicator = QLabel("✅")
            indicator.setAlignment(Qt.AlignCenter)
            indicator.setStyleSheet("font-size: 18px; background-color: transparent;")
            layout.addWidget(indicator)

        tile.setProperty("char_id", char_id)
        tile.setProperty("char_name", name)
        tile.clicked.connect(lambda: self.select_character(char_id, name))

        return tile

    def clear_layout(self, layout):
        """Очищает layout от всех виджетов"""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def filter_characters(self, text):
        """Фильтрует персонажей по введённому тексту"""
        self.load_characters(text)

    def select_character(self, char_id, name):
        """Выбирает персонажа и закрывает окно"""
        self.log(f"select_character: {char_id} -> {name}")
        self.selected_id = char_id
        self.selected_name = name
        self.accept()

    def get_selected_id(self):
        return self.selected_id

    def get_selected_name(self):
        return self.selected_name

    def closeEvent(self, event):
        self.log("closeEvent: called")
        event.accept()

    def reject(self):
        self.log("reject: called")
        super().reject()

    def accept(self):
        self.log("accept: called")
        super().accept()
