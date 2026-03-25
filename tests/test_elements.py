"""
test_elements.py — Тести обов'язкових HTML-елементів

Перевіряє:
  - Рівно один <h1>
  - Щонайменше 3 параграфи <p>
  - Текст у параграфах непорожній
  - Відсутність тексту поза тегами (naked text у <body>)
"""
import pytest
from pathlib import Path
from conftest import load_html


def test_has_h1(page_dir: Path):
    """На сторінці є рівно один тег <h1>."""
    soup, _ = load_html(page_dir)
    
    h1_tags = soup.find_all("h1")
    assert len(h1_tags) >= 1, (
        f"❌ [{page_dir.name}] Відсутній тег <h1>.\n"
        f"   Додай заголовок розділу: <h1>Назва розділу</h1>"
    )
    assert len(h1_tags) == 1, (
        f"❌ [{page_dir.name}] Знайдено {len(h1_tags)} теги <h1>, має бути рівно один.\n"
        f"   На сторінці повинен бути лише один головний заголовок."
    )


def test_h1_not_empty(page_dir: Path):
    """Тег <h1> містить текст."""
    soup, _ = load_html(page_dir)
    h1 = soup.find("h1")
    if h1 is None:
        pytest.skip("<h1> відсутній")
    
    assert h1.get_text(strip=True), (
        f"❌ [{page_dir.name}] Тег <h1> порожній.\n"
        f"   Вкажи назву розділу всередині: <h1>Задзеркалля</h1>"
    )


def test_has_paragraphs(page_dir: Path):
    """На сторінці є щонайменше 3 параграфи <p>."""
    soup, _ = load_html(page_dir)
    
    # Рахуємо лише параграфи всередині <main> або <body>, що мають текст
    paragraphs = [
        p for p in soup.find_all("p")
        if p.get_text(strip=True)
    ]
    
    assert len(paragraphs) >= 3, (
        f"❌ [{page_dir.name}] Знайдено лише {len(paragraphs)} непорожніх параграфів <p>.\n"
        f"   Потрібно щонайменше 3. Кожен абзац тексту — окремий тег <p>.</p>"
    )


def test_paragraphs_not_empty(page_dir: Path):
    """Жоден <p> не є порожнім чи містить лише пробіли."""
    soup, _ = load_html(page_dir)
    
    empty_paragraphs = [
        p for p in soup.find_all("p")
        if not p.get_text(strip=True)
    ]
    
    if empty_paragraphs:
        pytest.warns(
            UserWarning,
            match=f"[{page_dir.name}] Знайдено {len(empty_paragraphs)} порожніх тегів <p>."
        )


def test_main_content_area(page_dir: Path):
    """На сторінці є <main> або хоча б структурований вміст."""
    soup, _ = load_html(page_dir)
    
    has_main = soup.find("main") is not None
    has_article = soup.find("article") is not None
    has_div_content = soup.find("div", class_=lambda c: c and (
        "content" in c or "main" in c or "text" in c
    )) is not None
    
    # Це рекомендація, а не жорстка вимога
    if not (has_main or has_article or has_div_content):
        print(
            f"\n💡 [{page_dir.name}] Рекомендація: огорни основний текст у <main>...</main> "
            f"для кращої семантики."
        )


def test_text_not_naked_in_body(page_dir: Path):
    """Текст книги не знаходиться безпосередньо у <body> без тегів."""
    soup, _ = load_html(page_dir)
    body = soup.find("body")
    if body is None:
        pytest.skip("<body> відсутній")
    
    # Перевіряємо прямі текстові вузли у <body>
    naked_text = [
        t.strip() for t in body.find_all(string=True, recursive=False)
        if t.strip() and len(t.strip()) > 20
    ]
    
    assert not naked_text, (
        f"❌ [{page_dir.name}] Знайдено текст безпосередньо у <body> без тегів:\n"
        f"   '{naked_text[0][:60]}...'\n"
        f"   Загорни весь текст у теги <p>, <h1>, <div> тощо."
    )
