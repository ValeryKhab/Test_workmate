import os
import sys
import pytest
from report import read_csv, average_rating_report, main

TEST_CSV = os.path.join(os.path.dirname(__file__), "test_files", "products1.csv")
TEST_CSV_2 = os.path.join(os.path.dirname(__file__), "test_files", "products2.csv")
TEST_CSV_3 = os.path.join(os.path.dirname(__file__), "test_files", "empty.csv")

def test_read_csv_single():
    """Чтение одного файла"""
    items = read_csv([TEST_CSV])
    assert isinstance(items, list)
    assert len(items) > 0
    for item in items:
        assert "name" in item
        assert "brand" in item
        assert "price" in item
        assert "rating" in item

def test_read_csv_multiple():
    """Чтение нескольких файлов"""
    items = read_csv([TEST_CSV, TEST_CSV_2])
    assert isinstance(items, list)
    assert len(items) > 0
    for item in items:
        assert "name" in item
        assert "brand" in item
        assert "price" in item
        assert "rating" in item

def test_read_csv_files_file_not_found():
    """Чтение несуществующего файла (неверный путь)"""
    items = read_csv(["filenotfound.csv"])
    assert items is None

def test_average_rating_report():
    """Генерация отчета"""
    items = read_csv([TEST_CSV])
    report = average_rating_report(items)
    assert isinstance(report, list)
    assert all(isinstance(r, tuple) and len(r) == 2 for r in report)
    for brand, rating in report:
        assert isinstance(brand, str)
        assert isinstance(rating, float)

def test_main_average_rating(monkeypatch, capsys):
    """Запуск и работа скрипта с заполненным файлом"""
    monkeypatch.setattr(sys, 'argv', ['main.py', '--files', 'tests/test_files/products1.csv', '--report', 'average-rating'])
    main()
    captured = capsys.readouterr()
    assert "brand" in captured.out
    assert "rating" in captured.out

def test_main_empty_average_rating(monkeypatch, capsys):
    """Запуск и работа скрипта с пустым файлом"""
    monkeypatch.setattr(sys, 'argv', ['main.py', '--files', 'tests/test_files/empty.csv', '--report', 'average-rating'])
    main()
    captured = capsys.readouterr()
    assert "Нет данных для составления отчета" in captured.out
    