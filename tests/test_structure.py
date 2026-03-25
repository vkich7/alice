"""
test_structure.py — Тести структури HTML-документа

Перевіряє:
  - DOCTYPE html
  - Наявність тегів <html>, <head>, <body>
  - Атрибут lang на <html>
  - Кодування UTF-8 у <meta charset>
  - Наявність <title>
  - Підключення зовнішнього CSS через <link>
"""
import pytest
from pathlib import Path
from conftest import load_html


def test_index_html_exists(page_dir: Path):
    """Файл index.html існує."""
    html_file = page_dir / "index.html"
    assert html_file.exists(), (
        f"❌ [{page_dir.name}] Файл index.html не знайдено.\n"
        f"   Переконайся, що файл знаходиться у папці pages/{page_dir.name}/"
    )


def test_doctype(page_dir: Path):
    """Документ починається з <!DOCTYPE html>."""
    html_file = page_dir / "index.html"
    if not html_file.exists():
        pytest.skip("index.html відсутній")
    
    content = html_file.read_text(encoding="utf-8").strip()
    assert content.lower().startswith("<!doctype html"), (
        f"❌ [{page_dir.name}] Відсутній або неправильний DOCTYPE.\n"
        f"   Перший рядок файлу має бути: <!DOCTYPE html>"
    )


def test_has_html_tag(page_dir: Path):
    """Наявний тег <html>."""
    soup, _ = load_html(page_dir)
    assert soup.find("html") is not None, (
        f"❌ [{page_dir.name}] Відсутній тег <html>."
    )


def test_html_lang_attribute(page_dir: Path):
    """Тег <html> має атрибут lang='uk'."""
    soup, _ = load_html(page_dir)
    html_tag = soup.find("html")
    if html_tag is None:
        pytest.skip("<html> відсутній")
    
    lang = html_tag.get("lang", "")
    assert lang, (
        f"❌ [{page_dir.name}] Тег <html> не має атрибуту lang.\n"
        f"   Правильно: <html lang=\"uk\">"
    )
    assert lang.lower().startswith("uk"), (
        f"❌ [{page_dir.name}] Атрибут lang має значення '{lang}', очікується 'uk'.\n"
        f"   Правильно: <html lang=\"uk\">"
    )


def test_has_head_tag(page_dir: Path):
    """Наявний тег <head>."""
    soup, _ = load_html(page_dir)
    assert soup.find("head") is not None, (
        f"❌ [{page_dir.name}] Відсутній тег <head>."
    )


def test_has_body_tag(page_dir: Path):
    """Наявний тег <body>."""
    soup, _ = load_html(page_dir)
    assert soup.find("body") is not None, (
        f"❌ [{page_dir.name}] Відсутній тег <body>."
    )


def test_meta_charset(page_dir: Path):
    """Наявний <meta charset='UTF-8'>."""
    soup, _ = load_html(page_dir)
    
    meta_charset = soup.find("meta", attrs={"charset": True})
    assert meta_charset is not None, (
        f"❌ [{page_dir.name}] Відсутній тег <meta charset>.\n"
        f"   Додай у <head>: <meta charset=\"UTF-8\">"
    )
    
    charset_value = meta_charset.get("charset", "").upper()
    assert "UTF" in charset_value and "8" in charset_value, (
        f"❌ [{page_dir.name}] charset має значення '{meta_charset.get('charset')}', "
        f"очікується 'UTF-8'."
    )


def test_has_title(page_dir: Path):
    """Наявний і непорожній <title>."""
    soup, _ = load_html(page_dir)
    
    title = soup.find("title")
    assert title is not None, (
        f"❌ [{page_dir.name}] Відсутній тег <title>.\n"
        f"   Додай у <head>: <title>Назва сторінки</title>"
    )
    assert title.get_text(strip=True), (
        f"❌ [{page_dir.name}] Тег <title> порожній.\n"
        f"   Вкажи назву розділу, наприклад: <title>Задзеркалля — Аліса в Задзеркаллі</title>"
    )


def test_css_link(page_dir: Path):
    """Підключений зовнішній CSS через <link rel='stylesheet'>."""
    soup, _ = load_html(page_dir)
    
    links = soup.find_all("link", rel=lambda r: r and "stylesheet" in r)
    assert links, (
        f"❌ [{page_dir.name}] Не знайдено підключення зовнішнього CSS.\n"
        f"   Додай у <head>: <link rel=\"stylesheet\" href=\"style.css\">"
    )
    
    # Перевіряємо, що href вказує на style.css
    hrefs = [l.get("href", "") for l in links]
    assert any("style.css" in h for h in hrefs), (
        f"❌ [{page_dir.name}] <link> підключено, але href не містить 'style.css'.\n"
        f"   Знайдені href: {hrefs}\n"
        f"   Переконайся: <link rel=\"stylesheet\" href=\"style.css\">"
    )
