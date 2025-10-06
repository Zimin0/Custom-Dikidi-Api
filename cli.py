import sys
import argparse
from datetime import datetime

from entities.users import DikidiUser
from entities.datetime_slot import DateTimeSlot

from utils import DikidiApiClient
from services.authentication.service import AuthenticationService
from services.user.service import UserManager
from services.company.service import CompanyService 
from services.service.parsing_services_service import ParsingServicesService
from services.master.parsing_masters_service import ParsingMastersService  
from services.date.parsing_dates_service import ParsingDatesService  
from services.datetime_slot.parsing_datetime_slots_service import ParsingSlotsService
from services.booking.service import BookingService

def ask_yes_no(question: str, default: str | None = None) -> bool:
    # ask yes/no like linux prompts
    valid = {"y": True, "yes": True, "n": False, "no": False}
    if default not in (None, "y", "n"): raise ValueError("default must be None, 'y' or 'n'")
    if default is None:
        suffix = " [y/n] "
    elif default == "y":
        suffix = " [Y/n] "
    else:
        suffix = " [y/N] "
    while True:
        ans = input(question + suffix).strip().lower()
        if not ans and default is not None: return default == "y"
        if ans in valid: return valid[ans]
        print("please answer 'y' or 'n'.")

def ask_required(prompt: str, caster, validator, error_msg: str = "invalid input, try again"):
    # read input, cast, validate; loop until valid
    while True:
        raw = input(prompt).strip()
        try:
            val = caster(raw)
        except Exception:
            print(error_msg); continue
        if validator(val): return val
        print(error_msg)

def cast_int(s: str) -> int: return int(s)
def cast_str(s: str) -> str: return s.strip()
def cast_dt_strict(s: str) -> datetime: return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")  # strict dt
 
def validate_int(v) -> bool: return isinstance(v, int) # TODO: delete validation
def validate_str(v) -> bool: return isinstance(v, str) and len(v) > 0
def validate_dt(v) -> bool: return isinstance(v, datetime)

def choose_from(items: list, title: str, render) -> int:
    # print numbered list and return selected index (0-based)
    if not items:
        print(f"{title}: empty")
        return -1
    print(f"\n{title}:")

    for i, it in enumerate(items, 1):
        print(f"  {i}. {render(it)}")
        
    while True:
        raw = input("pick number: ").strip()
        if raw.isdigit():
            i = int(raw)
            if 1 <= i <= len(items): 
                return i - 1
        print("invalid choice, try again.")

def run_interactive() -> int:
    # init client and services
    client = DikidiApiClient()
    company_svc = CompanyService(client)
    services_svc = ParsingServicesService(client)
    masters_svc = ParsingMastersService(client)
    dates_svc = ParsingDatesService(client)
    datetimes_svc = ParsingSlotsService(client)

    auth_service = AuthenticationService()
    booking_svc = BookingService(client)

    # step 1: company
    company_id = ask_required("enter company id: ", cast_int, validate_int)
    company = company_svc.get_by_id(company_id)
    if not company:
        print(f"company {company_id} not found")
        return 1
    print(f"company: {getattr(company,'name', 'n/a')} (id={getattr(company,'id', company_id)})")

    # step 2: services
    services = services_svc.get_all_objects(company_id=company.id, category_id=None, amount=-1) or []
    sidx = choose_from(services, "available services", lambda s: f"{getattr(s,'name','?')} (id={getattr(s,'id','?')})")
    if sidx < 0: 
        return 1
    service = services[sidx]
    print(f"service selected: {getattr(service,'name','?')} (id={getattr(service,'id','?')})")

    # step 3: masters
    masters = masters_svc.get_all_objects(company_id=company.id, service_id=getattr(service,'id', None), amount=-1) or []
    midx = choose_from(masters, "available masters", lambda m: f"{getattr(m,'name','?')} (id={getattr(m,'id','?')})")
    if midx < 0: 
        return 1
    master = masters[midx]
    print(f"master selected: {getattr(master,'name','?')} (id={getattr(master,'id','?')})")

    # step 4-5: dates and datetimes
    dates_and_datetimes = {}
    dates = dates_svc.get_all_objects(company_id=company.id, service_id=service.id, master_id=master.id, amount=-1) or []
    for date in dates:
        slots = datetimes_svc.get_all_objects(company_id=company.id, service_id=service.id, master_id=master.id, date=date) or []
        dates_and_datetimes[date] = slots

    if dates:
        print("available dates:")
        didx = choose_from(dates, "available dates", lambda d: f"{getattr(d, "date_string", "?")} ({len(dates_and_datetimes[d])} free slots)")
        if didx < 0: 
            return 1
        date = dates[didx]
        print(f"date selected: {getattr(date, "date_string", "?")}")
        
    # step 5. datetime-slots
    slots = dates_and_datetimes[date]
    if slots:
        print("available slots:")
        sidx = choose_from(slots, "available slots", lambda s: f"{getattr(s, "slot_str", "?")}")
        if sidx < 0: 
            return 1
        slot = slots[sidx]
        print(f"slots selected: {getattr(slot, "date_string", "?")}")

    # summary + confirmation
    print("--------------------------------")
    print(f"Company: '{company.name}'({company.id})")
    print(f"Service: '{service.name}'({service.id})")
    print(f"Master: '{master.name}'({master.id})")
    print(f"Slot: {slot}")
    print("--------------------------------")

    if ask_yes_no("Book this slot?", default="y"):
        print("Need to login...")

        use_env = ask_yes_no("Get credentials from .env file?", default="y")
        if use_env:
            current_user = UserManager.read_from_env()
            session_hash = auth_service.auth(current_user)
        else:
            raise ValueError("Use .env file!!!")

        # phone = ask_required("Your phone number:", cast_str, validate_str)
        # password = ask_required("Your password:", cast_str, validate_str)

        booking_svc.book(
            company_id=company.id, 
            service_id=service.id, 
            master_id=master.id, 
            time_slot=slot,  # переписать на передачу строки а не объекта
            session_hash=session_hash,
            user=current_user
        )
        print("(+) Slot was booked.")
    else: 
        print("(x) aborted.")
        return 130
    
    return 0

def main() -> int:
    parser = argparse.ArgumentParser(description="Dikidi booking CLI")
    parser.add_argument("--company-id", type=int, required=False, help="company id")
    parser.add_argument("--category-id", type=int, required=False, help="category id")  # зарезервировано
    parser.add_argument("--service-id", type=int, required=False, help="service id")
    parser.add_argument("--master-id", type=int, required=False, help="master id")
    parser.add_argument("--date-time", required=False, help="datetime in 'YYYY-MM-DD HH:MM:SS'")

    # флаг как в требовании; по умолчанию True
    parser.add_argument(
        "--credentials-from-env",
        dest="credentials_from_env",
        action="store_true",
        default=True,
        help="read credentials from .env and authenticate (default: true)"
    )
    parser.add_argument(
        "--no-credentials-from-env",
        dest="credentials_from_env",
        action="store_false",
        help="disable reading credentials from .env"
    )

    args = parser.parse_args()

    # если нет company-id — предлагаем интерактивный режим
    if args.company_id is None:
        if ask_yes_no("no provided 'company-id'. start interactive mode?", default="y"):
            return run_interactive()
        else:
            return 130

    # базовая валидация обязательных для брони полей
    missing = [name for name, val in [
        ("service-id", args.service_id),
        ("master-id", args.master_id),
        ("date-time", args.date_time),
    ] if val is None]
    if missing:
        print(f"Missing required args for booking: {', '.join(missing)}")
        return 2

    # echo аргументов
    print("--------------------------------")
    print(f"company_id: {args.company_id}")
    print(f"category_id: {args.category_id}")
    print(f"service_id: {args.service_id}")
    print(f"master_id: {args.master_id}")
    print(f"datetime:   {args.date_time}")
    print(f"credentials_from_env: {args.credentials_from_env}")
    print("--------------------------------")

    if not ask_yes_no("Book this slot?", default="y"):
        print("(x) aborted.")
        return 130

    # инициализация сервисов
    client = DikidiApiClient()
    auth_service = AuthenticationService()
    booking_svc = BookingService(client)

    # аутентификация
    if args.credentials_from_env:
        current_user = UserManager.read_from_env()
        session_hash = auth_service.auth(current_user)
    else:
        raise ValueError("Use .env file or implement non-env credential flow.")

    # парсинг слота
    try:
        slot_dt = cast_dt_strict(args.date_time)
    except Exception:
        print("Invalid --date-time format. Expected 'YYYY-MM-DD HH:MM:SS'.")
        return 2

    # бронь
    booking_svc.book(
        company_id=args.company_id,
        service_id=args.service_id,
        master_id=args.master_id,
        time_slot=slot_dt,           # можно адаптировать, если book ожидает строку
        session_hash=session_hash,   # передаём как в интерактивной части
        user=current_user
    )
    print("(+) Slot was booked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
