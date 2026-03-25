# 📚 Аліса в Задзеркаллі — HTML-проєкт

> Навчальний проєкт: верстка сторінок книги Льюїса Керола у HTML/CSS

[![Tests](https://github.com/YOUR_USERNAME/alice-html-project/actions/workflows/tests.yml/badge.svg)](https://github.com/YOUR_USERNAME/alice-html-project/actions/workflows/tests.yml)

---

## 🎯 Завдання

Кожен студент отримує **одну сторінку** тексту книги та має оформити її у вигляді HTML-сторінки згідно з вимогами.

---

## 📋 Розподіл сторінок

| Студент | Сторінка | Файл тексту |
|---------|----------|-------------|
| *(прізвище 1)* | page_01 | `text/pages/page_01.txt` |
| *(прізвище 2)* | page_02 | `text/pages/page_02.txt` |
| *(прізвище 3)* | page_03 | `text/pages/page_03.txt` |
| *(прізвище 4)* | page_04 | `text/pages/page_04.txt` |
| *(прізвище 5)* | page_05 | `text/pages/page_05.txt` |

> 🔧 Викладач заповнює таблицю перед початком роботи.

---

## 🚀 Як почати роботу

### 1. Клонування репозиторію

```bash
git clone https://github.com/YOUR_USERNAME/alice-html-project.git
cd alice-html-project
```

### 2. Знайди свою сторінку

Відкрий файл `text/pages/page_XX.txt` — це твій текст.

### 3. Скопіюй шаблон у свою папку

```bash
cp TEMPLATE.html pages/page_XX/index.html
cp STYLE_TEMPLATE.css pages/page_XX/style.css
```

### 4. Редагуй файли

Відкрий `pages/page_XX/index.html` і `pages/page_XX/style.css` у редакторі.

### 5. Зроби коміт та пуш

```bash
git add pages/page_XX/
git commit -m "Add page_XX by Ім'я Прізвище"
git push
```

> ✅ Після пушу автоматично запустяться тести у GitHub Actions.  
> Результат побачиш у вкладці **Actions** → твій коміт.

---

## ✅ Вимоги до HTML-сторінки

Детальний опис — у файлі [`REQUIREMENTS.md`](REQUIREMENTS.md).

**Коротко:**

1. Коректна HTML5-структура (`<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`)
2. `<meta charset="UTF-8">`
3. `<title>` із назвою розділу
4. Підключений зовнішній CSS (`<link rel="stylesheet">`)
5. Один заголовок `<h1>` з назвою розділу
6. Весь текст оформлено у `<p>` параграфи
7. Текст відповідає призначеній сторінці
8. CSS-файл містить щонайменше 5 різних правил стилів

---

## 📁 Структура репозиторію

```
alice-html-project/
├── .github/
│   └── workflows/
│       └── tests.yml          # GitHub Actions CI
├── pages/
│   ├── example/               # Готовий приклад
│   │   ├── index.html
│   │   └── style.css
│   ├── page_01/               # Папка студента 1
│   │   ├── index.html         ← тут студент працює
│   │   └── style.css
│   └── ...
├── text/
│   └── pages/
│       ├── page_01.txt        # Текст для сторінки 1
│       └── ...
├── tests/
│   ├── conftest.py
│   ├── test_structure.py      # Тест: структура HTML
│   ├── test_elements.py       # Тест: обов'язкові елементи
│   ├── test_css.py            # Тест: наявність та зміст CSS
│   └── test_content.py        # Тест: відповідність тексту
├── TEMPLATE.html              # Шаблон для студентів
├── STYLE_TEMPLATE.css         # Шаблон CSS
├── REQUIREMENTS.md            # Детальні вимоги
└── README.md
```

---

## 🔍 Як читати результати тестів

Після пушу зайди у **GitHub → Actions** → останній workflow.

- ✅ **Passed** — все чудово!
- ❌ **Failed** — розгорни лог і знайди повідомлення про помилку

Приклад помилки:
```
FAILED tests/test_elements.py::test_has_h1 - AssertionError: Відсутній тег <h1>
```

---

## 💡 Корисні посилання

- [MDN: HTML basics](https://developer.mozilla.org/uk/docs/Learn/Getting_started_with_the_web/HTML_basics)
- [MDN: CSS basics](https://developer.mozilla.org/uk/docs/Learn/Getting_started_with_the_web/CSS_basics)
- [HTML Validator](https://validator.w3.org/)
