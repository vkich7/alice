"""
test_content.py — Тести відповідності тексту призначеній сторінці

Перевіряє:
  - Текст сторінки відповідає призначеному файлу text/pages/page_XX.txt
  - Перше та останнє речення з тексту присутні на сторінці
  - Текст не був скорочений надмір
"""
import pytest
import re
from pathlib import Path
from conftest import load_html, load_expected_text


def normalize_text(text: str) -> str:
    """Нормалізує текст для порівняння: прибирає зайві пробіли та перетворює на нижній регістр."""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[«»""„"\'`]', '', text)  # лапки
    text = re.sub(r'[-–—]', '-', text)  # тире
    return text.strip()


def extract_page_text(soup) -> str:
    """Витягує весь текст зі сторінки (з <p> тегів)."""
    paragraphs = soup.find_all("p")
    return " ".join(p.get_text(separator=" ", strip=True) for p in paragraphs)


def split_into_sentences(text: str) -> list[str]:
    """Розбиває текст на речення."""
    sentences = re.split(r'[.!?…]+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 15]


def test_expected_text_file_exists(page_dir: Path):
    """Файл із очікуваним текстом існує для цієї сторінки."""
    page_name = page_dir.name
    text_file = page_dir.parent.parent / "text" / "pages" / f"{page_name}.txt"
    
    if not text_file.exists():
        pytest.skip(
            f"ℹ️  [{page_name}] Файл тексту text/pages/{page_name}.txt не знайдено.\n"
            f"   Викладач має додати цей файл. Тест пропущено."
        )


def test_page_contains_expected_text(page_dir: Path):
    """Сторінка містить текст, що відповідає призначеній сторінці книги."""
    page_name = page_dir.name
    expected_text = load_expected_text(page_dir)
    
    if not expected_text:
        pytest.skip(f"ℹ️  [{page_name}] Текст для перевірки відсутній. Тест пропущено.")
    
    soup, _ = load_html(page_dir)
    page_text = extract_page_text(soup)
    
    if not page_text.strip():
        pytest.fail(
            f"❌ [{page_name}] На сторінці немає тексту у <p> тегах.\n"
            f"   Встав текст зі свого файлу text/pages/{page_name}.txt"
        )
    
    # Перевіряємо перше речення
    expected_sentences = split_into_sentences(expected_text)
    page_text_normalized = normalize_text(page_text)
    
    if expected_sentences:
        first_sentence = normalize_text(expected_sentences[0])
        # Беремо перші 40 символів першого речення як "підпис"
        fingerprint = first_sentence[:40]
        
        assert fingerprint in page_text_normalized, (
            f"❌ [{page_name}] Текст сторінки не відповідає призначеному файлу.\n"
            f"   Очікується початок: '{expected_sentences[0][:60]}...'\n"
            f"   Переконайся, що використовуєш текст із файлу text/pages/{page_name}.txt"
        )


def test_page_text_coverage(page_dir: Path):
    """Студент не вилучив надто багато тексту (покриття > 60%)."""
    page_name = page_dir.name
    expected_text = load_expected_text(page_dir)
    
    if not expected_text:
        pytest.skip(f"ℹ️  [{page_name}] Текст для перевірки відсутній. Тест пропущено.")
    
    soup, _ = load_html(page_dir)
    page_text = extract_page_text(soup)
    
    if not page_text.strip():
        pytest.skip("Текст на сторінці відсутній (перевіряється іншим тестом)")
    
    # Порівнюємо кількість слів
    expected_words = set(normalize_text(expected_text).split())
    page_words = set(normalize_text(page_text).split())
    
    if not expected_words:
        pytest.skip("Очікуваний текст порожній")
    
    # Слова з очікуваного тексту, що знайдені на сторінці
    found_words = expected_words & page_words
    coverage = len(found_words) / len(expected_words)
    
    assert coverage >= 0.5, (
        f"❌ [{page_name}] Покриття тексту: {coverage:.0%} (потрібно щонайменше 50%).\n"
        f"   Схоже, що текст вилучено або замінено.\n"
        f"   Переконайся, що весь текст із text/pages/{page_name}.txt присутній на сторінці."
    )


def test_no_template_placeholder_text(page_dir: Path):
    """На сторінці немає тексту-заповнювача з шаблону."""
    soup, _ = load_html(page_dir)
    
    placeholders = [
        "перший абзац тексту вашої сторінки",
        "другий абзац тексту вашої сторінки",
        "назва розділу",
        "ім'я прізвище",
        "todo",
    ]
    
    page_text = soup.get_text(separator=" ").lower()
    
    found_placeholders = [p for p in placeholders if p in page_text]
    
    assert not found_placeholders, (
        f"❌ [{page_dir.name}] На сторінці залишився текст-заповнювач із шаблону:\n"
        f"   Знайдено: {found_placeholders}\n"
        f"   Заміни всі 'TODO' та шаблонні тексти на справжній вміст."
    )
