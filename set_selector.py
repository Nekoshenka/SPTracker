"""
Окно выбора набора со списком и фильтром
"""

from datetime import datetime

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit,
    QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from locales import get_text


class SetSelector(QDialog):
    """Окно выбора набора со списком"""

    def __init__(self, parent=None, sets=None, current_lang="en", dark_theme=True, existing_progress=None):
        super().__init__(parent)
        self.sets = sets or []
        self.current_lang = current_lang
        self.dark_theme = dark_theme
        self.existing_progress = existing_progress or set()
        self.selected_char_id = None
        self.selected_id = None
        self.selected_name = None

        self.init_ui()
        self.load_sets()
        self.update_theme()

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] SetSelector: {message}")

    def init_ui(self):
        """Настройка интерфейса"""
        self.log("init_ui: started")
        self.setModal(True)
        self.setWindowTitle(get_text("select_set_title", self.current_lang))
        self.setMinimumSize(500, 450)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        self.title = QLabel(get_text("select_set", self.current_lang))
        self.title.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(self.title)

        search_layout = QHBoxLayout()
        search_label = QLabel("🔍")
        search_label.setStyleSheet("font-size: 16px;")
        search_layout.addWidget(search_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(get_text("search_set", self.current_lang))
        self.search_input.textChanged.connect(self.filter_sets)
        search_layout.addWidget(self.search_input)

        main_layout.addLayout(search_layout)

        self.count_label = QLabel()
        self.count_label.setStyleSheet("font-style: italic;")
        self.count_label.setAlignment(Qt.AlignRight)
        main_layout.addWidget(self.count_label)

        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.select_set)
        self.list_widget.itemClicked.connect(self.on_item_selected)
        main_layout.addWidget(self.list_widget)

        self.select_btn = QPushButton(get_text("confirm_selection", self.current_lang))
        self.select_btn.setMinimumHeight(35)
        self.select_btn.clicked.connect(self.confirm_selection)
        self.select_btn.setEnabled(False)
        main_layout.addWidget(self.select_btn)

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
            QListWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #3d3d3d;
            }
            QListWidget::item:hover {
                background-color: #3d3d3d;
            }
            QListWidget::item:selected {
                background-color: #4CAF50;
                color: white;
            }
            QScrollArea {
                border: none;
                background-color: #1e1e1e;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #444444;
                color: #777777;
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
            QListWidget {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eeeeee;
            }
            QListWidget::item:hover {
                background-color: #f0f0f0;
            }
            QListWidget::item:selected {
                background-color: #4CAF50;
                color: white;
            }
            QScrollArea {
                border: none;
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #e8e8e8;
                color: #999999;
            }
        """)

        self.title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333333;")
        self.count_label.setStyleSheet("color: #666666; font-style: italic;")

    def load_sets(self, filter_text=""):
        """Загружает наборы с фильтром"""
        self.log(f"load_sets: filter='{filter_text}'")
        self.list_widget.clear()

        filter_lower = filter_text.lower()
        filtered = []
        for set_id, name in self.sets:
            if filter_text and filter_lower not in name.lower():
                continue
            filtered.append((set_id, name))

        if not filtered:
            item = QListWidgetItem(get_text("no_sets_found", self.current_lang))
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.list_widget.addItem(item)
            self.count_label.setText(get_text("found_count", self.current_lang).format(0))
            return

        filtered.sort(key=lambda x: x[1].lower())

        for set_id, name in filtered:
            has_progress = False
            if self.selected_char_id and self.existing_progress:
                has_progress = (self.selected_char_id, set_id) in self.existing_progress

            display_text = f"✅ {name}" if has_progress else name

            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, set_id)

            if has_progress:
                font = item.font()
                font.setBold(True)
                item.setFont(font)

                if self.dark_theme:
                    item.setBackground(QColor(30, 80, 30))
                    item.setForeground(QColor(150, 255, 150))
                else:
                    item.setBackground(QColor(180, 230, 180))
                    item.setForeground(QColor(0, 130, 0))

            self.list_widget.addItem(item)

        self.count_label.setText(get_text("found_count", self.current_lang).format(len(filtered)))
        self.log(f"  loaded {len(filtered)} sets")

    def filter_sets(self, text):
        """Фильтрует наборы по введённому тексту"""
        self.load_sets(text)
        self.select_btn.setEnabled(False)

    def on_item_selected(self, item):
        """Обработчик клика по элементу"""
        self.selected_id = item.data(Qt.ItemDataRole.UserRole)
        self.selected_name = item.text()
        self.select_btn.setEnabled(True)
        self.log(f"  item selected: {self.selected_id} -> {self.selected_name}")

    def select_set(self, item):
        """Выбирает набор по двойному клику"""
        self.on_item_selected(item)
        self.confirm_selection()

    def confirm_selection(self):
        """Подтверждает выбор"""
        if self.selected_id and self.selected_name:
            self.log(f"confirm_selection: {self.selected_id} -> {self.selected_name}")
            self.accept()

    def get_selected_id(self):
        return self.selected_id

    def get_selected_name(self):
        return self.selected_name

    def set_character_id(self, char_id):
        """Устанавливает ID персонажа для проверки существующего прогресса"""
        self.selected_char_id = char_id
        self.load_sets(self.search_input.text() if hasattr(self, 'search_input') else "")

    def closeEvent(self, event):
        self.log("closeEvent: called")
        event.accept()

    def reject(self):
        self.log("reject: called")
        super().reject()

    def accept(self):
        self.log("accept: called")
        super().accept()
