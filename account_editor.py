"""
Окно создания/редактирования аккаунта
"""

import os
import json
from datetime import datetime

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QScrollArea, QWidget,
    QCheckBox, QMessageBox, QFrame
)

from locales import get_text


class AccountEditor(QDialog):
    """Окно редактирования аккаунта (модальное)"""

    def __init__(self, parent=None, game_data=None, account_data=None, lang="en", accounts_dir=None, dark_theme=True):
        super().__init__(parent)
        self.parent_window = parent
        self.game_data = game_data
        self.account_data = account_data
        self.current_lang = lang
        self.accounts_dir = accounts_dir
        self.dark_theme = dark_theme
        self.current_file_path = None

        self.character_checkboxes = {}

        self.init_ui()
        self.load_data()
        self.update_theme()

    def log(self, message):
        """Вывод отладочного сообщения"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] AccountEditor: {message}")

    def init_ui(self):
        """Настройка интерфейса"""
        self.setModal(True)

        if self.account_data is None:
            self.setWindowTitle(get_text("editor_title_create", self.current_lang))
        else:
            self.setWindowTitle(get_text("editor_title_edit", self.current_lang))

        self.setFixedSize(400, 600)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        name_layout = QVBoxLayout()
        name_label = QLabel(get_text("editor_account_name", self.current_lang))
        name_label.setStyleSheet("font-weight: bold;")
        name_layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(get_text("editor_name_placeholder", self.current_lang))
        self.name_input.setMinimumHeight(35)
        name_layout.addWidget(self.name_input)

        main_layout.addLayout(name_layout)

        chars_header = QHBoxLayout()
        chars_label = QLabel(get_text("editor_characters_list", self.current_lang))
        chars_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        chars_header.addWidget(chars_label)
        chars_header.addStretch()
        main_layout.addLayout(chars_header)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        self.btn_select_all = QPushButton("✅ " + get_text("editor_select_all", self.current_lang))
        self.btn_select_all.setMinimumHeight(32)
        self.btn_select_all.clicked.connect(self.select_all_characters)
        buttons_layout.addWidget(self.btn_select_all)

        self.btn_deselect_all = QPushButton("❌ " + get_text("editor_deselect_all", self.current_lang))
        self.btn_deselect_all.setMinimumHeight(32)
        self.btn_deselect_all.clicked.connect(self.deselect_all_characters)
        buttons_layout.addWidget(self.btn_deselect_all)

        main_layout.addLayout(buttons_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        self.scroll_content = QWidget()
        scroll_layout = QVBoxLayout(self.scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(3)

        characters = self.game_data.get("characters", {})

        char_list = []
        for char_id, char_data in characters.items():
            name = char_data.get(self.current_lang, char_id)
            char_list.append((name, char_id, char_data))

        char_list.sort(key=lambda x: x[0].lower())

        for name, char_id, char_data in char_list:
            checkbox = QCheckBox(name)
            checkbox.setProperty("char_id", char_id)
            checkbox.setMinimumHeight(35)
            scroll_layout.addWidget(checkbox)
            self.character_checkboxes[char_id] = checkbox

        scroll_layout.addStretch()
        scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(scroll_area)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        self.btn_save = QPushButton(get_text("editor_btn_save", self.current_lang))
        self.btn_save.setMinimumHeight(40)
        self.btn_save.clicked.connect(self.save_account)

        self.btn_cancel = QPushButton(get_text("editor_btn_cancel", self.current_lang))
        self.btn_cancel.setMinimumHeight(40)
        self.btn_cancel.clicked.connect(self.reject)

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_save)
        buttons_layout.addWidget(self.btn_cancel)

        main_layout.addLayout(buttons_layout)

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
            QScrollArea {
                background-color: #1e1e1e;
                border: none;
            }
            QScrollArea > QWidget > QWidget {
                background-color: #1e1e1e;
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
            QCheckBox {
                color: #e0e0e0;
                font-size: 13px;
                spacing: 8px;
                padding: 4px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #2d2d2d;
                border: 2px solid #555555;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border: 2px solid #4CAF50;
                border-radius: 3px;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #777777;
            }
            QPushButton {
                font-weight: bold;
                border: none;
                border-radius: 4px;
                padding: 8px 25px;
                font-size: 14px;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #555555;
                border: 1px solid #3d3d3d;
            }
        """)

        self.btn_select_all.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)

        self.btn_deselect_all.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
            QPushButton:pressed {
                background-color: #9a0007;
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
        """)

        self.btn_cancel.setStyleSheet("""
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
            QScrollArea {
                background-color: #f0f0f0;
                border: none;
            }
            QScrollArea > QWidget > QWidget {
                background-color: #f0f0f0;
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
            QCheckBox {
                color: #333333;
                font-size: 13px;
                spacing: 8px;
                padding: 4px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #ffffff;
                border: 2px solid #cccccc;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border: 2px solid #4CAF50;
                border-radius: 3px;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #aaaaaa;
            }
            QPushButton {
                font-weight: bold;
                border: none;
                border-radius: 4px;
                padding: 8px 25px;
                font-size: 14px;
            }
            QPushButton:disabled {
                background-color: #e8e8e8;
                color: #999999;
                border: 1px solid #dddddd;
            }
        """)

        self.btn_select_all.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)

        self.btn_deselect_all.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
            QPushButton:pressed {
                background-color: #9a0007;
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
        """)

        self.btn_cancel.setStyleSheet("""
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
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)

    def load_data(self):
        """Загружает данные аккаунта в поля (для редактирования)"""
        if self.account_data is None:
            return

        name = self.account_data.get("account_name", "")
        self.name_input.setText(name)

        owned = self.account_data.get("owned_characters", [])
        for char_id, checkbox in self.character_checkboxes.items():
            if char_id in owned:
                checkbox.setChecked(True)

        if self.accounts_dir and self.account_data:
            account_name = self.account_data.get("account_name", "").lower()
            safe_name = ''.join(c for c in account_name if c.isalnum() or c in (' ', '-', '_'))
            safe_name = safe_name.replace(' ', '_')

            if os.path.exists(self.accounts_dir):
                for f in os.listdir(self.accounts_dir):
                    if f.startswith(f"account_{safe_name}") and f.endswith(".json"):
                        self.current_file_path = os.path.join(self.accounts_dir, f)
                        break

    def select_all_characters(self):
        """Отмечает всех персонажей"""
        self.log("select_all_characters: called")
        for checkbox in self.character_checkboxes.values():
            checkbox.setChecked(True)

    def deselect_all_characters(self):
        """Снимает отметки со всех персонажей"""
        self.log("deselect_all_characters: called")
        for checkbox in self.character_checkboxes.values():
            checkbox.setChecked(False)

    def get_characters_with_progress(self):
        """Возвращает множество ID персонажей, у которых есть прогресс"""
        if self.account_data is None:
            return set()

        progress = self.account_data.get("progress", [])
        return {entry.get("character_id") for entry in progress if entry.get("character_id")}

    def save_account(self):
        """Сохраняет аккаунт (создаёт или перезаписывает)"""
        name = self.name_input.text().strip()
        if not name:
            self.show_warning(get_text("error_empty_name", self.current_lang))
            return

        new_owned = set()
        for char_id, checkbox in self.character_checkboxes.items():
            if checkbox.isChecked():
                new_owned.add(char_id)

        if not new_owned:
            self.show_warning(get_text("error_no_characters", self.current_lang))
            return

        if self.account_data is not None:
            chars_with_progress = self.get_characters_with_progress()
            old_owned = set(self.account_data.get("owned_characters", []))

            removed_with_progress = (old_owned - new_owned) & chars_with_progress

            if removed_with_progress:
                characters_data = self.game_data.get("characters", {})
                names = []
                for char_id in removed_with_progress:
                    char_data = characters_data.get(char_id, {})
                    name_localized = char_data.get(self.current_lang, char_id)
                    names.append(name_localized)

                self.show_warning(
                    get_text("error_cannot_remove_characters", self.current_lang).format(
                        ", ".join(names)
                    )
                )
                return

        if self.account_data is not None:
            progress = self.account_data.get("progress", [])
        else:
            progress = []

        account_data = {
            "account_name": name,
            "owned_characters": list(new_owned),
            "progress": progress
        }

        safe_name = name.lower()
        safe_name = ''.join(c for c in safe_name if c.isalnum() or c in (' ', '-', '_'))
        safe_name = safe_name.replace(' ', '_')

        if not safe_name:
            safe_name = "account"

        if self.accounts_dir is None:
            self.show_error(get_text("error_accounts_dir_not_set", self.current_lang))
            return

        if not os.path.exists(self.accounts_dir):
            try:
                os.makedirs(self.accounts_dir)
            except Exception as e:
                self.show_error(f"{get_text('error_accounts_dir_create', self.current_lang)}\n{str(e)}")
                return

        if self.account_data is not None and self.current_file_path:
            file_path = self.current_file_path

            old_name = self.account_data.get("account_name", "").lower()
            old_safe_name = ''.join(c for c in old_name if c.isalnum() or c in (' ', '-', '_'))
            old_safe_name = old_safe_name.replace(' ', '_')

            if old_safe_name != safe_name:
                new_file_path = os.path.join(self.accounts_dir, f"account_{safe_name}.json")
                if os.path.exists(new_file_path) and new_file_path != file_path:
                    counter = 1
                    while os.path.exists(new_file_path):
                        new_file_path = os.path.join(self.accounts_dir, f"account_{safe_name}_{counter}.json")
                        counter += 1
                try:
                    os.rename(file_path, new_file_path)
                    file_path = new_file_path
                except Exception as e:
                    self.show_error(f"{get_text('error_file_rename', self.current_lang)}\n{str(e)}")
                    return
        else:
            file_path = os.path.join(self.accounts_dir, f"account_{safe_name}.json")
            counter = 1
            while os.path.exists(file_path):
                file_path = os.path.join(self.accounts_dir, f"account_{safe_name}_{counter}.json")
                counter += 1

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(account_data, f, ensure_ascii=False, indent=2)

            self.show_success(get_text("success_saved", self.current_lang).format(name))
            self.accept()

        except Exception as e:
            self.show_error(f"{get_text('error_save_failed', self.current_lang)}\n{str(e)}")

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

    def show_warning(self, text):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(get_text("error_title", self.current_lang))
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

    def show_success(self, text):
        """Показывает сообщение об успехе без звука"""
        msg = QMessageBox(self)
        msg.setWindowTitle(get_text("success_title", self.current_lang))
        msg.setText(text)
        self._style_message_box(msg)
        msg.exec()

    def closeEvent(self, event):
        event.accept()
