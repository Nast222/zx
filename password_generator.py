import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import string
from datetime import datetime

# --- 1. КОНФИГУРАЦИЯ И КОНСТАНТЫ ---
HISTORY_FILE = 'history.json'
MIN_LENGTH = 8  # Минимальная длина пароля (рекомендуется от 8)
MAX_LENGTH = 64 # Максимальная длина пароля

# --- 2. КЛАСС ДЛЯ УПРАВЛЕНИЯ ПАРОЛЯМИ И ИСТОРИЕЙ ---
class PasswordManager:
    """
    Класс отвечает за логику генерации паролей и работу с файлом истории.
    """
    def __init__(self, filename):
        self.filename = filename
        self.history = self._load_history()

    def _load_history(self):
        """Приватный метод для загрузки истории из файла JSON."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Если файла нет или он пустой, возвращаем пустой список
            return []

    def _save_history(self):
        """Приватный метод для сохранения истории в файл JSON."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.history, file, ensure_ascii=False, indent=2)

    def add_to_history(self, password_data):
        """
        Добавляет новый пароль в историю и сохраняет файл.
        :param password_data: Словарь с данными о пароле.
        """
        self.history.append(password_data)
        self._save_history()

    def generate_password(self, length, use_digits, use_letters, use_specials):
        """
        Генерирует пароль на основе переданных параметров.
        :param length: Длина пароля.
        :param use_digits: Использовать ли цифры.
        :param use_letters: Использовать ли буквы.
        :param use_specials: Использовать ли спецсимволы.
        :return: Сгенерированная строка пароля.
        :raises ValueError: Если параметры заданы неверно.
        """
        # Проверка длины пароля
        if not (MIN_LENGTH <= length <= MAX_LENGTH):
            raise ValueError(f"Длина пароля должна быть от {MIN_LENGTH} до {MAX_LENGTH} символов.")
        
        # Формируем пул доступных символов на основе выбора пользователя
        chars = ''
        if use_letters:
            chars += string.ascii_letters  # Буквы (a-z, A-Z)
        if use_digits:
            chars += string.digits         # Цифры (0-9)
        if use_specials:
            chars += string.punctuation    # Спецсимволы (!"#$%&'()*+,-./:;<=>?@[$$^_`{|}~)
        
        # Проверка, что хотя бы одна группа символов выбрана
        if not chars:
            raise ValueError("Выберите хотя бы один тип символов (Буквы, Цифры или Спецсимволы).")
        
        # Генерация пароля. random.choices позволяет повторения символов.
        password = ''.join(random.choices(chars, k=length))
        
        return password

# --- 3. ГРАФИЧЕСКИЙ ИНТЕРФЕЙС (КЛАСС ПРИЛОЖЕНИЯ) ---
class PasswordGeneratorApp(tk.Tk):
    """
    Основной класс приложения, отвечающий за GUI.
    """
    def __init__(self):
        super().__init__()
        
        self.title("🔐 Генератор Случайных Паролей")
        self.geometry("750x550")
        
        # Инициализация менеджера данных
        self.manager = PasswordManager(HISTORY_FILE)
        
        # Создаем все виджеты (элементы окна)
        self.create_widgets()
        
    def create_widgets(self):
        """Метод для создания и размещения всех элементов интерфейса."""
        
        # --- РАМКА НАСТРОЕК ГЕНЕРАЦИИ ---
        settings_frame = ttk.LabelFrame(self, text="⚙️ Настройки генерации", padding="10")
        settings_frame.pack(fill='x', padx=10, pady=5)

         # Ползунок (Scale) для выбора длины
         ttk.Label(settings_frame, text="Длина пароля:").grid(row=0, column=0, sticky='w')
         self.length_var = tk.IntVar(value=12)
         self.length_slider = ttk.Scale(
             settings_frame,
             from_=MIN_LENGTH,
             to=MAX_LENGTH,
             variable=self.length_var,
             orient="horizontal",
             length=250,
             command=lambda x: self.length_var.set(int(float(x)))
         )
         self.length_slider.grid(row=0, column=1, columnspan=2)
         
         # Отображение текущего значения длины
         self.length_display = ttk.Label(settings_frame, textvariable=self.length_var)
         self.length_display.grid(row=0, column=3)
         
         # Чекбоксы (Checkbutton) для выбора типов символов
         self.use_digits_var = tk.BooleanVar(value=True)
         self.use_letters_var = tk.BooleanVar(value=True)
         self.use_specials_var = tk.BooleanVar(value=True)
         
         ttk.Checkbutton(settings_frame, text="Цифры (0-9)", variable=self.use_digits_var).grid(row=1, column=0, columnspan=2, sticky='w')
         ttk.Checkbutton(settings_frame, text="Буквы (a-zA-Z)", variable=self.use_letters_var).grid(row=2, column=0, columnspan=2, sticky='w')
         ttk.Checkbutton(settings_frame, text="Спецсимволы (!@#)", variable=self.use_specials_var).grid(row=3, column=0, columnspan=2, sticky='w')
         
         # Кнопка генерации и поле вывода результата
         self.generate_btn = ttk.Button(
             settings_frame,
             text="🔄 Сгенерировать пароль",
             command=self.on_generate_click,
             style="Accent.TButton"
         )
         self.generate_btn.grid(row=4, column=0, columnspan=4, pady=15)
         
         self.password_entry = ttk.Entry(settings_frame, width=45)
         self.password_entry.grid(row=5, column=0, columnspan=3)
         
         # Кнопка копирования в буфер обмена
         ttk.Button(settings_frame, text="📋 Копировать", command=self.copy_to_clipboard).grid(row=5, column=3)
         
         # --- РАМКА ИСТОРИИ ---
         history_frame = ttk.LabelFrame(self, text="📜 История генераций", padding="10")
         history_frame.pack(fill='both', expand=True, padx=10, pady=5)
         
         # Определение колонок для таблицы (Treeview)
         columns = ("timestamp", "length", "digits", "letters", "specials", "password")
         
         self.tree = ttk.Treeview(history_frame, columns=columns, show="headings")
         
         # Настройка заголовков и ширины колонок
         for col in columns:
             self.tree.heading(col, text={
                 "timestamp": "Дата/Время",
                 "length": "Длина",
                 "digits": "Цифры",
                 "letters": "Буквы",
                 "specials": "Спецсимволы",
                 "password": "Пароль"
             }[col])
             self.tree.column(col, minwidth=0, width=120)
             
         # Добавление вертикальной прокрутки для таблицы
         scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
         self.tree.configure(yscrollcommand=scrollbar.set)
         
         self.tree.pack(side="left", fill="both", expand=True)
         scrollbar.pack(side="right", fill="y")
         
    # --- 4. ЛОГИКА ОБРАБОТКИ СОБЫТИЙ ---
    def on_generate_click(self):
        """
        Обработчик нажатия кнопки "Сгенерировать".
        Здесь происходит валидация и вызов логики генерации.
        """
        try:
            # Получаем значения из интерфейса
            length = self.length_var.get()
            use_digits = self.use_digits_var.get()
            use_letters = self.use_letters_var.get()
            use_specials = self.use_specials_var.get()
            
            # Вызов метода генерации из менеджера данных
            new_password = self.manager.generate_password(length, use_digits, use_letters, use_specials)
            
            # Отображение пароля в поле ввода
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, new_password)
            
            # Подготовка данных для истории
            history_entry = {
                "password": new_password,
                "length": length,
                "digits": use_digits,
                "letters": use_letters,
                "specials": use_specials,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Сохранение в историю и обновление таблицы на экране
            self.manager.add_to_history(history_entry)
            self.update_history_view()
            
            messagebox.showinfo("Готово!", "Пароль успешно сгенерирован!")
            
        except ValueError as error:
            # Обработка ошибок валидации (например, неверная длина или нет выбранных символов)
            messagebox.showerror("Ошибка ввода", str(error))
    
    def update_history_view(self):
        """
        Обновляет виджет таблицы (Treeview), загружая в него данные из истории.
        Новые записи добавляются сверху.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for entry in reversed(self.manager.history): # reversed() - чтобы новые были сверху
            self.tree.insert("", "end", values=(
                entry['timestamp'],
                entry['length'],
                'Да' if entry['digits'] else 'Нет',
                'Да' if entry['letters'] else 'Нет',
                'Да' if entry['specials'] else 'Нет',
                entry['password']
            ))
    
    def copy_to_clipboard(self):
        """Копирует текущий пароль из поля ввода в системный буфер обмена."""
        password = self.password_entry.get()
        
        if password:
            self.clipboard_clear()      # Очищаем буфер обмена от старых данных
            self.clipboard_append(password) # Добавляем новый пароль
            
            messagebox.showinfo("Скопировано", "Пароль скопирован в буфер обмена!")


# --- 5. ТОЧКА ВХОДА В ПРИЛОЖЕНИЕ ---
if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
