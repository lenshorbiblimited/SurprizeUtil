import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import platform
import psutil
import datetime
import os
import shutil
import qrcode
from PIL import Image, ImageTk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import re
import random
import string
import math

class SurprizeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Surprize - Многофункциональная утилита")
        self.geometry("800x600")
        self.minsize(800, 600)
        
        # Настройка стиля
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure(bg="#f0f0f0")
        
        # Создание вкладок
        self.tab_control = ttk.Notebook(self)
        
        # Вкладка системной информации
        self.system_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.system_tab, text="Системная информация")
        self.setup_system_tab()
        
        # Вкладка организации файлов
        self.file_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.file_tab, text="Организация файлов")
        self.setup_file_tab()
        
        # Вкладка заметок
        self.notes_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.notes_tab, text="Заметки")
        self.setup_notes_tab()
        
        # Вкладка генератора паролей
        self.password_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.password_tab, text="Генератор паролей")
        self.setup_password_tab()
        
        # Вкладка генератора QR-кодов
        self.qr_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.qr_tab, text="QR-код")
        self.setup_qr_tab()
        
        # Вкладка облака слов
        self.wordcloud_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.wordcloud_tab, text="Облако слов")
        self.setup_wordcloud_tab()
        
        self.tab_control.pack(expand=1, fill="both")
        
    def setup_system_tab(self):
        # Создание фрейма для системной информации
        self.system_info_frame = ttk.Frame(self.system_tab)
        self.system_info_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.setup_system_info_frame()
        
        # Кнопка обновления
        refresh_btn = ttk.Button(self.system_tab, text="Обновить информацию", command=self.refresh_system_info)
        refresh_btn.pack(pady=10)
    
    def setup_system_info_frame(self):
        # Получение системной информации
        system_info = self.get_system_info()
        
        # Создание и размещение меток с информацией
        for i, (key, value) in enumerate(system_info.items()):
            ttk.Label(self.system_info_frame, text=f"{key}:", font=("Arial", 10, "bold")).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            ttk.Label(self.system_info_frame, text=value).grid(row=i, column=1, sticky="w", padx=5, pady=5)
    
    def refresh_system_info(self):
        # Обновление системной информации
        self.system_info_frame.destroy()
        self.system_info_frame = ttk.Frame(self.system_tab)
        self.system_info_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.setup_system_info_frame()
    
    def get_system_info(self):
        system_info = {
            "Операционная система": platform.system() + " " + platform.release(),
            "Версия Python": platform.python_version(),
            "Имя компьютера": platform.node(),
            "Процессор": platform.processor(),
            "Физическая память": f"{round(psutil.virtual_memory().total / (1024**3), 2)} ГБ",
            "Доступная память": f"{round(psutil.virtual_memory().available / (1024**3), 2)} ГБ",
            "Использование CPU": f"{psutil.cpu_percent()}%",
            "Текущее время": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        return system_info
    
    def setup_file_tab(self):
        frame = ttk.LabelFrame(self.file_tab, text="Организация файлов по типу")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Выбор директории
        dir_frame = ttk.Frame(frame)
        dir_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(dir_frame, text="Директория:").pack(side="left", padx=5)
        self.dir_entry = ttk.Entry(dir_frame, width=50)
        self.dir_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        browse_btn = ttk.Button(dir_frame, text="Обзор", command=self.browse_directory)
        browse_btn.pack(side="left", padx=5)
        
        # Опции сортировки
        options_frame = ttk.LabelFrame(frame, text="Опции")
        options_frame.pack(fill="x", padx=10, pady=10)
        
        self.create_dirs_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Создать директории для типов файлов", 
                       variable=self.create_dirs_var).pack(anchor="w", padx=5, pady=5)
        
        self.move_files_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Переместить файлы в соответствующие директории", 
                       variable=self.move_files_var).pack(anchor="w", padx=5, pady=5)
        
        # Кнопка запуска сортировки
        sort_btn = ttk.Button(frame, text="Организовать файлы", command=self.organize_files)
        sort_btn.pack(pady=10)
        
        # Лог операций
        log_frame = ttk.LabelFrame(frame, text="Лог операций")
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.log_text = tk.Text(log_frame, height=10, width=70)
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(self.log_text, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)
        self.log_text.config(state="disabled")
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
    
    def organize_files(self):
        directory = self.dir_entry.get()
        if not directory or not os.path.isdir(directory):
            messagebox.showerror("Ошибка", "Пожалуйста, выберите существующую директорию")
            return
        
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, f"Начало организации файлов в {directory}\n")
        
        try:
            file_types = {}
            # Сканирование файлов и определение типов
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    file_ext = os.path.splitext(filename)[1].lower()
                    if file_ext:
                        # Убираем точку из расширения
                        file_ext = file_ext[1:]
                        if file_ext not in file_types:
                            file_types[file_ext] = []
                        file_types[file_ext].append(filename)
            
            self.log_text.insert(tk.END, f"Найдено {sum(len(files) for files in file_types.values())} файлов с {len(file_types)} различными типами\n")
            
            # Создание директорий и перемещение файлов
            if self.create_dirs_var.get():
                for file_ext in file_types:
                    type_dir = os.path.join(directory, file_ext)
                    if not os.path.exists(type_dir):
                        os.makedirs(type_dir)
                        self.log_text.insert(tk.END, f"Создана директория: {file_ext}\n")
                    
                    if self.move_files_var.get():
                        for filename in file_types[file_ext]:
                            source = os.path.join(directory, filename)
                            destination = os.path.join(type_dir, filename)
                            shutil.move(source, destination)
                            self.log_text.insert(tk.END, f"Перемещен файл: {filename} -> {file_ext}/\n")
            
            self.log_text.insert(tk.END, "Организация файлов завершена успешно!\n")
            messagebox.showinfo("Успех", "Файлы успешно организованы!")
        
        except Exception as e:
            self.log_text.insert(tk.END, f"Ошибка: {str(e)}\n")
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
        
        self.log_text.config(state="disabled")
    
    def setup_notes_tab(self):
        frame = ttk.Frame(self.notes_tab)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Заголовок и поле для заметки
        ttk.Label(frame, text="Заголовок:").pack(anchor="w", padx=5, pady=5)
        self.title_entry = ttk.Entry(frame, width=50)
        self.title_entry.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(frame, text="Заметка:").pack(anchor="w", padx=5, pady=5)
        self.note_text = tk.Text(frame, height=10, width=70)
        self.note_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Кнопки для работы с заметками
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        save_btn = ttk.Button(btn_frame, text="Сохранить", command=self.save_note)
        save_btn.pack(side="left", padx=5)
        
        load_btn = ttk.Button(btn_frame, text="Загрузить", command=self.load_note)
        load_btn.pack(side="left", padx=5)
        
        clear_btn = ttk.Button(btn_frame, text="Очистить", command=self.clear_note)
        clear_btn.pack(side="left", padx=5)
    
    def save_note(self):
        title = self.title_entry.get().strip()
        note = self.note_text.get(1.0, tk.END).strip()
        
        if not title:
            messagebox.showerror("Ошибка", "Пожалуйста, введите заголовок заметки")
            return
        
        if not note:
            messagebox.showerror("Ошибка", "Пожалуйста, введите текст заметки")
            return
        
        # Создание директории для заметок, если она не существует
        notes_dir = os.path.join(os.path.expanduser("~"), "Surprize_Notes")
        if not os.path.exists(notes_dir):
            os.makedirs(notes_dir)
        
        # Сохранение заметки в файл
        filename = os.path.join(notes_dir, f"{title}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(note)
        
        messagebox.showinfo("Успех", f"Заметка '{title}' успешно сохранена!")
    
    def load_note(self):
        notes_dir = os.path.join(os.path.expanduser("~"), "Surprize_Notes")
        if not os.path.exists(notes_dir):
            messagebox.showerror("Ошибка", "Директория с заметками не найдена")
            return
        
        filename = filedialog.askopenfilename(
            initialdir=notes_dir,
            title="Выберите заметку",
            filetypes=(("Текстовые файлы", "*.txt"), ("Все файлы", "*.*"))
        )
        
        if filename:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    note_content = f.read()
                
                # Установка заголовка и содержимого заметки
                note_title = os.path.splitext(os.path.basename(filename))[0]
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, note_title)
                
                self.note_text.delete(1.0, tk.END)
                self.note_text.insert(tk.END, note_content)
                
                messagebox.showinfo("Успех", f"Заметка '{note_title}' успешно загружена!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить заметку: {str(e)}")
    
    def clear_note(self):
        self.title_entry.delete(0, tk.END)
        self.note_text.delete(1.0, tk.END)

    def setup_password_tab(self):
        frame = ttk.LabelFrame(self.password_tab, text="Генератор надежных паролей")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Настройки пароля
        options_frame = ttk.Frame(frame)
        options_frame.pack(fill="x", padx=10, pady=10)
        
        # Длина пароля
        ttk.Label(options_frame, text="Длина пароля:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.length_var = tk.IntVar(value=12)
        length_spinbox = ttk.Spinbox(options_frame, from_=4, to=64, textvariable=self.length_var, width=5)
        length_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Опции символов
        options_frame2 = ttk.Frame(frame)
        options_frame2.pack(fill="x", padx=10, pady=5)
        
        # Чекбоксы для выбора типов символов
        self.use_upper = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame2, text="Заглавные буквы (A-Z)", variable=self.use_upper).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.use_lower = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame2, text="Строчные буквы (a-z)", variable=self.use_lower).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.use_digits = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame2, text="Цифры (0-9)", variable=self.use_digits).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        self.use_special = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame2, text="Специальные символы (!@#$%^&*)", variable=self.use_special).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Кнопка генерации пароля
        generate_btn = ttk.Button(frame, text="Сгенерировать пароль", command=self.generate_password)
        generate_btn.pack(pady=10)
        
        # Результат
        result_frame = ttk.LabelFrame(frame, text="Сгенерированный пароль")
        result_frame.pack(fill="x", padx=10, pady=10, expand=True)
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(result_frame, textvariable=self.password_var, font=("Arial", 12), width=40)
        password_entry.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
        copy_btn = ttk.Button(result_frame, text="Копировать", command=self.copy_password)
        copy_btn.pack(side="left", padx=10, pady=10)
        
        # Индикатор надежности
        strength_frame = ttk.LabelFrame(frame, text="Надежность пароля")
        strength_frame.pack(fill="x", padx=10, pady=10)
        
        self.strength_var = tk.StringVar(value="Не определена")
        ttk.Label(strength_frame, textvariable=self.strength_var, font=("Arial", 10, "bold")).pack(padx=10, pady=10)
        
        # Полезные советы
        tips_frame = ttk.LabelFrame(frame, text="Полезные советы")
        tips_frame.pack(fill="x", padx=10, pady=10)
        
        tips_text = "• Используйте пароли длиной не менее 12 символов\n"
        tips_text += "• Включайте в пароли разные типы символов (буквы, цифры, специальные символы)\n"
        tips_text += "• Не используйте один и тот же пароль на разных сайтах\n"
        tips_text += "• Регулярно меняйте свои пароли"
        
        ttk.Label(tips_frame, text=tips_text, justify="left").pack(padx=10, pady=10, anchor="w")
    
    def generate_password(self):
        length = self.length_var.get()
        
        # Проверка выбора опций
        if not any([self.use_upper.get(), self.use_lower.get(), self.use_digits.get(), self.use_special.get()]):
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
            return
        
        # Создание набора символов
        chars = ""
        if self.use_upper.get():
            chars += string.ascii_uppercase
        if self.use_lower.get():
            chars += string.ascii_lowercase
        if self.use_digits.get():
            chars += string.digits
        if self.use_special.get():
            chars += string.punctuation
        
        # Генерация пароля
        password = "".join(random.choice(chars) for _ in range(length))
        self.password_var.set(password)
        
        # Оценка надежности пароля
        self.evaluate_password_strength(password)
    
    def evaluate_password_strength(self, password):
        strength = 0
        feedback = ""
        
        # Проверка длины
        if len(password) < 8:
            strength = 1
            feedback = "Очень слабый"
        elif len(password) < 10:
            strength = 2
            feedback = "Слабый"
        elif len(password) < 12:
            strength = 3
            feedback = "Средний"
        elif len(password) < 16:
            strength = 4
            feedback = "Хороший"
        else:
            strength = 5
            feedback = "Отличный"
        
        # Проверка разнообразия символов
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        # Увеличение оценки за разнообразие символов
        diversity = sum([has_upper, has_lower, has_digit, has_special])
        if diversity < 3 and strength > 2:
            strength -= 1
        elif diversity == 4 and strength < 5:
            strength += 1
        
        # Установка индикатора надежности
        if strength == 1:
            self.strength_var.set("Очень слабый пароль")
        elif strength == 2:
            self.strength_var.set("Слабый пароль")
        elif strength == 3:
            self.strength_var.set("Средний пароль")
        elif strength == 4:
            self.strength_var.set("Хороший пароль")
        elif strength == 5:
            self.strength_var.set("Отличный пароль")
    
    def copy_password(self):
        password = self.password_var.get()
        if password:
            self.clipboard_clear()
            self.clipboard_append(password)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена")

    def setup_qr_tab(self):
        frame = ttk.Frame(self.qr_tab)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Поле для ввода текста
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(input_frame, text="Введите текст или URL:").pack(pady=(10, 5), anchor="w")
        
        self.qr_text = ttk.Entry(input_frame, width=50)
        self.qr_text.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Кнопки управления
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(side="right")
        
        # Кнопка для вставки текста из буфера обмена
        paste_btn = ttk.Button(button_frame, text="Вставить", command=self.paste_to_qr)
        paste_btn.pack(pady=2)
        
        # Кнопка очистки
        clear_btn = ttk.Button(button_frame, text="Очистить", command=lambda: self.qr_text.delete(0, tk.END))
        clear_btn.pack(pady=2)
        
        # Настройки QR-кода
        settings_frame = ttk.LabelFrame(frame, text="Настройки")
        settings_frame.pack(fill="x", padx=10, pady=10)
        
        # Размер QR-кода
        ttk.Label(settings_frame, text="Размер:").grid(row=0, column=0, padx=5, pady=5)
        self.qr_size = ttk.Combobox(settings_frame, values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], width=5)
        self.qr_size.set("5")  # По умолчанию размер 5
        self.qr_size.grid(row=0, column=1, padx=5, pady=5)
        
        # Цвет QR-кода
        ttk.Label(settings_frame, text="Цвет:").grid(row=1, column=0, padx=5, pady=5)
        self.qr_color = ttk.Combobox(settings_frame, values=["Черный", "Синий", "Красный", "Зеленый"], width=10)
        self.qr_color.set("Черный")  # По умолчанию черный
        self.qr_color.grid(row=1, column=1, padx=5, pady=5)
        
        # Кнопка генерации
        generate_btn = ttk.Button(frame, text="Сгенерировать QR-код", command=self.generate_qr)
        generate_btn.pack(pady=10)
        
        # Фрейм для предпросмотра
        preview_frame = ttk.LabelFrame(frame, text="Предпросмотр")
        preview_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Метка для предпросмотра QR-кода
        self.qr_preview = ttk.Label(preview_frame, text="Здесь появится QR-код после генерации")
        self.qr_preview.pack(pady=20)
        
        # Кнопка сохранения
        self.save_qr_btn = ttk.Button(frame, text="Сохранить QR-код", command=self.save_qr, state="disabled")
        self.save_qr_btn.pack(pady=10)
        
        # Переменная для хранения текущего QR-кода
        self.qr_image = None
    
    def paste_to_qr(self):
        # Вставка текста из буфера обмена в поле для ввода QR-кода
        try:
            clipboard_text = self.clipboard_get()
            self.qr_text.delete(0, tk.END)
            self.qr_text.insert(0, clipboard_text)
        except:
            messagebox.showinfo("Информация", "Буфер обмена пуст или содержит недопустимые символы")
    
    def generate_qr(self):
        text = self.qr_text.get().strip()
        if not text:
            messagebox.showerror("Ошибка", "Введите текст или URL")
            return
        
        # Создание QR-кода
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=self.qr_size.get(),
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        # Создание изображения
        color_map = {
            "Черный": "#000000",
            "Синий": "#0000FF",
            "Красный": "#FF0000",
            "Зеленый": "#00FF00"
        }
        
        color = color_map.get(self.qr_color.get(), "#000000")
        img = qr.make_image(fill_color=color, back_color="white")
        
        # Сохранение изображения
        self.qr_image = img
        
        # Предпросмотр изображения
        photo_image = ImageTk.PhotoImage(img)
        self.qr_preview.configure(image=photo_image)
        self.qr_preview.image = photo_image  # Сохранение ссылки на изображение
        
        # Активация кнопки сохранения QR-кода
        self.save_qr_btn.config(state="normal")
    
    def save_qr(self):
        if not self.qr_image:
            messagebox.showerror("Ошибка", "Сначала сгенерируйте QR-код")
            return
        
        # Запрос на сохранение файла
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Все файлы", "*.*")],
            title="Сохранить QR-код"
        )
        
        if file_path:
            try:
                self.qr_image.save(file_path)
                messagebox.showinfo("Успех", f"QR-код сохранен как {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить QR-код: {str(e)}")

    def setup_wordcloud_tab(self):
        frame = ttk.Frame(self.wordcloud_tab)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Поле для ввода текста
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(input_frame, text="Введите или вставьте текст для создания облака слов:").pack(pady=(10, 5), anchor="w")
        
        self.wordcloud_text = tk.Text(input_frame, height=10, width=70)
        self.wordcloud_text.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Кнопки управления
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(side="right")
        
        # Кнопка для вставки текста из буфера обмена
        paste_btn = ttk.Button(button_frame, text="Вставить", command=self.paste_to_wordcloud)
        paste_btn.pack(pady=2)
        
        # Кнопка очистки
        clear_btn = ttk.Button(button_frame, text="Очистить", command=lambda: self.wordcloud_text.delete(1.0, tk.END))
        clear_btn.pack(pady=2)
        
        # Настройки облака слов
        settings_frame = ttk.LabelFrame(frame, text="Настройки")
        settings_frame.pack(fill="x", padx=10, pady=10)
        
        # Цвет фона
        ttk.Label(settings_frame, text="Цвет фона:").grid(row=0, column=0, padx=5, pady=5)
        self.bg_color = ttk.Combobox(settings_frame, values=["Белый", "Черный", "Синий", "Красный"], width=10)
        self.bg_color.set("Белый")
        self.bg_color.grid(row=0, column=1, padx=5, pady=5)
        
        # Цвет текста
        ttk.Label(settings_frame, text="Цвет текста:").grid(row=1, column=0, padx=5, pady=5)
        self.text_color = ttk.Combobox(settings_frame, values=["Черный", "Белый", "Синий", "Красный"], width=10)
        self.text_color.set("Черный")
        self.text_color.grid(row=1, column=1, padx=5, pady=5)
        
        # Максимальное количество слов
        ttk.Label(settings_frame, text="Макс. слов:").grid(row=2, column=0, padx=5, pady=5)
        self.max_words = ttk.Spinbox(settings_frame, from_=10, to=200, width=10)
        self.max_words.set(100)
        self.max_words.grid(row=2, column=1, padx=5, pady=5)
        
        # Кнопка для генерации облака слов
        generate_btn = ttk.Button(frame, text="Сгенерировать облако слов", command=self.generate_wordcloud)
        generate_btn.pack(pady=10)
        
        # Предпросмотр облака слов
        preview_frame = ttk.LabelFrame(frame, text="Предпросмотр")
        preview_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.wordcloud_preview = ttk.Label(preview_frame, text="Здесь появится облако слов после генерации")
        self.wordcloud_preview.pack(padx=10, pady=10, expand=True)
        
        # Кнопка сохранения
        self.save_btn = ttk.Button(frame, text="Сохранить изображение", command=self.save_wordcloud, state="disabled")
        self.save_btn.pack(pady=10)
        
        # Переменная для хранения текущего облака слов
        self.wordcloud_image = None
    
    def generate_wordcloud(self):
        text = self.wordcloud_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showerror("Ошибка", "Введите текст")
            return
        
        try:
            # Определение цветов
            colors = {
                "Белый": "white",
                "Черный": "black",
                "Синий": "navy",
                "Красный": "darkred"
            }
            
            bg_color = colors[self.bg_color.get()]
            text_color = colors[self.text_color.get()]
            max_words = int(self.max_words.get())
            
            # Создание облака слов
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color=bg_color,
                color_func=lambda *args, **kwargs: text_color,
                max_words=max_words,
                prefer_horizontal=0.7,
                min_font_size=10,
                max_font_size=100
            ).generate(text)
            
            # Сохранение изображения
            self.wordcloud_image = wordcloud.to_image()
            
            # Изменение размера для предпросмотра
            preview = self.wordcloud_image.copy()
            preview.thumbnail((600, 300))
            
            # Предпросмотр изображения
            photo_image = ImageTk.PhotoImage(preview)
            self.wordcloud_preview.configure(image=photo_image)
            self.wordcloud_preview.image = photo_image
            
            # Активация кнопки сохранения
            self.save_btn.config(state="normal")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при создании облака слов: {str(e)}")
    
    def save_wordcloud(self):
        if not self.wordcloud_image:
            messagebox.showerror("Ошибка", "Сначала создайте облако слов")
            return
        
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG файлы", "*.png"), ("Все файлы", "*.*")],
                title="Сохранить облако слов"
            )
            
            if file_path:
                self.wordcloud_image.save(file_path, "PNG")
                messagebox.showinfo("Успех", "Облако слов успешно сохранено")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении файла: {str(e)}")

    def paste_to_wordcloud(self):
        # Вставка текста из буфера обмена в поле для ввода облака слов
        try:
            clipboard_text = self.clipboard_get()
            self.wordcloud_text.delete(1.0, tk.END)
            self.wordcloud_text.insert(tk.END, clipboard_text)
        except:
            messagebox.showinfo("Информация", "Буфер обмена пуст или содержит недопустимые символы")

if __name__ == "__main__":
    app = SurprizeApp()
    app.mainloop()
