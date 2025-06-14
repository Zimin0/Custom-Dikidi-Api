import sys
from entities.companies import Company

from logger_init import logger

def select_option(options, prompt="Выберите вариант"):
    """Отображает список вариантов и запрашивает выбор пользователя."""
    if not options:
        print("Нет доступных вариантов.")
        return None
    
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    while True:
        try:
            choice = int(input(f"{prompt} (1-{len(options)}): "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print("Ошибка: Введите число из списка.")
        except ValueError:
            print("Ошибка: Введите число.")

def main():
    company_id = input("Введите ID компании: ") or "1554154" #or "550001"
    
    # Создание объекта компании
    company = Company(id=int(company_id))
    print(f"Парсим информацию о компании с id '{company_id}'...")
    company.parse_company_info()

    print(f"Компания: {company.name}")
    
    # Получение списка категорий
    print("Загружаем категории...")
    categories = company.get_its_categories()
    if not categories:
        print("Категории не найдены.")
        sys.exit(1)

    selected_category = select_option(categories, "Выберите категорию")
    if not selected_category:
        sys.exit(1)

    print(f"Выбрана категория: {selected_category.name}")

    # Получение списка сервисов
    print("Загружаем услуги...")
    services = selected_category.get_its_services(company.id)
    if not services:
        print("Услуги не найдены.")
        sys.exit(1)

    selected_service = select_option(services, "Выберите услугу")
    if not selected_service:
        sys.exit(1)

    print(f"Выбрана услуга: {selected_service.name}")

    # Получение списка мастеров
    print("Загружаем мастеров...")
    masters = selected_service.get_its_masters(company.id)
    if not masters:
        print("Мастера не найдены.")
        sys.exit(1)

    selected_master = select_option(masters, "Выберите мастера")
    if not selected_master:
        sys.exit(1)

    print(f"Выбран мастер: {selected_master.username}")

    # Получение доступных дат
    print("Загружаем доступные даты...")
    dates = selected_master.get_its_dates(company.id, selected_service.id)
    logger.debug(f"{dates=}")
    if not dates:
        print("Доступных дат нет.")
        sys.exit(1)
    
    selected_date = select_option(dates, "Выберите дату")
    if not selected_date:
        sys.exit(1)

    print(f"Выбрана дата: {selected_date}")
    
    # Получение доступных временных интервалов
    print("Загружаем доступные временные интервалы...")
    times = selected_date.get_its_times(company.id, selected_service.id, selected_master.id)
    if not times:
        print("Нет доступных временных интервалов.")
        sys.exit(1)

    selected_time = select_option(times, "Выберите время")
    if not selected_time:
        sys.exit(1)

    print(f"Выбран временной интервал: {selected_time}")
    print("\Просмотр завершен!\n")

if __name__ == "__main__":
    main()
