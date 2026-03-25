"""
test_css.py — Тести CSS-файлу

Перевіряє:
  - Файл style.css існує
  - Файл непорожній
  - Містить щонайменше 5 CSS-правил
  - Присутні обов'язкові властивості
"""
import pytest
import re
from pathlib import Path


# Обов'язкові CSS-властивості (хоча б одна з кожної групи)
REQUIRED_PROPERTIES = {
    "шрифт": ["font-family", "font-size", "font-weight"],
    "колір тексту": ["color"],
    "фон": ["background-color", "background"],
    "відступи": ["margin", "padding", "margin-top", "margin-bottom",
                  "padding-top", "padding-bottom", "margin-left", "margin-right"],
    "розмір/висота рядка": ["line-height", "font-size"],
}


def load_css(page_dir: Path) -> str:
    """Завантажує вміст style.css."""
    css_file = page_dir / "style.css"
    assert css_file.exists(), (
        f"❌ [{page_dir.name}] Файл style.css не знайдено у {page_dir.name}/\n"
        f"   Створи файл style.css поряд з index.html"
    )
    return css_file.read_text(encoding="utf-8")


def count_css_rules(css_content: str) -> int:
    """Рахує кількість CSS-правил (блоків { })."""
    # Видаляємо коментарі
    css_no_comments = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    # Рахуємо відкриваючі дужки (кожна = одне правило)
    rules = re.findall(r'\{[^{}]*\}', css_no_comments, re.DOTALL)
    return len(rules)


def test_style_css_exists(page_dir: Path):
    """Файл style.css існує."""
    css_file = page_dir / "style.css"
    assert css_file.exists(), (
        f"❌ [{page_dir.name}] Файл style.css не знайдено.\n"
        f"   Переконайся, що файл знаходиться у папці pages/{page_dir.name}/"
    )


def test_style_css_not_empty(page_dir: Path):
    """Файл style.css не порожній."""
    css_content = load_css(page_dir)
    
    # Видаляємо коментарі та пробіли
    content_no_comments = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    meaningful_content = content_no_comments.strip()
    
    assert meaningful_content, (
        f"❌ [{page_dir.name}] Файл style.css порожній або містить лише коментарі.\n"
        f"   Додай CSS-стилі для оформлення сторінки."
    )


def test_css_has_enough_rules(page_dir: Path):
    """CSS містить щонайменше 5 правил."""
    css_content = load_css(page_dir)
    rule_count = count_css_rules(css_content)
    
    assert rule_count >= 5, (
        f"❌ [{page_dir.name}] CSS містить лише {rule_count} правил, потрібно щонайменше 5.\n"
        f"   Додай більше стилів: для body, h1, p, header, footer тощо."
    )


def test_css_has_font_property(page_dir: Path):
    """CSS містить властивість для шрифту."""
    css_content = load_css(page_dir).lower()
    
    found = any(prop in css_content for prop in ["font-family", "font-size"])
    assert found, (
        f"❌ [{page_dir.name}] CSS не містить властивостей для шрифту (font-family або font-size).\n"
        f"   Додай, наприклад: body {{ font-family: Georgia, serif; }}"
    )


def test_css_has_color_property(page_dir: Path):
    """CSS містить властивість color."""
    css_content = load_css(page_dir).lower()
    
    assert "color" in css_content, (
        f"❌ [{page_dir.name}] CSS не містить властивості color.\n"
        f"   Задай колір тексту, наприклад: body {{ color: #333; }}"
    )


def test_css_has_background_property(page_dir: Path):
    """CSS містить властивість background-color або background."""
    css_content = load_css(page_dir).lower()
    
    found = "background-color" in css_content or "background" in css_content
    assert found, (
        f"❌ [{page_dir.name}] CSS не містить властивостей фону (background-color або background).\n"
        f"   Задай колір фону, наприклад: body {{ background-color: #fff; }}"
    )


def test_css_has_spacing_property(page_dir: Path):
    """CSS містить властивість margin або padding."""
    css_content = load_css(page_dir).lower()
    
    found = "margin" in css_content or "padding" in css_content
    assert found, (
        f"❌ [{page_dir.name}] CSS не містить відступів (margin або padding).\n"
        f"   Додай відступи, наприклад: p {{ margin-bottom: 1em; }}"
    )


def test_css_has_line_height_or_font_size(page_dir: Path):
    """CSS містить line-height або font-size для читабельності."""
    css_content = load_css(page_dir).lower()
    
    found = "line-height" in css_content or "font-size" in css_content
    assert found, (
        f"❌ [{page_dir.name}] CSS не містить line-height або font-size.\n"
        f"   Для гарного читання додай: p {{ line-height: 1.7; font-size: 1.1em; }}"
    )
