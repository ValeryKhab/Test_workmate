"""Анализ рейтинга брендов"""

import csv
import argparse
from tabulate import tabulate


def read_csv(file_list):
    """
    Чтение данных из файлов
    
    Args:
        file_list (List[str]): Список путей к файлам

    Returns:
        data (List[Dict]): Список товаров, где каждый представлен словарём с ключами:
            - 'name' (str): Название товара
            - 'brand' (str): Название бренда
            - 'price' (float): Цена
            - 'rating' (float): Рейтинг
    """
    data = []
    for filename in file_list:
        try:
            with open(filename, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append({
                        'name': row['name'],
                        'brand': row['brand'],
                        'price': float(row['price']),
                        'rating': float(row['rating'])
                    })
        except FileNotFoundError:
            print(f"Ошибка: файл '{filename}' не найден.")
            return
        except Exception as e:
            print(f"Ошибка при чтении файла '{filename}': {e}")
            return
    return data

def average_rating_report(data):
    """
    Подсчет среднего рейтинга для каждого бренда
    
    Args:
        data (List[str]): Данные из файлов

    Returns:
        report (List[Tuple[str, float]]): Отчет (бренд, средний рейтинг)
    """
    brand_data = {}
    for item in data:
        brand = item['brand']
        rating = item['rating']
        if brand not in brand_data:
            brand_data[brand] = {'total_rating': 0, 'count': 0}
        brand_data[brand]['total_rating'] += rating
        brand_data[brand]['count'] += 1
    report = [
        (brand, round(data['total_rating'] / data['count'], 2))
        for brand, data in brand_data.items()
    ]
    return report

REPORTS = {
    "average-rating": {
        "func": average_rating_report,
        "headers": ["brand", "rating"]
    },
}

def main():
    """
    Главная функция для запуска скрипта из командной строки
    Парсит аргументы командной строки, считывает CSV-файлы, формирует отчёт и выводит в виде таблицы
    
    CLI Args:
        --files: Список CSV-файлов для обработки
        --report: Тип отчёта
    """
    parser = argparse.ArgumentParser(description="Формирование отчетов о рейтингах товаров")
    parser.add_argument("--files", nargs="+", required=True,
                        help="Пути к CSV-файлам с данными (можно несколько)")
    parser.add_argument("--report", required=True, choices=REPORTS.keys(),
                        help=f"Тип отчета ({', '.join(REPORTS.keys())})")
    args = parser.parse_args()
    try:
        data = read_csv(args.files)
        if not data:
            print("Нет данных для составления отчета")
            return
        report_type = REPORTS[args.report]
        report_func = report_type["func"]
        headers = report_type["headers"]
        report = report_func(data)
        if not report:
            print("Получен пустой отчет")
            return
        print(tabulate(report, headers, tablefmt="pretty", showindex=range(1, len(report)+1)))
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
