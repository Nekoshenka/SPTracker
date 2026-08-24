"""
Окно внесения/удаления связки персонаж ↔ набор
"""

import sys
import os
import json
from datetime import datetime

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QMessageBox, QFrame,
    QWidget
)
from PySide6.QtCore import Qt, Signal

from locales import get_text
from character_selector import CharacterSelector
from set_selector import SetSelector


class ProgressEditor(QDialog):
    """Окно внесения/удаления связки"""

    progress_added = Signal(dict)
    progress_removed = Signal(dict)

    def __init__(self, parent=None, game_data=None, account_data=None, lang="en", dark_theme=True):
        super().__init__(parent)
        self.parent_window = parent
        self.game_data = game_data
        self.account_data = account_data
        self.current_lang = lang
        self.dark_theme = dark_theme

        self.selected_character_id = None
        self.selected_character_name = None
        self.selected_set_id = None
        self.selected_set_name = None

        self.owned_characters = []
        self.available_sets = []
        self.characters_sets = {}
        self.sets_characters = {}

        self.selection_order = None

        self.is_existing_progress = False

        self.init_ui()
        self.load_data()
        self.update_ui_state()
        self.update_theme()

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] ProgressEditor: {message}")

    def init_ui(self):
        """Настройка интерфейса"""
        self.log("init_ui: started")
        self.setModal(True)
        self.setWindowTitle(get_text("progress_title", self.current_lang))
        self.setFixedSize(600, 400)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        self.info_label = QLabel(
            get_text("progress_account_info", self.current_lang).format(
                self.account_data.get("account_name", "Unknown")
            )
        )
        self.info_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.info_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.info_label)

        char_frame = QFrame()
        char_frame.setFrameShape(QFrame.StyledPanel)
        char_layout = QHBoxLayout(char_frame)
        char_layout.setContentsMargins(10, 10, 10, 10)

        char_icon = QLabel("👤")
        char_icon.setStyleSheet("font-size: 18px;")
        char_layout.addWidget(char_icon)

        self.char_label = QLabel(get_text("progress_character", self.current_lang))
        self.char_label.setStyleSheet("font-weight: bold;")
        char_layout.addWidget(self.char_label)

        self.char_display = QLineEdit()
        self.char_display.setPlaceholderText(get_text("progress_char_placeholder", self.current_lang))
        self.char_display.setReadOnly(True)
        char_layout.addWidget(self.char_display)

        self.char_select_btn = QPushButton("📋")
        self.char_select_btn.setFixedSize(35, 35)
        self.char_select_btn.setToolTip(get_text("select_character", self.current_lang))
        self.char_select_btn.clicked.connect(self.select_character)
        char_layout.addWidget(self.char_select_btn)

        self.char_clear_btn = QPushButton("✕")
        self.char_clear_btn.setFixedSize(35, 35)
        self.char_clear_btn.setToolTip(get_text("clear_field", self.current_lang))
        self.char_clear_btn.clicked.connect(self.clear_character)
        self.char_clear_btn.setVisible(False)
        char_layout.addWidget(self.char_clear_btn)

        main_layout.addWidget(char_frame)

        set_frame = QFrame()
        set_frame.setFrameShape(QFrame.StyledPanel)
        set_layout = QHBoxLayout(set_frame)
        set_layout.setContentsMargins(10, 10, 10, 10)

        set_icon = QLabel("📦")
        set_icon.setStyleSheet("font-size: 18px;")
        set_layout.addWidget(set_icon)

        self.set_label = QLabel(get_text("progress_set", self.current_lang))
        self.set_label.setStyleSheet("font-weight: bold;")
        set_layout.addWidget(self.set_label)

        self.set_display = QLineEdit()
        self.set_display.setPlaceholderText(get_text("progress_set_placeholder", self.current_lang))
        self.set_display.setReadOnly(True)
        set_layout.addWidget(self.set_display)

        self.set_select_btn = QPushButton("📋")
        self.set_select_btn.setFixedSize(35, 35)
        self.set_select_btn.setToolTip(get_text("select_set", self.current_lang))
        self.set_select_btn.clicked.connect(self.select_set)
        set_layout.addWidget(self.set_select_btn)

        self.set_clear_btn = QPushButton("✕")
        self.set_clear_btn.setFixedSize(35, 35)
        self.set_clear_btn.setToolTip(get_text("clear_field", self.current_lang))
        self.set_clear_btn.clicked.connect(self.clear_set)
        self.set_clear_btn.setVisible(False)
        set_layout.addWidget(self.set_clear_btn)

        main_layout.addWidget(set_frame)

        actions_frame = QWidget()
        actions_layout = QHBoxLayout(actions_frame)
        actions_layout.setContentsMargins(0, 10, 0, 0)
        actions_layout.setSpacing(15)

        self.btn_save = QPushButton("✅ " + get_text("progress_btn_save", self.current_lang))
        self.btn_save.setMinimumHeight(40)
        self.btn_save.clicked.connect(self.save_progress)
        self.btn_save.setEnabled(False)

        self.btn_clear = QPushButton("🗑️ " + get_text("clear_all", self.current_lang))
        self.btn_clear.setMinimumHeight(40)
        self.btn_clear.clicked.connect(self.clear_all)
        self.btn_clear.setEnabled(False)

        actions_layout.addWidget(self.btn_save)
        actions_layout.addWidget(self.btn_clear)

        main_layout.addWidget(actions_frame)

        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: #999999; font-style: italic;")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

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
                border-radius: 6px;
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
            QLineEdit:disabled {
                background-color: #3d3d3d;
                color: #999999;
            }
            QPushButton {
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 25px;
            }
            QPushButton:disabled {
                background-color: #444444;
                color: #777777;
            }
        """)

        for btn in [self.char_select_btn, self.set_select_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3d3d3d;
                    color: #e0e0e0;
                    border: 1px solid #555555;
                    border-radius: 4px;
                    font-size: 16px;
                    padding: 0px;
                    margin: 0px;
                }
                QPushButton:hover {
                    background-color: #4d4d4d;
                }
            """)

        for btn in [self.char_clear_btn, self.set_clear_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #999999;
                    border: none;
                    font-size: 16px;
                    padding: 0px;
                    margin: 0px;
                }
                QPushButton:hover {
                    color: #ff4444;
                }
            """)

        self.btn_clear.setStyleSheet("""
            QPushButton {
                background-color: #3d3d3d;
                color: #e0e0e0;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 8px 25px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #555555;
                border: 1px solid #3d3d3d;
            }
        """)

        self.info_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #e0e0e0;")

        for label in [self.char_label, self.set_label]:
            label.setStyleSheet("font-weight: bold; color: #e0e0e0;")

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
                border-radius: 6px;
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
            QLineEdit:disabled {
                background-color: #f0f0f0;
                color: #999999;
            }
            QPushButton {
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 25px;
            }
            QPushButton:disabled {
                background-color: #e8e8e8;
                color: #999999;
            }
        """)

        for btn in [self.char_select_btn, self.set_select_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    color: #333333;
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    font-size: 16px;
                    padding: 0px;
                    margin: 0px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)

        for btn in [self.char_clear_btn, self.set_clear_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #999999;
                    border: none;
                    font-size: 16px;
                    padding: 0px;
                    margin: 0px;
                }
                QPushButton:hover {
                    color: #ff4444;
                }
            """)

        self.btn_clear.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 8px 25px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:disabled {
                background-color: #e8e8e8;
                color: #999999;
                border: 1px solid #dddddd;
            }
        """)

        self.btn_save.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 25px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #e8e8e8;
                color: #999999;
                border: 1px solid #dddddd;
            }
        """)

        self.info_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #333333;")

        for label in [self.char_label, self.set_label]:
            label.setStyleSheet("font-weight: bold; color: #333333;")

    def load_data(self):
        """Загружает данные из game_data и аккаунта"""
        self.log("load_data: started")
        if not self.game_data or not self.account_data:
            return

        owned_ids = self.account_data.get("owned_characters", [])
        characters = self.game_data.get("characters", {})
        sets = self.game_data.get("sets", {})

        self.owned_characters = []
        for char_id in owned_ids:
            if char_id in characters:
                name = characters[char_id].get(self.current_lang, char_id)
                self.owned_characters.append((char_id, name))
        self.owned_characters.sort(key=lambda x: x[1].lower())

        self.available_sets = []
        for set_id, set_data in sets.items():
            name = set_data.get(self.current_lang, set_id)
            self.available_sets.append((set_id, name))
        self.available_sets.sort(key=lambda x: x[1].lower())

        self.characters_sets = {char_id: [] for char_id in owned_ids}
        self.sets_characters = {}

        for set_id, set_data in sets.items():
            liked_by = set_data.get("liked_by", [])
            self.sets_characters[set_id] = []
            for char_id in liked_by:
                if char_id in owned_ids:
                    self.sets_characters[set_id].append(char_id)
                    if char_id in self.characters_sets:
                        self.characters_sets[char_id].append(set_id)

        self.log("load_data: completed")

    def select_character(self):
        """Открывает окно выбора персонажа"""
        self.log("select_character: called")

        if not self.owned_characters:
            self.show_info(get_text("no_characters", self.current_lang))
            return

        filtered_chars = self.owned_characters
        if self.selected_set_id:
            set_chars = self.sets_characters.get(self.selected_set_id, [])
            if not set_chars:
                self.show_info(get_text("no_characters_for_set", self.current_lang))
                return
            filtered_chars = [(char_id, name) for char_id, name in self.owned_characters
                              if char_id in set_chars]

        selector = CharacterSelector(
            parent=self,
            characters=filtered_chars,
            current_lang=self.current_lang,
            game_data=self.game_data,
            dark_theme=self.dark_theme
        )

        result = selector.exec()
        if result == QDialog.DialogCode.Accepted:
            char_id = selector.get_selected_id()
            if char_id:
                self.selected_character_id = char_id
                self.selected_character_name = selector.get_selected_name()
                self.selection_order = 'character_first'
                self.update_ui_state()
                self.log(f"  selected character: {char_id} -> {self.selected_character_name}")

    def select_set(self):
        """Открывает окно выбора набора"""
        self.log("select_set: called")

        filtered_sets = self.available_sets
        if self.selected_character_id:
            char_sets = self.characters_sets.get(self.selected_character_id, [])
            if not char_sets:
                self.show_info(get_text("progress_no_sets_text", self.current_lang))
                self.clear_character()
                return
            filtered_sets = [(set_id, name) for set_id, name in self.available_sets
                             if set_id in char_sets]

        selector = SetSelector(
            parent=self,
            sets=filtered_sets,
            current_lang=self.current_lang,
            dark_theme=self.dark_theme
        )

        result = selector.exec()
        if result == QDialog.DialogCode.Accepted:
            set_id = selector.get_selected_id()
            if set_id:
                self.selected_set_id = set_id
                self.selected_set_name = selector.get_selected_name()
                self.selection_order = 'set_first'
                self.update_ui_state()
                self.log(f"  selected set: {set_id} -> {self.selected_set_name}")

    def clear_character(self):
        self.log("clear_character: called")
        self.selected_character_id = None
        self.selected_character_name = None
        self.is_existing_progress = False
        if self.selection_order == 'character_first':
            self.selection_order = None
        self.update_ui_state()

    def clear_set(self):
        self.log("clear_set: called")
        self.selected_set_id = None
        self.selected_set_name = None
        self.is_existing_progress = False
        if self.selection_order == 'set_first':
            self.selection_order = None
        self.update_ui_state()

    def clear_all(self):
        """Очищает все поля"""
        self.log("clear_all: called")
        self.selected_character_id = None
        self.selected_character_name = None
        self.selected_set_id = None
        self.selected_set_name = None
        self.selection_order = None
        self.is_existing_progress = False
        self.update_ui_state()

    def update_status(self):
        """Обновляет статусную строку"""
        char_id = self.selected_character_id
        set_id = self.selected_set_id

        self.log(f"update_status: char_id={char_id}, set_id={set_id}")

        if char_id and set_id:
            progress = self.account_data.get("progress", [])
            for entry in progress:
                if entry.get("character_id") == char_id and entry.get("set_id") == set_id:
                    self.status_label.setText(
                        get_text("progress_already_done", self.current_lang)
                    )
                    self.status_label.setStyleSheet("color: #FF9800; font-style: italic;")
                    self.btn_save.setEnabled(False)
                    self.log("  status: already done")
                    return

            self.status_label.setText(
                get_text("progress_ready_to_save", self.current_lang)
            )
            self.status_label.setStyleSheet("color: #4CAF50; font-style: italic;")
            self.btn_save.setEnabled(True)
            self.log("  status: ready to save")
        elif char_id and not set_id:
            self.status_label.setText(
                get_text("progress_select_set", self.current_lang)
            )
            self.status_label.setStyleSheet("color: #999999; font-style: italic;")
            self.btn_save.setEnabled(False)
            self.log("  status: select set")
        elif not char_id and set_id:
            self.status_label.setText(
                get_text("progress_select_character", self.current_lang)
            )
            self.status_label.setStyleSheet("color: #999999; font-style: italic;")
            self.btn_save.setEnabled(False)
            self.log("  status: select character")
        else:
            self.status_label.setText(
                get_text("progress_select_both", self.current_lang)
            )
            self.status_label.setStyleSheet("color: #999999; font-style: italic;")
            self.btn_save.setEnabled(False)
            self.log("  status: select both")

    def update_ui_state(self):
        """Обновляет состояние UI в зависимости от выбранных значений"""
        self.log("update_ui_state: called")

        if self.selected_character_name:
            self.char_display.setText(self.selected_character_name)
            self.char_clear_btn.setVisible(True)
            self.char_select_btn.setText("✅")
        else:
            self.char_display.setText("")
            self.char_clear_btn.setVisible(False)
            self.char_select_btn.setText("📋")

        if self.selected_set_name:
            self.set_display.setText(self.selected_set_name)
            self.set_clear_btn.setVisible(True)
            self.set_select_btn.setText("✅")
        else:
            self.set_display.setText("")
            self.set_clear_btn.setVisible(False)
            self.set_select_btn.setText("📋")

        has_any_selection = self.selected_character_id is not None or self.selected_set_id is not None
        self.btn_clear.setEnabled(has_any_selection)

        self.is_existing_progress = False
        if self.selected_character_id and self.selected_set_id:
            progress = self.account_data.get("progress", [])
            for entry in progress:
                if entry.get("character_id") == self.selected_character_id and entry.get(
                        "set_id") == self.selected_set_id:
                    self.is_existing_progress = True
                    break

        if self.selected_character_id and self.selected_set_id:
            if self.is_existing_progress:
                self.btn_save.setText("🗑️ " + get_text("progress_btn_delete", self.current_lang))
                if self.dark_theme:
                    self.btn_save.setStyleSheet("""
                        QPushButton {
                            font-weight: bold;
                            background-color: #d32f2f;
                            color: white;
                            border: none;
                            border-radius: 4px;
                            padding: 8px 25px;
                            font-size: 14px;
                        }
                        QPushButton:hover {
                            background-color: #b71c1c;
                        }
                        QPushButton:pressed {
                            background-color: #9a0007;
                        }
                        QPushButton:disabled {
                            background-color: #444444;
                            color: #777777;
                        }
                    """)
                else:
                    self.btn_save.setStyleSheet("""
                        QPushButton {
                            font-weight: bold;
                            background-color: #d32f2f;
                            color: white;
                            border: none;
                            border-radius: 4px;
                            padding: 8px 25px;
                            font-size: 14px;
                        }
                        QPushButton:hover {
                            background-color: #b71c1c;
                        }
                        QPushButton:pressed {
                            background-color: #9a0007;
                        }
                        QPushButton:disabled {
                            background-color: #e8e8e8;
                            color: #999999;
                            border: 1px solid #dddddd;
                        }
                    """)
                self.btn_save.setEnabled(True)
                self.status_label.setText(get_text("progress_ready_to_delete", self.current_lang))
                self.status_label.setStyleSheet("color: #FF9800; font-style: italic;")
            else:
                self.btn_save.setText("✅ " + get_text("progress_btn_save", self.current_lang))
                if self.dark_theme:
                    self.btn_save.setStyleSheet("""
                        QPushButton {
                            font-weight: bold;
                            background-color: #4CAF50;
                            color: white;
                            border: none;
                            border-radius: 4px;
                            padding: 8px 25px;
                            font-size: 14px;
                        }
                        QPushButton:hover {
                            background-color: #45a049;
                        }
                        QPushButton:pressed {
                            background-color: #3d8b40;
                        }
                        QPushButton:disabled {
                            background-color: #444444;
                            color: #777777;
                        }
                    """)
                else:
                    self.btn_save.setStyleSheet("""
                        QPushButton {
                            font-weight: bold;
                            background-color: #4CAF50;
                            color: white;
                            border: none;
                            border-radius: 4px;
                            padding: 8px 25px;
                            font-size: 14px;
                        }
                        QPushButton:hover {
                            background-color: #45a049;
                        }
                        QPushButton:pressed {
                            background-color: #3d8b40;
                        }
                        QPushButton:disabled {
                            background-color: #e8e8e8;
                            color: #999999;
                            border: 1px solid #dddddd;
                        }
                    """)
                self.btn_save.setEnabled(True)
                self.status_label.setText(get_text("progress_ready_to_save", self.current_lang))
                self.status_label.setStyleSheet("color: #4CAF50; font-style: italic;")
        else:
            self.btn_save.setText("✅ " + get_text("progress_btn_save", self.current_lang))
            if self.dark_theme:
                self.btn_save.setStyleSheet("""
                    QPushButton {
                        font-weight: bold;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 8px 25px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #45a049;
                    }
                    QPushButton:pressed {
                        background-color: #3d8b40;
                    }
                    QPushButton:disabled {
                        background-color: #444444;
                        color: #777777;
                    }
                """)
            else:
                self.btn_save.setStyleSheet("""
                    QPushButton {
                        font-weight: bold;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 8px 25px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #45a049;
                    }
                    QPushButton:pressed {
                        background-color: #3d8b40;
                    }
                    QPushButton:disabled {
                        background-color: #e8e8e8;
                        color: #999999;
                        border: 1px solid #dddddd;
                    }
                """)
            self.btn_save.setEnabled(False)
            self.status_label.setText(get_text("progress_select_both", self.current_lang))
            self.status_label.setStyleSheet("color: #999999; font-style: italic;")

        self.log("update_ui_state: completed")

    def save_progress(self):
        """Сохраняет или удаляет связку"""
        self.log("save_progress: called")
        if not self.selected_character_id or not self.selected_set_id:
            return

        progress = self.account_data.get("progress", [])

        existing_index = -1
        for i, entry in enumerate(progress):
            if entry.get("character_id") == self.selected_character_id and entry.get("set_id") == self.selected_set_id:
                existing_index = i
                break

        if existing_index >= 0:
            reply = QMessageBox.question(
                self,
                get_text("progress_delete_title", self.current_lang),
                get_text("progress_delete_confirm", self.current_lang).format(
                    self.selected_character_name,
                    self.selected_set_name
                ),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.No:
                self.log("  deletion cancelled by user")
                return

            removed = progress.pop(existing_index)
            self.account_data["progress"] = progress
            self.log(f"  removed: {removed}")

            try:
                self._save_account_file()
                self.progress_removed.emit({
                    "character_id": self.selected_character_id,
                    "set_id": self.selected_set_id
                })
                self.show_success(get_text("progress_delete_success_text", self.current_lang))
                self.update_ui_state()
            except Exception as e:
                self.show_error(get_text("progress_save_error", self.current_lang).format(str(e)))
            return

        progress.append({
            "character_id": self.selected_character_id,
            "set_id": self.selected_set_id
        })
        self.account_data["progress"] = progress

        try:
            self._save_account_file()
            self.progress_added.emit({
                "character_id": self.selected_character_id,
                "set_id": self.selected_set_id
            })
            self.show_success(get_text("progress_success_text", self.current_lang))
            self.update_ui_state()
        except Exception as e:
            self.show_error(get_text("progress_save_error", self.current_lang).format(str(e)))

    def _save_account_file(self):
        """Сохраняет файл аккаунта"""
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        accounts_dir = os.path.join(base_dir, "data", "accounts")

        account_name = self.account_data.get("account_name", "").lower()
        safe_name = ''.join(c for c in account_name if c.isalnum() or c in (' ', '-', '_'))
        safe_name = safe_name.replace(' ', '_')

        file_path = None
        if os.path.exists(accounts_dir):
            for f in os.listdir(accounts_dir):
                if f.startswith(f"account_{safe_name}") and f.endswith(".json"):
                    file_path = os.path.join(accounts_dir, f)
                    break

        if not file_path:
            file_path = os.path.join(accounts_dir, f"account_{safe_name}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.account_data, f, ensure_ascii=False, indent=2)

    def _style_message_box(self, msg):
        """Применяет стиль к QMessageBox в зависимости от темы"""
        if self.dark_theme:
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #1e1e1e;
                }
                QMessageBox QLabel {
                    color: #e0e0e0;
                }
                QMessageBox QPushButton {
                    background-color: #3d3d3d;
                    color: #e0e0e0;
                    border: 1px solid #555555;
                    border-radius: 4px;
                    padding: 5px 15px;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #4d4d4d;
                }
            """)
        else:
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #f0f0f0;
                }
                QMessageBox QLabel {
                    color: #333333;
                }
                QMessageBox QPushButton {
                    background-color: #f0f0f0;
                    color: #333333;
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    padding: 5px 15px;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)

    def show_info(self, text):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(get_text("info_title", self.current_lang))
        msg.setText(text)
        self._style_message_box(msg)
        msg.exec()

    def show_success(self, text):
        """Показывает сообщение об успехе"""
        msg = QMessageBox(self)
        msg.setWindowTitle(get_text("success_title", self.current_lang))
        msg.setText(text)
        self._style_message_box(msg)
        msg.exec()

    def show_error(self, text):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(get_text("error_title", self.current_lang))
        msg.setText(text)
        self._style_message_box(msg)
        msg.exec()

    def closeEvent(self, event):
        self.log("closeEvent: called")
        event.accept()

    def reject(self):
        self.log("reject: called")
        super().reject()

    def accept(self):
        self.log("accept: called")
        super().accept()
