# Run with: docker-compose exec backend python -m app.utils.seed_data

from datetime import datetime
from app.database import SessionLocal
from app.models import (
    Project, ProjectStatus,
    Task, TaskStatus, TaskPriority,
    Resource, ResourceType, ResourceStatus,
    Budget
)
from app.services.similarity_service import SimilarityService


def seed_database():
    db = SessionLocal()
    try:
        print("Seeding database...")

        projects_data = [
            # 0 — ПНХЗ: теплообменники
            {
                "name": "Ревизия и ремонт теплообменного оборудования ПНХЗ (95 ед.)",
                "description": (
                    "Плановый ремонт теплообменного оборудования ПНХЗ: "
                    "разборка, чистка, замена трубных пучков, ревизия корпусов, сборка 95 теплообменников. "
                    "Замена пароперегревателя Е-402 ПГПН. "
                    "Сварных стыков: 480. Прокладок/фланцев: 3200 шт. КИП и ЗРА: 520 комплектов."
                ),
                "status": ProjectStatus.COMPLETED,
                "start_date": datetime(2022, 4, 11),
                "planned_end_date": datetime(2022, 6, 5),
                "actual_end_date": datetime(2022, 6, 4),
                "total_budget": 350_000_000.0,
                "spent_amount": 342_000_000.0,
                "location": "Павлодар",
                "customer": "ПНХЗ",
            },
            # 1 — ПНХЗ: колонны и насосы
            {
                "name": "Замена колонного оборудования и насосных агрегатов ПНХЗ",
                "description": (
                    "Замена ёмкости Е-102 ПГПН, сепаратора С-302 ПГПН, "
                    "замена 11 тарелок колонны К-102 ПГПН, 6 единиц насосного оборудования, "
                    "монтаж ПКУ — 46 единиц. "
                    "Ревизия и ремонт ёмкостного и колонного оборудования — 166 единиц. "
                    "Демонтаж-монтаж ТРО — более 1400 шт."
                ),
                "status": ProjectStatus.COMPLETED,
                "start_date": datetime(2022, 4, 15),
                "planned_end_date": datetime(2022, 6, 20),
                "actual_end_date": datetime(2022, 6, 18),
                "total_budget": 280_000_000.0,
                "spent_amount": 272_000_000.0,
                "location": "Павлодар",
                "customer": "ПНХЗ",
            },
            # 2 — ПНХЗ: печи
            {
                "name": "Ревизия технологических печей и замена конвекций ПНХЗ (30 ед.)",
                "description": (
                    "Ревизия и ремонт 30 единиц технологических печей ПНХЗ: "
                    "замена горелок, ревизия змеевиков, восстановление огнеупорной футеровки. "
                    "Замена конвекционных частей 2 технологических печей. "
                    "Чистка технологического оборудования — 145 единиц. "
                    "Задействовано: ИТР — 83 чел., рабочие — 1292 чел., техника — 50 ед."
                ),
                "status": ProjectStatus.COMPLETED,
                "start_date": datetime(2022, 4, 1),
                "planned_end_date": datetime(2022, 6, 30),
                "actual_end_date": datetime(2022, 6, 28),
                "total_budget": 420_000_000.0,
                "spent_amount": 412_000_000.0,
                "location": "Павлодар",
                "customer": "ПНХЗ",
            },
            # 3 — АНПЗ: трубопровод DR-201 CCR
            {
                "name": "Замена трубопровода-осушителя DR-201 (CCR) АНПЗ",
                "description": (
                    "Замена трубопровода-осушителя DR-201 из нержавеющей стали "
                    "на установке CCR (каталитического риформинга) АНПЗ. "
                    "Диаметр от Ду20 до Ду300 мм, длина 152 метра. "
                    "Демонтаж старого, сварка и монтаж нового трубопровода. НК сварных швов 100%. "
                    "Повышена надёжность работы установки каталитического риформинга."
                ),
                "status": ProjectStatus.COMPLETED,
                "start_date": datetime(2022, 9, 10),
                "planned_end_date": datetime(2022, 10, 20),
                "actual_end_date": datetime(2022, 10, 18),
                "total_budget": 65_000_000.0,
                "spent_amount": 63_500_000.0,
                "location": "Атырау",
                "customer": "АНПЗ",
            },
            # 4 — АНПЗ: циклоны R-105 ФКК
            {
                "name": "Замена 4 циклонов регенератора R-105 (ФКК) АНПЗ",
                "description": (
                    "Замена 4 циклонов на регенераторе R-105 установки "
                    "каталитического крекинга (ФКК) АНПЗ на высотной отметке до 60 м. "
                    "Работа выполнялась одновременно изнутри и снаружи аппарата. "
                    "Исключён риск аварийного останова установки реакторного блока ФКК."
                ),
                "status": ProjectStatus.COMPLETED,
                "start_date": datetime(2022, 9, 5),
                "planned_end_date": datetime(2022, 10, 15),
                "actual_end_date": datetime(2022, 10, 14),
                "total_budget": 95_000_000.0,
                "spent_amount": 92_000_000.0,
                "location": "Атырау",
                "customer": "АНПЗ",
            },
            # 5 — АНПЗ: клапан реактора R-104 ФКК
            {
                "name": "Замена основного клапана реактора R-104 (ФКК) АНПЗ",
                "description": (
                    "Полная замена основного клапана реактора R-104 "
                    "установки каталитического крекинга (ФКК) АНПЗ, "
                    "включая станцию управления гидравлическим оборудованием. "
                    "Весь комплекс: подбор оборудования, логистика, монтаж, предпусковая наладка. "
                    "Повышена надёжность работы реакторного блока ФКК."
                ),
                "status": ProjectStatus.COMPLETED,
                "start_date": datetime(2022, 9, 1),
                "planned_end_date": datetime(2022, 11, 10),
                "actual_end_date": datetime(2022, 11, 10),
                "total_budget": 210_000_000.0,
                "spent_amount": 208_000_000.0,
                "location": "Атырау",
                "customer": "АНПЗ",
            },
            # 6 — АНПЗ: теплообменники АВТ-2
            {
                "name": "Замена теплообменников Т-6, Т-23, Т-26, Т-28 (АВТ-2) АНПЗ",
                "description": (
                    "Полная замена теплообменных аппаратов Т-6, Т-23, Т-26, Т-28 "
                    "и трубопроводов обвязки на установке АВТ-2 "
                    "(атмосферно-вакуумной перегонки нефти) АНПЗ. "
                    "Повышена производительность установки и качество продукции. "
                    "Масса заменённого оборудования — более 120 тонн."
                ),
                "status": ProjectStatus.COMPLETED,
                "start_date": datetime(2023, 9, 5),
                "planned_end_date": datetime(2023, 10, 2),
                "actual_end_date": datetime(2023, 10, 1),
                "total_budget": 380_000_000.0,
                "spent_amount": 374_000_000.0,
                "location": "Атырау",
                "customer": "АНПЗ",
            },
            # 7 — АНПЗ: конвекционная часть печи П-1 АВТ-2 ← KEY for PDF demo
            {
                "name": "Замена конвекционной части печи П-1 (АВТ-2) АНПЗ",
                "description": (
                    "Замена конвекционной секции трубчатой печи П-1 "
                    "установки АВТ-2 (атмосферно-вакуумной перегонки нефти) АНПЗ (Атырау). "
                    "Демонтаж старой конвекционной части, монтаж новой с заменой трубных змеевиков, "
                    "регенеративных труб, несущих конструкций и арматуры. "
                    "Ранее выявленный дефект устранён, срок эксплуатации оборудования существенно продлён. "
                    "Гидроиспытания, сушка огнеупорной футеровки по температурному графику, пуск. "
                    "Сварных стыков: 312. Задействовано: 85 специалистов."
                ),
                "status": ProjectStatus.COMPLETED,
                "start_date": datetime(2023, 9, 1),
                "planned_end_date": datetime(2023, 10, 2),
                "actual_end_date": datetime(2023, 10, 2),
                "total_budget": 520_000_000.0,
                "spent_amount": 514_000_000.0,
                "location": "Атырау",
                "customer": "АНПЗ",
            },
            # 8 — АНПЗ: реакторы CCR R-101, R-104
            {
                "name": "Модернизация реакторов CCR R-101 и R-104 АНПЗ",
                "description": (
                    "Модернизация реакторов R-101 и R-104 установки "
                    "непрерывного каталитического риформинга (CCR) АНПЗ: "
                    "замена внутренних устройств на более производительные. "
                    "Повышены качество и производительность технологической установки."
                ),
                "status": ProjectStatus.COMPLETED,
                "start_date": datetime(2023, 9, 5),
                "planned_end_date": datetime(2023, 9, 28),
                "actual_end_date": datetime(2023, 9, 27),
                "total_budget": 180_000_000.0,
                "spent_amount": 176_000_000.0,
                "location": "Атырау",
                "customer": "АНПЗ",
            },
            # 9 — АНПЗ: реакторы УДГ
            {
                "name": "Замена конусных частей реакторов УДГ Р-1—Р-4 АНПЗ",
                "description": (
                    "Замена конусных частей реакторов Р-1, Р-2, Р-3, Р-4 "
                    "установки гидроочистки дизельного топлива (УДГ) АНПЗ. "
                    "Устранены ранее выявленные дефекты корпуса реакторов. "
                    "Исключён риск аварийного останова установки."
                ),
                "status": ProjectStatus.COMPLETED,
                "start_date": datetime(2023, 9, 1),
                "planned_end_date": datetime(2023, 10, 2),
                "actual_end_date": datetime(2023, 10, 2),
                "total_budget": 130_000_000.0,
                "spent_amount": 127_000_000.0,
                "location": "Атырау",
                "customer": "АНПЗ",
            },
            # 10 — АНПЗ: модернизация КТ-1 (ongoing)
            {
                "name": "Модернизация компрессорной станции КТ-1 АНПЗ",
                "description": (
                    "Модернизация компрессорной станции КТ-1 на АНПЗ: "
                    "замена морально и физически устаревшего оборудования (с 1981 г.) "
                    "на центробежные компрессоры жирного газа Hitachi. "
                    "Оснащение АСУ ТП, антипомпажной защитой, диагностикой. "
                    "Интеграция установок порошкового пожаротушения и сухого газового уплотнения. "
                    "Прогнозируемая экономия > 120 млн тенге в год."
                ),
                "status": ProjectStatus.IN_PROGRESS,
                "start_date": datetime(2023, 6, 1),
                "planned_end_date": datetime(2025, 7, 31),
                "total_budget": 850_000_000.0,
                "spent_amount": 620_000_000.0,
                "location": "Атырау",
                "customer": "АНПЗ",
            },
        ]

        projects = []
        for proj_data in projects_data:
            project = Project(**proj_data)
            db.add(project)
            projects.append(project)
        db.commit()
        print(f"Created {len(projects)} projects")
        for proj in projects:
            db.refresh(proj)

        # ---- Tasks ----

        tasks_p0 = [
            {"project_id": projects[0].id, "name": "Подготовка и вывод теплообменников из работы",
             "description": "Отключение, дренаж, продувка, установка заглушек на 95 аппаратах",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2022, 4, 11), "planned_end_date": datetime(2022, 4, 18),
             "actual_end_date": datetime(2022, 4, 18), "progress_percentage": 100.0,
             "assigned_to": "Бригада подготовки"},
            {"project_id": projects[0].id, "name": "Разборка, чистка и дефектовка (95 ед.)",
             "description": "Гидроструйная чистка, вскрытие, дефектоскопия трубных пучков и корпусов",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2022, 4, 19), "planned_end_date": datetime(2022, 5, 15),
             "actual_end_date": datetime(2022, 5, 14), "progress_percentage": 100.0,
             "assigned_to": "Слесари-ремонтники"},
            {"project_id": projects[0].id, "name": "Замена трубных пучков и ревизия корпусов",
             "description": "Установка новых пучков, развальцовка труб, ревизия фланцев и прокладок",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2022, 5, 15), "planned_end_date": datetime(2022, 5, 30),
             "actual_end_date": datetime(2022, 5, 29), "progress_percentage": 100.0,
             "assigned_to": "Монтажники + сварщики НАКС"},
            {"project_id": projects[0].id, "name": "Гидроиспытания и ввод в работу",
             "description": "Опрессовка на 1.25Р, снятие заглушек, подключение, пуск",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2022, 5, 30), "planned_end_date": datetime(2022, 6, 4),
             "actual_end_date": datetime(2022, 6, 4), "progress_percentage": 100.0,
             "assigned_to": "Испытательная бригада"},
        ]

        tasks_p1 = [
            {"project_id": projects[1].id, "name": "Вывод из работы и подготовка оборудования",
             "description": "Остановка, дренаж, продувка Е-102, С-302, К-102, насосов",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2022, 4, 15), "planned_end_date": datetime(2022, 4, 22),
             "actual_end_date": datetime(2022, 4, 22), "progress_percentage": 100.0,
             "assigned_to": "Бригада подготовки"},
            {"project_id": projects[1].id, "name": "Замена тарелок колонны К-102 (11 шт.) и ревизия",
             "description": "Вскрытие колонны, демонтаж/монтаж 11 тарелок, контроль сварных швов",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2022, 4, 23), "planned_end_date": datetime(2022, 5, 20),
             "actual_end_date": datetime(2022, 5, 18), "progress_percentage": 100.0,
             "assigned_to": "Монтажники"},
            {"project_id": projects[1].id, "name": "Замена Е-102, С-302 и 6 насосных агрегатов",
             "description": "Демонтаж и монтаж новых аппаратов и насосов, обвязка, центровка",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2022, 5, 1), "planned_end_date": datetime(2022, 6, 10),
             "actual_end_date": datetime(2022, 6, 8), "progress_percentage": 100.0,
             "assigned_to": "Слесари-ремонтники + монтажники"},
            {"project_id": projects[1].id, "name": "Монтаж ПКУ (46 ед.) и испытания",
             "description": "Монтаж пружинных компенсирующих устройств, гидроиспытания, пуск",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2022, 6, 10), "planned_end_date": datetime(2022, 6, 18),
             "actual_end_date": datetime(2022, 6, 18), "progress_percentage": 100.0,
             "assigned_to": "Монтажники"},
        ]

        tasks_p2 = [
            {"project_id": projects[2].id, "name": "Подготовка печей к ремонту (30 ед.)",
             "description": "Охлаждение, продувка, установка лесов, наряды-допуски",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2022, 4, 1), "planned_end_date": datetime(2022, 4, 10),
             "actual_end_date": datetime(2022, 4, 10), "progress_percentage": 100.0,
             "assigned_to": "Бригады подготовки"},
            {"project_id": projects[2].id, "name": "Ревизия горелок и змеевиков (30 печей)",
             "description": "Разборка горелок, замена форсунок, ревизия трубных змеевиков, дефектоскопия",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2022, 4, 11), "planned_end_date": datetime(2022, 5, 31),
             "actual_end_date": datetime(2022, 5, 28), "progress_percentage": 100.0,
             "assigned_to": "Слесари КИПиА + огнеупорщики"},
            {"project_id": projects[2].id, "name": "Замена конвекционных частей (2 печи)",
             "description": "Демонтаж старых конвекций, монтаж новых с заменой трубных секций и опорных конструкций",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2022, 5, 1), "planned_end_date": datetime(2022, 6, 20),
             "actual_end_date": datetime(2022, 6, 18), "progress_percentage": 100.0,
             "assigned_to": "Сварщики НАКС + монтажники"},
            {"project_id": projects[2].id, "name": "Чистка оборудования (145 ед.) и пуск печей",
             "description": "Гидроструйная чистка 145 единиц, сушка футеровки, выход на рабочий режим",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2022, 6, 19), "planned_end_date": datetime(2022, 6, 28),
             "actual_end_date": datetime(2022, 6, 28), "progress_percentage": 100.0,
             "assigned_to": "Технологи"},
        ]

        tasks_p3 = [
            {"project_id": projects[3].id, "name": "Демонтаж старого трубопровода DR-201",
             "description": "Снятие изоляции, резка и демонтаж 152 м трубопровода нержавеющая сталь Ду20-300",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2022, 9, 10), "planned_end_date": datetime(2022, 9, 20),
             "actual_end_date": datetime(2022, 9, 19), "progress_percentage": 100.0,
             "assigned_to": "Монтажники"},
            {"project_id": projects[3].id, "name": "Сварка и монтаж нового трубопровода (152 м)",
             "description": "Сварка труб из нержавеющей стали, монтаж опор и подвесок, фланцевые соединения",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2022, 9, 20), "planned_end_date": datetime(2022, 10, 10),
             "actual_end_date": datetime(2022, 10, 9), "progress_percentage": 100.0,
             "assigned_to": "Сварщики НАКС + монтажники"},
            {"project_id": projects[3].id, "name": "НК сварных соединений и гидроиспытания",
             "description": "Радиографический контроль 100% стыков, гидроиспытание на 1.25Р, устранение замечаний",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2022, 10, 10), "planned_end_date": datetime(2022, 10, 18),
             "actual_end_date": datetime(2022, 10, 18), "progress_percentage": 100.0,
             "assigned_to": "Лаборатория НК"},
        ]

        tasks_p4 = [
            {"project_id": projects[4].id, "name": "Вывод регенератора из работы и установка лесов",
             "description": "Остановка R-105, продувка, дегазация, монтаж подвесных лесов до отметки 60 м",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2022, 9, 5), "planned_end_date": datetime(2022, 9, 12),
             "actual_end_date": datetime(2022, 9, 12), "progress_percentage": 100.0,
             "assigned_to": "Бригада подготовки"},
            {"project_id": projects[4].id, "name": "Демонтаж 4 циклонов (изнутри и снаружи)",
             "description": "Одновременный демонтаж 4 циклонов снаружи и изнутри аппарата на высоте до 60 м",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2022, 9, 13), "planned_end_date": datetime(2022, 9, 28),
             "actual_end_date": datetime(2022, 9, 27), "progress_percentage": 100.0,
             "assigned_to": "Монтажники высотники"},
            {"project_id": projects[4].id, "name": "Монтаж новых циклонов и испытания",
             "description": "Установка и приварка новых циклонов, контроль сварных швов, пуск регенератора",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2022, 9, 28), "planned_end_date": datetime(2022, 10, 14),
             "actual_end_date": datetime(2022, 10, 14), "progress_percentage": 100.0,
             "assigned_to": "Сварщики НАКС + монтажники"},
        ]

        tasks_p5 = [
            {"project_id": projects[5].id, "name": "Демонтаж клапана реактора R-104",
             "description": "Остановка реактора, демонтаж основного клапана и гидростанции",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2022, 9, 1), "planned_end_date": datetime(2022, 9, 15),
             "actual_end_date": datetime(2022, 9, 15), "progress_percentage": 100.0,
             "assigned_to": "Механики + слесари"},
            {"project_id": projects[5].id, "name": "Монтаж нового клапана со станцией гидравлики",
             "description": "Установка нового клапана DN=600, монтаж гидравлической станции управления",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2022, 9, 16), "planned_end_date": datetime(2022, 10, 25),
             "actual_end_date": datetime(2022, 10, 25), "progress_percentage": 100.0,
             "assigned_to": "Инженеры-механики"},
            {"project_id": projects[5].id, "name": "Предпусковая наладка и испытания",
             "description": "Наладка гидравлики, проверка хода клапана, функциональные испытания, пуск R-104",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2022, 10, 26), "planned_end_date": datetime(2022, 11, 10),
             "actual_end_date": datetime(2022, 11, 10), "progress_percentage": 100.0,
             "assigned_to": "КИПиА + технологи"},
        ]

        tasks_p6 = [
            {"project_id": projects[6].id, "name": "Демонтаж 4 теплообменников и трубопроводов обвязки",
             "description": "Отключение, демонтаж аппаратов Т-6, Т-23, Т-26, Т-28 и всей обвязки",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2023, 9, 5), "planned_end_date": datetime(2023, 9, 15),
             "actual_end_date": datetime(2023, 9, 14), "progress_percentage": 100.0,
             "assigned_to": "Монтажники + автокраны"},
            {"project_id": projects[6].id, "name": "Монтаж новых теплообменников и трубопроводов",
             "description": "Установка новых аппаратов, монтаж трубопроводов обвязки, сварка стыков",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2023, 9, 15), "planned_end_date": datetime(2023, 9, 28),
             "actual_end_date": datetime(2023, 9, 27), "progress_percentage": 100.0,
             "assigned_to": "Сварщики НАКС + монтажники"},
            {"project_id": projects[6].id, "name": "НК сварных швов, гидроиспытания, пуск АВТ-2",
             "description": "УЗК и РГК 100% стыков, гидроиспытания на 1.25Р, ввод установки в работу",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2023, 9, 28), "planned_end_date": datetime(2023, 10, 1),
             "actual_end_date": datetime(2023, 10, 1), "progress_percentage": 100.0,
             "assigned_to": "Лаборатория НК + технологи"},
        ]

        tasks_p7 = [
            {"project_id": projects[7].id, "name": "Остановка печи П-1 и подготовка к ремонту",
             "description": "Плановая остановка печи П-1 АВТ-2, охлаждение, продувка, монтаж лесов внутри камеры сгорания",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2023, 9, 1), "planned_end_date": datetime(2023, 9, 6),
             "actual_end_date": datetime(2023, 9, 6), "progress_percentage": 100.0,
             "assigned_to": "Бригада подготовки"},
            {"project_id": projects[7].id, "name": "Демонтаж старой конвекционной секции",
             "description": "Разборка обшивки, извлечение старых трубных змеевиков конвекции, демонтаж несущих конструкций",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2023, 9, 7), "planned_end_date": datetime(2023, 9, 16),
             "actual_end_date": datetime(2023, 9, 16), "progress_percentage": 100.0,
             "assigned_to": "Монтажники + автокран"},
            {"project_id": projects[7].id, "name": "Монтаж новой конвекционной секции и змеевиков",
             "description": "Установка новых несущих конструкций, монтаж трубных секций конвекции из стали 15Х5М, сварка стыков",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2023, 9, 17), "planned_end_date": datetime(2023, 9, 28),
             "actual_end_date": datetime(2023, 9, 27), "progress_percentage": 100.0,
             "assigned_to": "Сварщики НАКС 6 разряда + монтажники"},
            {"project_id": projects[7].id, "name": "НК сварных соединений и гидроиспытания",
             "description": "Радиографический контроль 100% сварных стыков (312 шт.), гидроиспытание на 1.25Р",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2023, 9, 28), "planned_end_date": datetime(2023, 9, 30),
             "actual_end_date": datetime(2023, 9, 30), "progress_percentage": 100.0,
             "assigned_to": "Лаборатория НК"},
            {"project_id": projects[7].id, "name": "Сушка футеровки по графику и пуск печи",
             "description": "Плавный разогрев конвекции по температурному графику, сушка огнеупорной футеровки, выход на рабочий режим",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2023, 10, 1), "planned_end_date": datetime(2023, 10, 2),
             "actual_end_date": datetime(2023, 10, 2), "progress_percentage": 100.0,
             "assigned_to": "Технологи АВТ-2"},
        ]

        tasks_p8 = [
            {"project_id": projects[8].id, "name": "Вывод реакторов R-101 и R-104 (CCR) из работы",
             "description": "Остановка CCR, дегазация реакторов, подготовка к вскрытию",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2023, 9, 5), "planned_end_date": datetime(2023, 9, 9),
             "actual_end_date": datetime(2023, 9, 9), "progress_percentage": 100.0,
             "assigned_to": "Эксплуатация CCR"},
            {"project_id": projects[8].id, "name": "Замена внутренних устройств R-101 и R-104",
             "description": "Демонтаж старых внутренних устройств, установка новых высокопроизводительных устройств",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2023, 9, 10), "planned_end_date": datetime(2023, 9, 25),
             "actual_end_date": datetime(2023, 9, 24), "progress_percentage": 100.0,
             "assigned_to": "Инженеры-механики"},
            {"project_id": projects[8].id, "name": "Сборка реакторов и пуск CCR",
             "description": "Сборка реакторов, загрузка катализатора, пуско-наладка установки CCR",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2023, 9, 25), "planned_end_date": datetime(2023, 9, 27),
             "actual_end_date": datetime(2023, 9, 27), "progress_percentage": 100.0,
             "assigned_to": "Технологи + механики"},
        ]

        tasks_p9 = [
            {"project_id": projects[9].id, "name": "Вывод УДГ из работы и вскрытие реакторов",
             "description": "Остановка установки УДГ, дегазация 4 реакторов, вскрытие люков",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2023, 9, 1), "planned_end_date": datetime(2023, 9, 6),
             "actual_end_date": datetime(2023, 9, 6), "progress_percentage": 100.0,
             "assigned_to": "Бригада подготовки"},
            {"project_id": projects[9].id, "name": "Замена конусных частей Р-1, Р-2, Р-3, Р-4",
             "description": "Демонтаж дефектных конусных частей, монтаж новых, сварка и НК швов",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2023, 9, 7), "planned_end_date": datetime(2023, 9, 28),
             "actual_end_date": datetime(2023, 9, 28), "progress_percentage": 100.0,
             "assigned_to": "Сварщики НАКС + механики"},
            {"project_id": projects[9].id, "name": "Испытания и ввод в работу",
             "description": "Гидроиспытания, загрузка катализатора, пуск установки УДГ",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2023, 9, 29), "planned_end_date": datetime(2023, 10, 2),
             "actual_end_date": datetime(2023, 10, 2), "progress_percentage": 100.0,
             "assigned_to": "Технологи"},
        ]

        tasks_p10 = [
            {"project_id": projects[10].id, "name": "Демонтаж старых компрессоров КТ-1",
             "description": "Остановка и демонтаж устаревшего компрессорного оборудования с 1981 г.",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2023, 6, 1), "planned_end_date": datetime(2023, 9, 30),
             "actual_end_date": datetime(2023, 9, 28), "progress_percentage": 100.0,
             "assigned_to": "Монтажники + механики"},
            {"project_id": projects[10].id, "name": "Монтаж и обвязка компрессоров Hitachi",
             "description": "Установка центробежных компрессоров жирного газа Hitachi, монтаж обвязки, трубопроводов",
             "status": TaskStatus.IN_PROGRESS, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2023, 10, 1), "planned_end_date": datetime(2025, 3, 31),
             "progress_percentage": 80.0, "assigned_to": "Инженеры-механики"},
            {"project_id": projects[10].id, "name": "Монтаж АСУ ТП и антипомпажной защиты",
             "description": "Монтаж и наладка систем автоматического управления, антипомпажная защита, диагностика",
             "status": TaskStatus.IN_PROGRESS, "priority": TaskPriority.HIGH,
             "start_date": datetime(2024, 6, 1), "planned_end_date": datetime(2025, 7, 31),
             "progress_percentage": 50.0, "assigned_to": "Инженеры КИПиА"},
        ]

        all_tasks = (tasks_p0 + tasks_p1 + tasks_p2 + tasks_p3 + tasks_p4 +
                     tasks_p5 + tasks_p6 + tasks_p7 + tasks_p8 + tasks_p9 +
                     tasks_p10)
        for task_data in all_tasks:
            db.add(Task(**task_data))
        db.commit()
        print(f"Created {len(all_tasks)} tasks")

        # ---- Resources ----

        resources_p0 = [
            {"project_id": projects[0].id, "name": "Слесарь-ремонтник 4-5 разряда",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 10.0, "unit": "чел/дн", "unit_cost": 12000.0},
            {"project_id": projects[0].id, "name": "Сварщик НАКС 5 разряда",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 5.0, "unit": "чел/дн", "unit_cost": 18000.0},
            {"project_id": projects[0].id, "name": "Трубные пучки теплообменников (замена)",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 30.0, "unit": "шт", "unit_cost": 5_500_000.0},
            {"project_id": projects[0].id, "name": "Прокладочный материал (паронит ПОН-Б)",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 3200.0, "unit": "шт", "unit_cost": 8500.0},
            {"project_id": projects[0].id, "name": "Автокран 25т",
             "resource_type": ResourceType.EQUIPMENT, "status": ResourceStatus.AVAILABLE,
             "quantity": 2.0, "unit": "маш/см", "unit_cost": 120000.0},
        ]

        resources_p1 = [
            {"project_id": projects[1].id, "name": "Монтажник 5 разряда",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 8.0, "unit": "чел/дн", "unit_cost": 14000.0},
            {"project_id": projects[1].id, "name": "Сварщик НАКС 5 разряда",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 4.0, "unit": "чел/дн", "unit_cost": 18000.0},
            {"project_id": projects[1].id, "name": "Контактные тарелки К-102 (11 шт.)",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 11.0, "unit": "шт", "unit_cost": 3_200_000.0},
            {"project_id": projects[1].id, "name": "Насосные агрегаты (замена, 6 ед.)",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 6.0, "unit": "шт", "unit_cost": 8_500_000.0},
            {"project_id": projects[1].id, "name": "Автокран 50т",
             "resource_type": ResourceType.EQUIPMENT, "status": ResourceStatus.AVAILABLE,
             "quantity": 1.0, "unit": "маш/см", "unit_cost": 200000.0},
        ]

        resources_p2 = [
            {"project_id": projects[2].id, "name": "Огнеупорщик 5 разряда",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 12.0, "unit": "чел/дн", "unit_cost": 16000.0},
            {"project_id": projects[2].id, "name": "Сварщик НАКС 5 разряда",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 6.0, "unit": "чел/дн", "unit_cost": 18000.0},
            {"project_id": projects[2].id, "name": "Слесарь КИПиА 4 разряда",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 8.0, "unit": "чел/дн", "unit_cost": 15000.0},
            {"project_id": projects[2].id, "name": "Форсунки горелок (замена)",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 60.0, "unit": "шт", "unit_cost": 350000.0},
            {"project_id": projects[2].id, "name": "Конвекционная секция трубчатой печи (в сборе)",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 2.0, "unit": "шт", "unit_cost": 85_000_000.0},
            {"project_id": projects[2].id, "name": "Леса строительные (комплект)",
             "resource_type": ResourceType.EQUIPMENT, "status": ResourceStatus.AVAILABLE,
             "quantity": 5.0, "unit": "комплект", "unit_cost": 350000.0},
        ]

        resources_p3 = [
            {"project_id": projects[3].id, "name": "Сварщик НАКС 5 разряда (нержавеющая сталь)",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 4.0, "unit": "чел/дн", "unit_cost": 22000.0},
            {"project_id": projects[3].id, "name": "Монтажник трубопроводов 5 разряда",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 3.0, "unit": "чел/дн", "unit_cost": 15000.0},
            {"project_id": projects[3].id, "name": "Труба нержавеющая Ду20-300 AISI 304",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 152.0, "unit": "м", "unit_cost": 185000.0},
            {"project_id": projects[3].id, "name": "Сварочная проволока ER308L",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 80.0, "unit": "кг", "unit_cost": 4500.0},
        ]

        resources_p4 = [
            {"project_id": projects[4].id, "name": "Монтажник-высотник 5 разряда",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 6.0, "unit": "чел/дн", "unit_cost": 20000.0},
            {"project_id": projects[4].id, "name": "Сварщик НАКС 5 разряда",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 4.0, "unit": "чел/дн", "unit_cost": 18000.0},
            {"project_id": projects[4].id, "name": "Циклоны регенератора (новые, 4 шт.)",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 4.0, "unit": "шт", "unit_cost": 12_000_000.0},
            {"project_id": projects[4].id, "name": "Подвесные леса (до 60м)",
             "resource_type": ResourceType.EQUIPMENT, "status": ResourceStatus.AVAILABLE,
             "quantity": 1.0, "unit": "комплект", "unit_cost": 850000.0},
        ]

        resources_p5 = [
            {"project_id": projects[5].id, "name": "Инженер-механик (клапанное оборудование)",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 3.0, "unit": "чел/дн", "unit_cost": 30000.0},
            {"project_id": projects[5].id, "name": "Клапан реактора DN=600 (новый)",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 1.0, "unit": "шт", "unit_cost": 95_000_000.0},
            {"project_id": projects[5].id, "name": "Гидравлическая станция управления",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 1.0, "unit": "шт", "unit_cost": 55_000_000.0},
            {"project_id": projects[5].id, "name": "Автокран 50т",
             "resource_type": ResourceType.EQUIPMENT, "status": ResourceStatus.AVAILABLE,
             "quantity": 1.0, "unit": "маш/см", "unit_cost": 200000.0},
        ]

        resources_p6 = [
            {"project_id": projects[6].id, "name": "Сварщик НАКС 6 разряда",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 6.0, "unit": "чел/дн", "unit_cost": 22000.0},
            {"project_id": projects[6].id, "name": "Монтажник трубопроводов 5 разряда",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 4.0, "unit": "чел/дн", "unit_cost": 15000.0},
            {"project_id": projects[6].id, "name": "Теплообменники Т-6, Т-23, Т-26, Т-28 (новые)",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 4.0, "unit": "шт", "unit_cost": 55_000_000.0},
            {"project_id": projects[6].id, "name": "Трубопроводы обвязки (в сборе)",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 1.0, "unit": "комплект", "unit_cost": 45_000_000.0},
            {"project_id": projects[6].id, "name": "Автокран 50т",
             "resource_type": ResourceType.EQUIPMENT, "status": ResourceStatus.AVAILABLE,
             "quantity": 2.0, "unit": "маш/см", "unit_cost": 200000.0},
        ]

        # KEY project resources (for PDF demo similarity)
        resources_p7 = [
            {"project_id": projects[7].id, "name": "Сварщик НАКС 6 разряда (жаропрочные стали)",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 8.0, "unit": "чел/дн", "unit_cost": 24000.0},
            {"project_id": projects[7].id, "name": "Монтажник трубопроводов 5 разряда",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 6.0, "unit": "чел/дн", "unit_cost": 15000.0},
            {"project_id": projects[7].id, "name": "Огнеупорщик 5 разряда",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 4.0, "unit": "чел/дн", "unit_cost": 16000.0},
            {"project_id": projects[7].id, "name": "Конвекционная секция печи П-1 (новая, в сборе)",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 1.0, "unit": "шт", "unit_cost": 280_000_000.0},
            {"project_id": projects[7].id, "name": "Трубы жаропрочные 15Х5М (змеевик)",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 48.0, "unit": "шт", "unit_cost": 1_800_000.0},
            {"project_id": projects[7].id, "name": "Огнеупорный цемент и кирпич",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 8000.0, "unit": "шт", "unit_cost": 900.0},
            {"project_id": projects[7].id, "name": "Автокран 50т",
             "resource_type": ResourceType.EQUIPMENT, "status": ResourceStatus.IN_USE,
             "quantity": 1.0, "unit": "маш/см", "unit_cost": 200000.0},
            {"project_id": projects[7].id, "name": "Леса строительные (комплект)",
             "resource_type": ResourceType.EQUIPMENT, "status": ResourceStatus.IN_USE,
             "quantity": 2.0, "unit": "комплект", "unit_cost": 350000.0},
        ]

        resources_p8 = [
            {"project_id": projects[8].id, "name": "Инженер-механик (реакторное оборудование CCR)",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 4.0, "unit": "чел/дн", "unit_cost": 30000.0},
            {"project_id": projects[8].id, "name": "Внутренние устройства реакторов R-101 и R-104",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 2.0, "unit": "комплект", "unit_cost": 55_000_000.0},
            {"project_id": projects[8].id, "name": "Автокран 25т",
             "resource_type": ResourceType.EQUIPMENT, "status": ResourceStatus.AVAILABLE,
             "quantity": 1.0, "unit": "маш/см", "unit_cost": 120000.0},
        ]

        resources_p9 = [
            {"project_id": projects[9].id, "name": "Сварщик НАКС 5 разряда",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 4.0, "unit": "чел/дн", "unit_cost": 18000.0},
            {"project_id": projects[9].id, "name": "Конусные части реакторов Р-1—Р-4 (комплект)",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 4.0, "unit": "шт", "unit_cost": 18_000_000.0},
            {"project_id": projects[9].id, "name": "Сварочные электроды УОНИ 13/55",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 150.0, "unit": "кг", "unit_cost": 1500.0},
        ]

        resources_p10 = [
            {"project_id": projects[10].id, "name": "Инженер-механик и КИПиА",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.IN_USE,
             "quantity": 25.0, "unit": "чел/дн", "unit_cost": 35000.0},
            {"project_id": projects[10].id, "name": "Слесари-монтажники 5-6 разряда",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.IN_USE,
             "quantity": 40.0, "unit": "чел/дн", "unit_cost": 18000.0},
            {"project_id": projects[10].id, "name": "Компрессоры жирного газа Hitachi (новые)",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 2.0, "unit": "шт", "unit_cost": 280_000_000.0},
            {"project_id": projects[10].id, "name": "Автокран 100т",
             "resource_type": ResourceType.EQUIPMENT, "status": ResourceStatus.IN_USE,
             "quantity": 2.0, "unit": "маш/см", "unit_cost": 350000.0},
        ]

        all_resources = (resources_p0 + resources_p1 + resources_p2 + resources_p3 +
                         resources_p4 + resources_p5 + resources_p6 + resources_p7 +
                         resources_p8 + resources_p9 + resources_p10)
        for res_data in all_resources:
            resource = Resource(**res_data)
            resource.calculate_total_cost()
            db.add(resource)
        db.commit()
        print(f"Created {len(all_resources)} resources")

        # ---- Budgets ----

        budgets = [
            # p0 — теплообменники ПНХЗ
            {"project_id": projects[0].id, "category": "Материалы",
             "description": "Трубные пучки, прокладки, метизы, сварочные материалы",
             "planned_amount": 200_000_000.0, "actual_amount": 195_000_000.0},
            {"project_id": projects[0].id, "category": "Работа",
             "description": "Слесари, сварщики НАКС, дефектоскописты",
             "planned_amount": 120_000_000.0, "actual_amount": 117_000_000.0},
            {"project_id": projects[0].id, "category": "Техника",
             "description": "Автокраны, установки гидрочистки",
             "planned_amount": 30_000_000.0, "actual_amount": 30_000_000.0},
            # p1 — колонны ПНХЗ
            {"project_id": projects[1].id, "category": "Оборудование",
             "description": "Насосные агрегаты, тарелки, ёмкости, ПКУ",
             "planned_amount": 180_000_000.0, "actual_amount": 175_000_000.0},
            {"project_id": projects[1].id, "category": "Работа",
             "description": "Монтажники, сварщики, слесари",
             "planned_amount": 80_000_000.0, "actual_amount": 77_000_000.0},
            {"project_id": projects[1].id, "category": "Техника",
             "description": "Краны, строительные леса",
             "planned_amount": 20_000_000.0, "actual_amount": 20_000_000.0},
            # p2 — печи ПНХЗ
            {"project_id": projects[2].id, "category": "Материалы",
             "description": "Конвекционные секции, форсунки, огнеупорный материал",
             "planned_amount": 250_000_000.0, "actual_amount": 245_000_000.0},
            {"project_id": projects[2].id, "category": "Работа",
             "description": "Огнеупорщики, сварщики, слесари КИПиА",
             "planned_amount": 130_000_000.0, "actual_amount": 127_000_000.0},
            {"project_id": projects[2].id, "category": "Техника",
             "description": "Краны, леса, гидроструйные установки",
             "planned_amount": 40_000_000.0, "actual_amount": 40_000_000.0},
            # p3 — трубопровод DR-201
            {"project_id": projects[3].id, "category": "Материалы",
             "description": "Трубы нержавеющие, фитинги, электроды ER308L",
             "planned_amount": 40_000_000.0, "actual_amount": 38_500_000.0},
            {"project_id": projects[3].id, "category": "Работа",
             "description": "Сварщики, монтажники, НК-лаборатория",
             "planned_amount": 20_000_000.0, "actual_amount": 20_000_000.0},
            {"project_id": projects[3].id, "category": "НК и испытания",
             "description": "Радиографический контроль, гидроиспытания",
             "planned_amount": 5_000_000.0, "actual_amount": 5_000_000.0},
            # p4 — циклоны R-105
            {"project_id": projects[4].id, "category": "Оборудование",
             "description": "Циклоны регенератора (4 шт.)",
             "planned_amount": 60_000_000.0, "actual_amount": 58_000_000.0},
            {"project_id": projects[4].id, "category": "Работа",
             "description": "Монтажники-высотники, сварщики НАКС",
             "planned_amount": 25_000_000.0, "actual_amount": 24_000_000.0},
            {"project_id": projects[4].id, "category": "Техника и леса",
             "description": "Подвесные леса до 60м, такелаж",
             "planned_amount": 10_000_000.0, "actual_amount": 10_000_000.0},
            # p5 — клапан R-104
            {"project_id": projects[5].id, "category": "Оборудование",
             "description": "Клапан реактора DN=600, гидростанция управления",
             "planned_amount": 160_000_000.0, "actual_amount": 158_000_000.0},
            {"project_id": projects[5].id, "category": "Работа и наладка",
             "description": "Инженеры-механики, слесари, пуско-наладка",
             "planned_amount": 35_000_000.0, "actual_amount": 35_000_000.0},
            {"project_id": projects[5].id, "category": "Логистика",
             "description": "Доставка оборудования, такелаж, автокран",
             "planned_amount": 15_000_000.0, "actual_amount": 15_000_000.0},
            # p6 — теплообменники АВТ-2
            {"project_id": projects[6].id, "category": "Оборудование",
             "description": "Теплообменники Т-6,23,26,28 и трубопроводы обвязки",
             "planned_amount": 280_000_000.0, "actual_amount": 274_000_000.0},
            {"project_id": projects[6].id, "category": "Работа",
             "description": "Сварщики НАКС, монтажники, НК-лаборатория",
             "planned_amount": 80_000_000.0, "actual_amount": 80_000_000.0},
            {"project_id": projects[6].id, "category": "Техника",
             "description": "Автокраны 50т, инструмент",
             "planned_amount": 20_000_000.0, "actual_amount": 20_000_000.0},
            # p7 — конвекция П-1 АВТ-2 (KEY project)
            {"project_id": projects[7].id, "category": "Оборудование и материалы",
             "description": "Конвекционная секция П-1 (в сборе), трубы 15Х5М, огнеупорный кирпич",
             "planned_amount": 400_000_000.0, "actual_amount": 395_000_000.0},
            {"project_id": projects[7].id, "category": "Работа",
             "description": "Сварщики НАКС 6р, монтажники, огнеупорщики",
             "planned_amount": 90_000_000.0, "actual_amount": 88_000_000.0},
            {"project_id": projects[7].id, "category": "НК и испытания",
             "description": "Радиографический контроль 312 стыков, гидроиспытания",
             "planned_amount": 20_000_000.0, "actual_amount": 19_500_000.0},
            {"project_id": projects[7].id, "category": "Техника",
             "description": "Автокран 50т, строительные леса",
             "planned_amount": 10_000_000.0, "actual_amount": 11_500_000.0},
            # p8 — реакторы CCR
            {"project_id": projects[8].id, "category": "Внутренние устройства",
             "description": "Внутренние устройства реакторов R-101, R-104 (в сборе)",
             "planned_amount": 130_000_000.0, "actual_amount": 127_000_000.0},
            {"project_id": projects[8].id, "category": "Работа",
             "description": "Инженеры-механики, монтажники, пуско-наладка",
             "planned_amount": 40_000_000.0, "actual_amount": 39_000_000.0},
            {"project_id": projects[8].id, "category": "Техника",
             "description": "Кран, инструмент",
             "planned_amount": 10_000_000.0, "actual_amount": 10_000_000.0},
            # p9 — реакторы УДГ
            {"project_id": projects[9].id, "category": "Материалы",
             "description": "Конусные части реакторов (4 шт.), электроды",
             "planned_amount": 90_000_000.0, "actual_amount": 88_000_000.0},
            {"project_id": projects[9].id, "category": "Работа",
             "description": "Сварщики НАКС, механики, НК-лаборатория",
             "planned_amount": 30_000_000.0, "actual_amount": 29_000_000.0},
            {"project_id": projects[9].id, "category": "НК и испытания",
             "description": "УЗК, РГК, гидроиспытания",
             "planned_amount": 10_000_000.0, "actual_amount": 10_000_000.0},
            # p10 — КТ-1
            {"project_id": projects[10].id, "category": "Оборудование Hitachi",
             "description": "Центробежные компрессоры жирного газа, АСУ ТП, антипомпажная защита",
             "planned_amount": 700_000_000.0, "actual_amount": 530_000_000.0},
            {"project_id": projects[10].id, "category": "СМР и пуско-наладка",
             "description": "Монтаж, обвязка, пуско-наладочные работы, интеграция пожаротушения",
             "planned_amount": 150_000_000.0, "actual_amount": 90_000_000.0},
        ]

        for budget_data in budgets:
            db.add(Budget(**budget_data))
        db.commit()
        print(f"Created {len(budgets)} budget entries")

        # ---- Precompute embeddings ----
        print("Computing embeddings for projects (this may take a moment)...")
        similarity = SimilarityService(db)
        for proj in projects:
            db.refresh(proj)
        for proj in projects:
            try:
                similarity.index_project(proj)
                print(f"  Indexed: {proj.name[:60]}")
            except Exception as e:
                print(f"  Failed to index {proj.name[:60]}: {e}")

        print("\nDatabase seeding completed successfully!")
        print(f"Summary:")
        print(f"   - Projects: {len(projects)}")
        print(f"   - Tasks: {len(all_tasks)}")
        print(f"   - Resources: {len(all_resources)}")
        print(f"   - Budget Entries: {len(budgets)}")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
