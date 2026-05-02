import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import json
import string
import os

# --- КОНФИГУРАЦИЯ ---
HISTORY_FILE = 'history.json'
MIN_LENGTH = 4   # Минимальная длина пароля для безопасности
MAX_LENGTH = 128 # Максимальная длина пароля

# --- 1. МОДЕЛЬ ДАННЫХ (КЛАСС УПРАВЛЕНИЯ) ---
class PasswordManager:
    """Отвечает за генерацию паролей и управление историей."""
    def __init__(self, filename):
        self.filename = filename
        self.history = self.load_history()

    def load_history(self):
        """Загружает историю из JSON. Если файла нет, возвращает пустой список."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_history(self):
        """Сохраняет текущий список истории в JSON."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def add_to_history(self, password, length, use_digits, use_letters, use_specials):
        """Добавляет новый пароль в историю."""
        self.history.append({
            "password": password,
            "length": length,
            "digits": use_digits,
            "letters": use_letters,
            "specials": use_specials,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.save_history()

    def generate_password(self, length, use_digits, use_letters, use_specials):
        """Генерирует пароль на основе выбранных параметров."""
        if length < MIN_LENGTH or length > MAX_LENGTH:
            raise ValueError(f"Длина должна быть от {MIN_LENGTH} до {MAX_LENGTH}.")
        
        # Формируем набор символов (pool) на основе чекбоксов
        chars = ''
        if use_letters:
            chars += string.ascii_letters  # a-zA-Z
        if use_digits:
            chars += string.digits         # 0-9
        if use_specials:
            chars += string.punctuation    # Спецсимволы !"#$%&'()*+,-./:;<=>?@[$$^_`{|}~
        
        if not chars:
            raise ValueError("Выберите хотя бы один тип символов для генерации.")
        
        # Генерируем пароль, гарантируя наличие символов из каждой выбранной группы
        password = []
        if use_letters: password.append(random.choice(string.ascii_letters))
        if use_digits:   password.append(random.choice(string.digits))
        if use_specials: password.Вот подробная пошаговая инструкция и полный код для создания приложения **Random Password Generator**.

Это приложение позволяет генерировать сложные пароли с гибкой настройкой и сохранять историю созданных паролей.

---

### 1. Структура проекта

Создайте папку для проекта (например, `password_generator`) и добавьте в нее следующие файлы:
