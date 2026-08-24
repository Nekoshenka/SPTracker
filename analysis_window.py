"""
Окно анализа наборов
"""

from datetime import datetime

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QScrollArea
)
from PySide6.QtCore import Qt

from locales import get_text


class AnalysisWindow(QDialog):
    """Окно анализа наборов"""

    def __init__(self, parent=None, game_data=None, account_data=None, lang="en", dark_theme=True):
        super().__init__(parent)
        self.parent_window = parent
        self.game_data = game_data
        self.account_data = account_data
        self.current_lang = lang
        self.dark_theme = dark_theme

        self.analysis_results = []

        self.init_ui()
        self.calculate_analysis()
        self.fill_table()
        self.update_theme()

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] AnalysisWindow: {message}")

    def init_ui(self):
        """Настройка интерфейса"""
        self.log("init_ui: started")
        self.setModal(True)
        self.setWindowTitle(get_text("analysis_title", self.current_lang))
        self.setFixedSize(700, 500)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        self.title_label = QLabel(get_text("analysis_title", self.current_lang))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(self.title_label)

        self.info_label = QLabel(
            get_text("analysis_account_info", self.current_lang).format(
                self.account_data.get("account_name", "Unknown")
            )
        )
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-size: 14px;")
        main_layout.addWidget(self.info_label)

        self.hint_label = QLabel(get_text("analysis_hint", self.current_lang))
        self.hint_label.setAlignment(Qt.AlignCenter)
        self.hint_label.setStyleSheet("font-size: 12px; font-style: italic;")
        main_layout.addWidget(self.hint_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

        self.table.setHorizontalHeaderLabels([
            get_text("analysis_col_set", self.current_lang),
            get_text("analysis_col_value", self.current_lang)
        ])

        scroll_area.setWidget(self.table)
        main_layout.addWidget(scroll_area)

        self.close_btn = QPushButton(get_text("analysis_btn_close", self.current_lang))
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
            QTableWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444444;
                border-radius: 4px;
                gridline-color: #444444;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QHeaderView::section {
                background-color: #3d3d3d;
                color: #e0e0e0;
                border: 1px solid #444444;
                padding: 8px;
                font-weight: bold;
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
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #555555;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #777777;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #e0e0e0;")
        self.info_label.setStyleSheet("font-size: 14px; color: #999999;")
        self.hint_label.setStyleSheet("font-size: 12px; color: #777777; font-style: italic;")
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
            QTableWidget {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 4px;
                gridline-color: #cccccc;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QHeaderView::section {
                background-color: #e8e8e8;
                color: #333333;
                border: 1px solid #cccccc;
                padding: 8px;
                font-weight: bold;
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
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #e0e0e0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #cccccc;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #aaaaaa;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333333;")
        self.info_label.setStyleSheet("font-size: 14px; color: #666666;")
        self.hint_label.setStyleSheet("font-size: 12px; color: #888888; font-style: italic;")
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
        """)

    def calculate_analysis(self):
        """Вычисляет анализ наборов"""
        self.log("calculate_analysis: started")

        sets_data = self.game_data.get("sets", {})
        owned_ids = self.account_data.get("owned_characters", [])
        progress = self.account_data.get("progress", [])

        existing_progress = set()
        for entry in progress:
            char_id = entry.get("character_id")
            set_id = entry.get("set_id")
            if char_id and set_id:
                existing_progress.add((char_id, set_id))

        analysis_results = []

        for set_id, set_data in sets_data.items():
            liked_by = set_data.get("liked_by", [])

            owned_liked = [char_id for char_id in liked_by if char_id in owned_ids]

            value = 0
            has_any_progress = False

            for char_id in owned_liked:
                if (char_id, set_id) not in existing_progress:
                    value += 1
                else:
                    has_any_progress = True

            if value > 0:
                set_name = set_data.get(self.current_lang, set_id)
                analysis_results.append({
                    "set_id": set_id,
                    "set_name": set_name,
                    "value": value,
                    "has_progress": has_any_progress
                })

        analysis_results.sort(
            key=lambda x: (not x["has_progress"], -x["value"])
        )

        self.analysis_results = analysis_results
        self.log(f"  found {len(analysis_results)} sets with value > 0")
        self.log("calculate_analysis: completed")

    def fill_table(self):
        """Заполняет таблицу"""
        self.log("fill_table: started")

        results = self.analysis_results
        self.table.setRowCount(len(results))

        for row, result in enumerate(results):
            set_name_item = QTableWidgetItem(result["set_name"])
            set_name_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, set_name_item)

            value_item = QTableWidgetItem(str(result["value"]))
            value_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, value_item)

            if result["has_progress"]:
                for col in range(2):
                    item = self.table.item(row, col)
                    if item:
                        item.setBackground(Qt.darkGreen)
                        item.setForeground(Qt.white)

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        self.log("fill_table: completed")
