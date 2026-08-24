"""
Окно статистики аккаунта
"""

from datetime import datetime

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from locales import get_text


class StatisticsWindow(QDialog):
    """Окно статистики аккаунта"""

    def __init__(self, parent=None, game_data=None, account_data=None, lang="en", dark_theme=True):
        super().__init__(parent)
        self.parent_window = parent
        self.game_data = game_data
        self.account_data = account_data
        self.current_lang = lang
        self.dark_theme = dark_theme

        self.init_ui()
        self.calculate_statistics()
        self.fill_table()
        self.fill_percent_table()
        self.update_theme()

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] StatisticsWindow: {message}")

    def init_ui(self):
        """Настройка интерфейса"""
        self.log("init_ui: started")
        self.setModal(True)
        self.setWindowTitle(get_text("statistics_title", self.current_lang))
        self.setFixedSize(800, 600)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        self.title_label = QLabel(get_text("statistics_title", self.current_lang))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(self.title_label)

        self.info_label = QLabel(
            get_text("statistics_account_info", self.current_lang).format(
                self.account_data.get("account_name", "Unknown")
            )
        )
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-size: 14px;")
        main_layout.addWidget(self.info_label)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setRowCount(3)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.table.setHorizontalHeaderLabels([
            get_text("stat_col_sets", self.current_lang),
            get_text("stat_col_gems", self.current_lang),
            get_text("stat_col_mora", self.current_lang)
        ])

        self.table.setVerticalHeaderLabels([
            get_text("stat_row_obtained", self.current_lang),
            get_text("stat_row_max_owned", self.current_lang),
            get_text("stat_row_max_absolute", self.current_lang)
        ])

        main_layout.addWidget(self.table, 3)

        self.percent_title = QLabel(get_text("stat_percent_title", self.current_lang))
        self.percent_title.setAlignment(Qt.AlignCenter)
        self.percent_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 5px; margin-bottom: 5px;")
        self.percent_title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        main_layout.addWidget(self.percent_title, 1)

        self.percent_table = QTableWidget()
        self.percent_table.setColumnCount(2)
        self.percent_table.setRowCount(1)
        self.percent_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.percent_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.percent_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.percent_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.percent_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)

        self.percent_table.setHorizontalHeaderLabels([
            get_text("stat_percent_owned", self.current_lang),
            get_text("stat_percent_limit", self.current_lang)
        ])

        self.percent_table.setVerticalHeaderLabels([
            get_text("stat_percent_progress", self.current_lang)
        ])

        self.percent_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.percent_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        main_layout.addWidget(self.percent_table, 1)

        self.close_btn = QPushButton(get_text("stat_btn_close", self.current_lang))
        self.close_btn.setMinimumHeight(40)
        self.close_btn.clicked.connect(self.accept)

        close_layout = QHBoxLayout()
        close_layout.addStretch()
        close_layout.addWidget(self.close_btn)
        close_layout.addStretch()
        main_layout.addLayout(close_layout)

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
            QFrame {
                background-color: #2d2d2d;
                border: 1px solid #444444;
                border-radius: 8px;
            }
            QTableWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444444;
                border-radius: 4px;
                gridline-color: #444444;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #4CAF50;
                color: white;
            }
            QHeaderView::section {
                background-color: #3d3d3d;
                color: #e0e0e0;
                border: 1px solid #444444;
                padding: 8px;
                font-weight: bold;
            }
            QTableCornerButton::section {
                background-color: #4d4d4d;
                border: 1px solid #444444;
            }
            QPushButton {
                background-color: #3d3d3d;
                color: #e0e0e0;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
            QPushButton:pressed {
                background-color: #2d2d2d;
            }
        """)

        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #e0e0e0;")
        self.info_label.setStyleSheet("font-size: 14px; color: #999999;")
        self.percent_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #e0e0e0; margin-top: 15px;")
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #3d3d3d;
                color: #e0e0e0;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
            QPushButton:pressed {
                background-color: #2d2d2d;
            }
        """)

    def _apply_light_theme(self):
        """Применяет светлую тему"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333333;
            }
            QFrame {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 8px;
            }
            QTableWidget {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 4px;
                gridline-color: #cccccc;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #4CAF50;
                color: white;
            }
            QHeaderView::section {
                background-color: #e8e8e8;
                color: #333333;
                border: 1px solid #cccccc;
                padding: 8px;
                font-weight: bold;
            }
            QTableCornerButton::section {
                background-color: #d8d8d8;
                border: 1px solid #cccccc;
            }
            QPushButton {
                background-color: #f0f0f0;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)

        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333333;")
        self.info_label.setStyleSheet("font-size: 14px; color: #666666;")
        self.percent_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #333333; margin-top: 15px;")
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)

    def calculate_statistics(self):
        """Вычисляет все статистические данные"""
        self.log("calculate_statistics: started")

        characters_data = self.game_data.get("characters", {})
        sets_data = self.game_data.get("sets", {})
        owned_ids = self.account_data.get("owned_characters", [])
        progress = self.account_data.get("progress", [])

        unique_progress = set()
        for entry in progress:
            char_id = entry.get("character_id")
            set_id = entry.get("set_id")
            if char_id and set_id:
                unique_progress.add((char_id, set_id))

        obtained_sets = len(unique_progress)
        self.log(f"  obtained_sets: {obtained_sets}")

        max_owned_sets = 0
        for char_id in owned_ids:
            if char_id in characters_data:
                char_sets = []
                for set_id, set_data in sets_data.items():
                    liked_by = set_data.get("liked_by", [])
                    if char_id in liked_by:
                        char_sets.append(set_id)
                max_owned_sets += len(char_sets)

        self.log(f"  max_owned_sets: {max_owned_sets}")

        absolute_max_sets = 0
        for char_id, char_data in characters_data.items():
            char_sets = []
            for set_id, set_data in sets_data.items():
                liked_by = set_data.get("liked_by", [])
                if char_id in liked_by:
                    char_sets.append(set_id)
            absolute_max_sets += len(char_sets)

        self.log(f"  absolute_max_sets: {absolute_max_sets}")

        if max_owned_sets > 0:
            percent_owned = round((obtained_sets / max_owned_sets) * 100, 2)
        else:
            percent_owned = 0.0

        self.log(f"  percent_owned: {percent_owned}%")

        if absolute_max_sets > 0:
            percent_absolute = round((obtained_sets / absolute_max_sets) * 100, 2)
        else:
            percent_absolute = 0.0

        self.log(f"  percent_absolute: {percent_absolute}%")

        if absolute_max_sets > 0:
            limit_percent = round((max_owned_sets / absolute_max_sets) * 100, 2)
        else:
            limit_percent = 0.0

        self.log(f"  limit_percent: {limit_percent}%")

        self.stats = {
            "obtained": obtained_sets,
            "max_owned": max_owned_sets,
            "max_absolute": absolute_max_sets,
            "percent_owned": percent_owned,
            "percent_absolute": percent_absolute,
            "limit_percent": limit_percent,
            "limit_display": f"{max_owned_sets}/{absolute_max_sets}"
        }

        self.log("calculate_statistics: completed")

    def fill_table(self):
        """Заполняет первую таблицу данными"""
        self.log("fill_table: started")

        obtained = self.stats["obtained"]
        max_owned = self.stats["max_owned"]
        max_absolute = self.stats["max_absolute"]

        for row in range(3):
            for col in range(3):
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignCenter)
                if self.dark_theme:
                    item.setBackground(QColor(45, 45, 45))
                else:
                    item.setBackground(QColor(255, 255, 255))
                self.table.setItem(row, col, item)

        value_item = QTableWidgetItem(str(obtained))
        value_item.setTextAlignment(Qt.AlignCenter)
        if self.dark_theme:
            value_item.setBackground(QColor(45, 45, 45))
        else:
            value_item.setBackground(QColor(255, 255, 255))
        self.table.setItem(0, 0, value_item)

        gems_obtained = obtained * 20
        mora_obtained = obtained * 20000

        value_item = QTableWidgetItem(f"{gems_obtained:,} ✦".replace(",", " "))
        value_item.setTextAlignment(Qt.AlignCenter)
        if self.dark_theme:
            value_item.setBackground(QColor(45, 45, 45))
        else:
            value_item.setBackground(QColor(255, 255, 255))
        self.table.setItem(0, 1, value_item)

        value_item = QTableWidgetItem(f"{mora_obtained:,} ◎".replace(",", " "))
        value_item.setTextAlignment(Qt.AlignCenter)
        if self.dark_theme:
            value_item.setBackground(QColor(45, 45, 45))
        else:
            value_item.setBackground(QColor(255, 255, 255))
        self.table.setItem(0, 2, value_item)

        # Строка 2: Максимум из имеющихся
        value_item = QTableWidgetItem(str(max_owned))
        value_item.setTextAlignment(Qt.AlignCenter)
        if self.dark_theme:
            value_item.setBackground(QColor(45, 45, 45))
        else:
            value_item.setBackground(QColor(255, 255, 255))
        self.table.setItem(1, 0, value_item)

        gems_max_owned = max_owned * 20
        mora_max_owned = max_owned * 20000

        value_item = QTableWidgetItem(f"{gems_max_owned:,} ✦".replace(",", " "))
        value_item.setTextAlignment(Qt.AlignCenter)
        if self.dark_theme:
            value_item.setBackground(QColor(45, 45, 45))
        else:
            value_item.setBackground(QColor(255, 255, 255))
        self.table.setItem(1, 1, value_item)

        value_item = QTableWidgetItem(f"{mora_max_owned:,} ◎".replace(",", " "))
        value_item.setTextAlignment(Qt.AlignCenter)
        if self.dark_theme:
            value_item.setBackground(QColor(45, 45, 45))
        else:
            value_item.setBackground(QColor(255, 255, 255))
        self.table.setItem(1, 2, value_item)

        # Строка 3: Абсолютный максимум
        value_item = QTableWidgetItem(str(max_absolute))
        value_item.setTextAlignment(Qt.AlignCenter)
        if self.dark_theme:
            value_item.setBackground(QColor(45, 45, 45))
        else:
            value_item.setBackground(QColor(255, 255, 255))
        self.table.setItem(2, 0, value_item)

        gems_max_absolute = max_absolute * 20
        mora_max_absolute = max_absolute * 20000

        value_item = QTableWidgetItem(f"{gems_max_absolute:,} ✦".replace(",", " "))
        value_item.setTextAlignment(Qt.AlignCenter)
        if self.dark_theme:
            value_item.setBackground(QColor(45, 45, 45))
        else:
            value_item.setBackground(QColor(255, 255, 255))
        self.table.setItem(2, 1, value_item)

        value_item = QTableWidgetItem(f"{mora_max_absolute:,} ◎".replace(",", " "))
        value_item.setTextAlignment(Qt.AlignCenter)
        if self.dark_theme:
            value_item.setBackground(QColor(45, 45, 45))
        else:
            value_item.setBackground(QColor(255, 255, 255))
        self.table.setItem(2, 2, value_item)

        self.log("fill_table: completed")

    def fill_percent_table(self):
        """Заполняет вторую таблицу (проценты)"""
        self.log("fill_percent_table: started")

        percent_owned = self.stats["percent_owned"]
        percent_absolute = self.stats["percent_absolute"]
        limit_percent = self.stats["limit_percent"]

        for col in range(2):
            item = QTableWidgetItem("")
            item.setTextAlignment(Qt.AlignCenter)
            if self.dark_theme:
                item.setBackground(QColor(45, 45, 45))
            else:
                item.setBackground(QColor(255, 255, 255))
            self.percent_table.setItem(0, col, item)

        item = QTableWidgetItem(f"{percent_owned}%")
        item.setTextAlignment(Qt.AlignCenter)
        if self.dark_theme:
            item.setBackground(QColor(45, 45, 45))
        else:
            item.setBackground(QColor(255, 255, 255))
        self.percent_table.setItem(0, 0, item)

        item = QTableWidgetItem(f"{percent_absolute}% / {limit_percent}%")
        item.setTextAlignment(Qt.AlignCenter)
        if self.dark_theme:
            item.setBackground(QColor(45, 45, 45))
        else:
            item.setBackground(QColor(255, 255, 255))
        self.percent_table.setItem(0, 1, item)

        self.log("fill_percent_table: completed")
