"""
conftest.py — спільні фікстури та утиліти для тестів
"""
import pytest
import os
from pathlib import Path
from bs4 import BeautifulSoup


# ── Шлях до кореня проєкту ──────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent


def get_all_student_pages() -> list[Path]:
    """Повертає список усіх папок сторінок (крім example)."""
    pages_dir = ROOT / "pages"
    return [
        p for p in pages_dir.iterdir()
        if p.is_dir() and p.name != "example"
    ]


def get_pages_to_test() -> list[Path]:
    """
    Якщо задана змінна середовища CHANGED_PAGES — тестує тільки їх.
    Інакше — всі сторінки.
    """
    changed = os.environ.get("CHANGED_PAGES", "")
    if changed:
        pages = []
        for name in changed.split(","):
            name = name.strip()
            p = ROOT / "pages" / name
            if p.is_dir():
                pages.append(p)
        return pages
    return get_all_student_pages()


def load_html(page_dir: Path) -> BeautifulSoup:
    """Завантажує і парсить index.html зі сторінки."""
    html_file = page_dir / "index.html"
    assert html_file.exists(), (
        f"Файл index.html не знайдено у {page_dir.name}/\n"
        f"Переконайся, що файл називається саме 'index.html'"
    )
    content = html_file.read_text(encoding="utf-8")
    return BeautifulSoup(content, "html.parser"), content


def load_expected_text(page_dir: Path) -> str:
    """Завантажує очікуваний текст для сторінки."""
    page_name = page_dir.name  # наприклад: page_01
    text_file = ROOT / "text" / "pages" / f"{page_name}.txt"
    if not text_file.exists():
        return ""
    return text_file.read_text(encoding="utf-8")


# ── Параметризовані фікстури ─────────────────────────────────────────────────

def pytest_generate_tests(metafunc):
    """Автоматично параметризує тести для кожної сторінки студента."""
    if "page_dir" in metafunc.fixturenames:
        pages = get_pages_to_test()
        if not pages:
            pytest.skip("Немає сторінок для тестування")
        metafunc.parametrize(
            "page_dir",
            pages,
            ids=[p.name for p in pages]
        )
