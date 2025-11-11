# Test_workmate
Тестовое задание: Анализ рейтинга брендов

## Структура проекта:
- `report.py` — основной скрипт для формирования отчётов
- `tests/` - папка с тестами, выполненными с помощью `pytest` 
- `tests/test_files/` - CSV-файлы для тестов

## Параметры:
- `--files` — один или несколько CSV-файлов с товарами
- `--report` — тип отчета. Доступные варианты:
  - `average-rating` — средний рейтинг по брендам

## Запуск скрипта:
Для проверки сркипта можно использовать следующую команду (из папки проекта):  
```python report.py --files products1.csv products2.csv --report average-rating```
Пример результата работы программы представлен на картинке:    
  
<img width="585" height="142" alt="image" src="https://github.com/user-attachments/assets/e3154da5-4038-4484-a94b-383a9a044e94" />  

## Запуск тестов с отображением покрытия:  
Для запуска тестов с отображением покрытия можно использовать следующую команду:  
```pytest --cov=report tests/```  
С просмотром непокрытых строк:  
```pytest --cov=report tests/ --cov-report=term-missing```  
Отчет по покрытию представлен на картинке:  

<img width="585" height="163" alt="image" src="https://github.com/user-attachments/assets/b7272538-79d8-4efc-8e92-58a98006db31" />

## Расширяемость кода:
Добавление новых отчетов устроено следующим образом:  
### 1. Создать функцию генерации отчета  
Функция должна принимать список товаров (как возвращает функция `read_csv`) и возвращать список кортежей. Пример новой функции для отчета:  
```
def max_price_report(data):
    """
    Подсчет максимальной цены для каждого бренда
    
    Args:
        data (List[str]): Данные из файлов

    Returns:
        report (List[Tuple[str, float]]): Отчет (бренд, максимальная цена)
    """
    brand_data = {}
    for item in data:
        if item['brand'] not in brand_data:
            brand_data[item['brand']] = 0
        brand_data[item['brand']] = max(brand_data[item['brand']], item['price'])
    
    report = [(b, v) for b, v in brand_data.items()]
    return sorted(report, key=lambda x: x[1], reverse=True)
```
### 2. Добавить отчёт REPORTS  
В файле `report.py` есть словарь `REPORTS`:  
```
REPORTS = {
    "average-rating": {
        "func": average_rating_report,
        "headers": ["brand", "rating"]
    },
}
```  
Чтобы подключить новый отчёт, добавьте новый элемент (функция и заголовки таблицы):    
```REPORTS["max-price"] = {"func": max_price_report, "headers": ["brand", "price"]}```    
Новый словарь:  
```
REPORTS = {
    "average-rating": {
        "func": average_rating_report,
        "headers": ["brand", "rating"]
    },
    "max-price": {
        "func": max_price_report,
        "headers": ["brand", "price"]
    },
}
```  
### 3. Использовать отчёт через командную строку  
После добавления в REPORTS новый отчёт становится доступен для запуска:  
```python report.py --files products1.csv products2.csv --report max-price```  
Скрипт автоматически выберет функцию и заголовки для таблицы
