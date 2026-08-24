"""
Файл локализации интерфейса
Поддерживаемые языки: en (по умолчанию), ru
"""

LOCALES = {
    "en": {
        "window_title": "Serenitea Pot Tracker",

        "no_account": "(select account)",
        "open_folder_tooltip": "Open data folder",

        "btn_create_account": "Create Account",
        "btn_edit_account": "Edit Account",
        "btn_add_progress": "Progress",
        "btn_statistics": "Statistics",
        "btn_exit": "Exit",

        "msg_create_account": "Create Account",
        "msg_edit_account": "Edit Account",
        "msg_add_progress": "Progress",
        "msg_statistics": "Statistics",
        "msg_lang_switched": "Language switched to EN",

        "error_critical": "A critical error occurred.\nThe application will be closed.",
        "error_folder_fail": "Failed to open folder",
        "error_folder_create": "Failed to create data/ folder",
        "error_window_title": "Critical Error",

        "no_accounts": "(no accounts)",
        "refresh_tooltip": "Refresh account list",
        "refresh_done": "Accounts updated. Found {} account(s).",

        "editor_title_create": "Create Account",
        "editor_title_edit": "Edit Account",
        "editor_account_name": "Account Name:",
        "editor_name_placeholder": "Enter account name...",
        "editor_characters_list": "Your Characters:",
        "editor_btn_save": "Save",
        "editor_btn_cancel": "Cancel",

        "error_title": "Error",
        "error_empty_name": "Account name cannot be empty!",
        "error_no_characters": "Select at least one character!",
        "error_save_failed": "Failed to save account!",
        "success_title": "Success",
        "success_saved": "Account '{}' saved successfully!",

        "progress_title": "Progress",
        "progress_account_info": "Account: {}",
        "progress_character": "Character:",
        "progress_char_placeholder": "Select or search character...",
        "progress_set": "Set:",
        "progress_set_placeholder": "Select or search set...",
        "progress_btn_save": "Save",
        "progress_btn_cancel": "Cancel",
        "info_title": "Warning!",

        "progress_no_sets_title": "No Favorite Sets",
        "progress_no_sets_text": "This character has no favorite sets yet.\nPlease check back in a future update!",
        "progress_no_sets_placeholder": "No sets available",
        "progress_ready_to_save": "Ready to save this progress!",
        "progress_select_set": "Select a set",
        "progress_select_character": "Select a character",
        "progress_select_both": "Select character and set",
        "progress_already_done": "This progress has already been saved!",
        "progress_warning_title": "Warning",
        "progress_warning_duplicate": "This progress has already been saved!",
        "progress_success_title": "Success",
        "progress_success_text": "Progress saved successfully!",
        "progress_save_error": "Error saving progress: {}",
        "no_items": "No items found",

        "select_character": "Select Character",
        "select_character_title": "Select Character",
        "search_character": "Search character...",
        "no_characters_found": "No characters found",
        "select_set": "Select Set",
        "select_set_title": "Select Set",
        "search_set": "Search set...",
        "no_sets_found": "No sets found",
        "found_count": "Found: {}",
        "no_characters": "You don't have any characters!",
        "confirm_selection": "Confirm Selection",
        "clear_field": "Clear field",
        "clear_all": "Clear all",

        "editor_select_all": "Select All",
        "editor_deselect_all": "Deselect All",

        "no_account_selected": "No Account Selected",
        "select_or_create_account": "Select or create an account to get started",
        "account_loaded": "Account loaded successfully",
        "stat_characters": "Characters",
        "stat_progress": "Progress",
        "stat_sets": "Sets",

        "app_title": "Serenitea Pot Tracker",
        "theme_tooltip": "Toggle theme",
        "theme_switched": "Theme switched",

        "btn_analysis": "Analysis of sets",
        "msg_analysis": "Analysis of sets (coming soon!)",

        "no_characters_for_set": "No characters like this set!",

        "tooltip_select_account_first": "Please select an account first",

        "progress_btn_delete": "Delete Progress",
        "progress_ready_to_delete": "Click to delete this progress",
        "progress_delete_title": "Delete Progress",
        "progress_delete_confirm": "Are you sure you want to delete the progress for:\n\n{} → {}?\n\nThis action cannot be undone!",
        "progress_delete_success_title": "Deleted",
        "progress_delete_success_text": "Progress deleted successfully!",

        "statistics_title": "Statistics",
        "statistics_account_info": "Account: {}",
        "stat_col_sets": "Sets",
        "stat_col_gems": "Primogems",
        "stat_col_mora": "Mora",
        "stat_row_obtained": "Obtained",
        "stat_row_max_owned": "Max from owned",
        "stat_row_max_absolute": "Absolute max",
        "stat_btn_close": "Close",

        "stat_percent_limit": "Absolute (done/limit (due to characters count))",
        "stat_percent_title": "Progress Percentage",
        "stat_percent_owned": "From Owned",
        "stat_percent_absolute": "Absolute Max",
        "stat_percent_progress": "Progress",

        "analysis_title": "Analysis of sets",
        "analysis_account_info": "Account: {}",
        "analysis_hint": "Value is a number that represents how many gifts a given set can bring.\nThe sets that previously gave gifts are highlighted in green, which means they are already done and can be used.",
        "analysis_col_set": "Set Name",
        "analysis_col_value": "Value",
        "analysis_btn_close": "Close",

        "error_cannot_remove_characters": "Cannot remove characters with existing progress:\n{}",

        "error_data_folder_not_found": "data/ folder not found!\n\nPlease make sure the data/ folder is located next to the application.\n\nExpected path: {}\n\nThe application will be closed.",
        "error_game_data_not_found": "game_data_v*.json file not found!\n\nPlease make sure the game database file is located in the data/ folder.\n\nExpected path: {}\n\nThe application will be closed.",
        "error_game_data_no_characters": "File {} has invalid structure:\nMissing 'characters' field.\n\nThe application will be closed.",
        "error_game_data_no_sets": "File {} has invalid structure:\nMissing 'sets' field.\n\nThe application will be closed.",
        "error_game_data_json_parse": "JSON parsing error in file {}:\n\n{}\n\nPlease check the file integrity.\n\nThe application will be closed.",
        "error_game_data_load": "Error loading {}:\n\n{}\n\nThe application will be closed.",

        "error_no_account_selected": "No account selected!",
        "error_data_not_loaded": "Game data not loaded!",
        "error_account_not_found": "Selected account not found in list!",

        "info_game_data_loaded": "Loaded game_data version {} from file {}",

        "error_accounts_dir_not_set": "Accounts folder path is not set!",
        "error_accounts_dir_create": "Failed to create accounts folder:",
        "error_file_rename": "Failed to rename file:",
    },
    "ru": {
        "window_title": "Трекер Чайника Безмятежности",

        "no_account": "(выберите аккаунт)",
        "open_folder_tooltip": "Открыть папку data/",

        "btn_create_account": "Создание аккаунта",
        "btn_edit_account": "Редактирование аккаунта",
        "btn_add_progress": "Прогресс",
        "btn_statistics": "Статистика",
        "btn_exit": "Выход",

        "msg_create_account": "Создание аккаунта",
        "msg_edit_account": "Редактирование аккаунта",
        "msg_add_progress": "Прогресс",
        "msg_statistics": "Статистика",
        "msg_lang_switched": "Язык переключен на RU",

        "error_critical": "Произошла критическая ошибка.\nПриложение будет закрыто.",
        "error_folder_fail": "Не удалось открыть папку",
        "error_folder_create": "Не удалось создать папку data/",
        "error_window_title": "Критическая ошибка",

        "no_accounts": "(нет аккаунтов)",
        "refresh_tooltip": "Обновить список аккаунтов",
        "refresh_done": "Список обновлён. Найдено аккаунтов: {}.",

        "editor_title_create": "Создание аккаунта",
        "editor_title_edit": "Редактирование аккаунта",
        "editor_account_name": "Имя аккаунта:",
        "editor_name_placeholder": "Введите имя аккаунта...",
        "editor_characters_list": "Ваши персонажи:",
        "editor_btn_save": "Сохранить",
        "editor_btn_cancel": "Отмена",

        "error_title": "Ошибка",
        "error_empty_name": "Имя аккаунта не может быть пустым!",
        "error_no_characters": "Выберите хотя бы одного персонажа!",
        "error_save_failed": "Не удалось сохранить аккаунт!",
        "success_title": "Успех",
        "success_saved": "Аккаунт '{}' успешно сохранён!",

        "progress_title": "Прогресс",
        "progress_account_info": "Аккаунт: {}",
        "progress_character": "Персонаж:",
        "progress_char_placeholder": "Выберите или найдите персонажа...",
        "progress_set": "Набор:",
        "progress_set_placeholder": "Выберите или найдите набор...",
        "progress_btn_save": "Сохранить",
        "progress_btn_cancel": "Отмена",
        "info_title": "Внимание!",

        "progress_no_sets_title": "Нет любимых наборов",
        "progress_no_sets_text": "У этого персонажа пока нет любимых наборов.\nПопробуйте снова в новой версии!",
        "progress_no_sets_placeholder": "Нет доступных наборов",
        "progress_ready_to_save": "Готово к сохранению!",
        "progress_select_set": "Выберите набор",
        "progress_select_character": "Выберите персонажа",
        "progress_select_both": "Выберите персонажа и набор",
        "progress_already_done": "Этот прогресс уже внесён!",
        "progress_warning_title": "Предупреждение",
        "progress_warning_duplicate": "Этот прогресс уже внесён!",
        "progress_success_title": "Успех",
        "progress_success_text": "Прогресс успешно сохранён!",
        "progress_save_error": "Ошибка сохранения прогресса: {}",
        "no_items": "Ничего не найдено",

        "select_character": "Выбрать персонажа",
        "select_character_title": "Выбор персонажа",
        "search_character": "Поиск персонажа...",
        "no_characters_found": "Персонажи не найдены",
        "select_set": "Выбрать набор",
        "select_set_title": "Выбор набора",
        "search_set": "Поиск набора...",
        "no_sets_found": "Наборы не найдены",
        "found_count": "Найдено: {}",
        "no_characters": "У вас нет персонажей!",
        "confirm_selection": "Подтвердить выбор",
        "clear_field": "Очистить поле",
        "clear_all": "Очистить всё",

        "editor_select_all": "Выбрать всех",
        "editor_deselect_all": "Убрать всех",

        "no_account_selected": "Аккаунт не выбран",
        "select_or_create_account": "Выберите или создайте аккаунт чтобы начать",
        "account_loaded": "Аккаунт успешно загружен",
        "stat_characters": "Персонажей",
        "stat_progress": "Связок",
        "stat_sets": "Наборов",

        "app_title": "Трекер Чайника Безмятежности",
        "theme_tooltip": "Сменить тему",
        "theme_switched": "Тема изменена",

        "btn_analysis": "Анализ наборов",
        "msg_analysis": "Анализ наборов (скоро!)",

        "no_characters_for_set": "Нет персонажей, которым нравится этот набор!",

        "tooltip_select_account_first": "Сначала выберите аккаунт",

        "progress_btn_delete": "Удалить прогресс",
        "progress_ready_to_delete": "Нажмите для удаления этого прогресса",
        "progress_delete_title": "Удаление прогресса",
        "progress_delete_confirm": "Вы уверены, что хотите удалить прогресс:\n\n{} → {}?\n\nЭто действие будет неотменимо!",
        "progress_delete_success_title": "Удалено",
        "progress_delete_success_text": "Прогресс успешно удалён!",

        "statistics_title": "Статистика",
        "statistics_account_info": "Аккаунт: {}",
        "stat_col_sets": "Подарков за наборы",
        "stat_col_gems": "Камней истока",
        "stat_col_mora": "Моры",
        "stat_row_obtained": "Получено",
        "stat_row_max_owned": "Максимум из имеющихся",
        "stat_row_max_absolute": "Абсолютный максимум",
        "stat_btn_close": "Закрыть",

        "stat_percent_limit": "Абсолютный (выполнено/предел(из-за количества персонажей))",
        "stat_percent_title": "Процент выполнения",
        "stat_percent_owned": "Из имеющихся",
        "stat_percent_absolute": "Абсолютный максимум",
        "stat_percent_progress": "Процент выполнения",

        "analysis_title": "Анализ наборов",
        "analysis_account_info": "Аккаунт: {}",
        "analysis_hint": "Ценность - это число, отображающее, сколько подарков может принести данный набор.\nЗелёным выделены наборы, которые ранее давали подарки вашим персонажам, то есть они уже имеются.",
        "analysis_col_set": "Название набора",
        "analysis_col_value": "Ценность",
        "analysis_btn_close": "Закрыть",

        "error_cannot_remove_characters": "Нельзя убрать персонажей с существующим прогрессом:\n{}",

        "error_data_folder_not_found": "Папка data/ не найдена!\n\nПожалуйста, убедитесь, что папка data/ находится рядом с приложением.\n\nОжидаемый путь: {}\n\nПриложение будет закрыто.",
        "error_game_data_not_found": "Файл game_data_v*.json не найден!\n\nПожалуйста, убедитесь, что файл с базой данных игры находится в папке data/.\n\nОжидаемый путь: {}\n\nПриложение будет закрыто.",
        "error_game_data_no_characters": "Файл {} имеет неверную структуру:\nОтсутствует поле 'characters'.\n\nПриложение будет закрыто.",
        "error_game_data_no_sets": "Файл {} имеет неверную структуру:\nОтсутствует поле 'sets'.\n\nПриложение будет закрыто.",
        "error_game_data_json_parse": "Ошибка парсинга JSON в файле {}:\n\n{}\n\nПожалуйста, проверьте целостность файла.\n\nПриложение будет закрыто.",
        "error_game_data_load": "Ошибка загрузки {}:\n\n{}\n\nПриложение будет закрыто.",

        "error_no_account_selected": "Аккаунт не выбран!",
        "error_data_not_loaded": "Данные игры не загружены!",
        "error_account_not_found": "Выбранный аккаунт не найден в списке!",

        "info_game_data_loaded": "Загружена game_data версии {} из файла {}",

        "error_accounts_dir_not_set": "Путь к папке accounts/ не указан!",
        "error_accounts_dir_create": "Не удалось создать папку accounts/:",
        "error_file_rename": "Не удалось переименовать файл:",
    }
}


def get_text(key: str, lang: str = "en") -> str:
    """
    Возвращает текст по ключу для указанного языка.
    Если ключ не найден, возвращает сам ключ.
    """
    if lang not in LOCALES:
        lang = "en"
    return LOCALES[lang].get(key, key)
