#Run with: docker-compose exec backend python -m app.utils.seed_data

from datetime import datetime, timedelta
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
        print("Starting database seeding...")

        projects_data = [
            {
                "name": "Residential Complex Alpha",
                "description": "Modern 10-story residential building with 120 apartments",
                "status": ProjectStatus.IN_PROGRESS,
                "start_date": datetime(2025, 9, 1),
                "planned_end_date": datetime(2026, 12, 31),
                "total_budget": 8500000.0,
                "spent_amount": 3200000.0,
                "location": "Astana, Esil District"
            },
            {
                "name": "Business Center Omega",
                "description": "15-story office building with retail on ground floor",
                "status": ProjectStatus.IN_PROGRESS,
                "start_date": datetime(2025, 7, 15),
                "planned_end_date": datetime(2027, 6, 30),
                "total_budget": 15000000.0,
                "spent_amount": 4500000.0,
                "location": "Almaty, Bostandyk District"
            },
            {
                "name": "Shopping Mall Gamma",
                "description": "3-story shopping center with parking",
                "status": ProjectStatus.PLANNING,
                "start_date": datetime(2025, 12, 1),
                "planned_end_date": datetime(2027, 3, 31),
                "total_budget": 12000000.0,
                "spent_amount": 0.0,
                "location": "Shymkent, City Center"
            },
            # --- AVC-specific oil refinery projects ---
            {
                "name": "Капитальный ремонт теплообменника Е-101А АНПЗ",
                "description": "Замена трубного пучка, чистка межтрубного пространства, ревизия арматуры. Теплообменник кожухотрубный, давление 25 атм.",
                "status": ProjectStatus.COMPLETED,
                "start_date": datetime(2023, 4, 1),
                "planned_end_date": datetime(2023, 5, 20),
                "actual_end_date": datetime(2023, 5, 18),
                "total_budget": 45_000_000.0,
                "spent_amount": 43_200_000.0,
                "location": "АНПЗ, Атырау"
            },
            {
                "name": "Ремонт насосного агрегата ЦН-201 ПНХЗ",
                "description": "Замена рабочего колеса, торцевых уплотнений, подшипников. Балансировка ротора. Насос центробежный ЦН-201.",
                "status": ProjectStatus.COMPLETED,
                "start_date": datetime(2023, 8, 10),
                "planned_end_date": datetime(2023, 9, 10),
                "actual_end_date": datetime(2023, 9, 12),
                "total_budget": 12_500_000.0,
                "spent_amount": 13_100_000.0,
                "location": "ПНХЗ, Павлодар"
            },
            {
                "name": "Замена трубопровода нефтепродуктов Ду300 АНПЗ",
                "description": "Демонтаж старого трубопровода 120м, монтаж нового из стали 09Г2С, гидроиспытания, изоляция минватой 80мм",
                "status": ProjectStatus.COMPLETED,
                "start_date": datetime(2023, 10, 1),
                "planned_end_date": datetime(2023, 11, 30),
                "actual_end_date": datetime(2023, 12, 3),
                "total_budget": 28_000_000.0,
                "spent_amount": 29_500_000.0,
                "location": "АНПЗ, Атырау"
            },
            {
                "name": "Текущий ремонт печи П-101 установки АВТ",
                "description": "Замена огнеупорной футеровки, ревизия горелок, ремонт змеевика. Печь трубчатая вертикальная.",
                "status": ProjectStatus.COMPLETED,
                "start_date": datetime(2024, 2, 5),
                "planned_end_date": datetime(2024, 3, 25),
                "actual_end_date": datetime(2024, 3, 22),
                "total_budget": 85_000_000.0,
                "spent_amount": 82_000_000.0,
                "location": "ПНХЗ, Павлодар"
            },
            {
                "name": "Ремонт компрессора К-301 КЦ-2",
                "description": "Капитальный ремонт центробежного компрессора: замена лабиринтных уплотнений, ревизия ротора, замена подшипников скольжения",
                "status": ProjectStatus.IN_PROGRESS,
                "start_date": datetime(2024, 11, 1),
                "planned_end_date": datetime(2025, 2, 28),
                "total_budget": 120_000_000.0,
                "spent_amount": 65_000_000.0,
                "location": "АНПЗ, Атырау"
            },
            {
                "name": "Капитальный ремонт резервуара РВС-10000 №3 АНПЗ",
                "description": "Капитальный ремонт резервуара вертикального стального объёмом 10 000 м3 резервуарного парка №1А: замена днища, ремонт стенки, замена кровли, антикоррозионная защита, монтаж плавающего понтона",
                "status": ProjectStatus.COMPLETED,
                "start_date": datetime(2024, 3, 1),
                "planned_end_date": datetime(2024, 5, 30),
                "actual_end_date": datetime(2024, 5, 28),
                "total_budget": 118_000_000.0,
                "spent_amount": 115_700_000.0,
                "location": "КАЗАХСТАН, Атырауская область, г. Атырау, АНПЗ"
            },
            # --- AVC large-scale turnaround projects (from company portfolio) ---
            {
                "name": "Капитальный ремонт МНПЗ — 23 установки, 8 производств",
                "description": (
                    "Капитальный ремонт 23 технологических установок на 8 производствах МНПЗ. "
                    "Замена пароперегревателя Е-402, ёмкости Е-102, сепаратора С-302, "
                    "11 тарелок колонны К-102; замена 6 ед. насосного оборудования; "
                    "ревизия и ремонт теплообменного оборудования — 95 ед.; "
                    "ревизия ёмкостного и колонного оборудования — 166 ед.; "
                    "ревизия технологических печей — 30 ед.; "
                    "замена конвекций технологических печей — 2 ед.; "
                    "демонтаж-монтаж ТРО — более 1400 шт; монтаж ПКУ — 46 ед.; "
                    "чистка технологического оборудования — 145 ед. "
                    "Сварных стыков/швов: 2717. Прокладок/фланцев: 20 286 шт. КИП и ЗРА: 3 070 комплектов. "
                    "Задействовано: инженеры ИТР — 83 чел., рабочие — 1292 чел."
                ),
                "status": ProjectStatus.COMPLETED,
                "start_date": datetime(2022, 4, 1),
                "planned_end_date": datetime(2022, 6, 30),
                "actual_end_date": datetime(2022, 6, 28),
                "total_budget": 2_500_000_000.0,
                "spent_amount": 2_480_000_000.0,
                "location": "МНПЗ"
            },
            {
                "name": "ППР АНПЗ — 24 технологических установки (1-й цикл)",
                "description": (
                    "Планово-предупредительный ремонт 24 технологических установок АНПЗ. "
                    "Установка CCR: замена трубопровода-осушителя DR-201 из нержавеющей стали Ду20–300 мм, 152 м. "
                    "Регенератор R-105 (ФКК): замена 4 циклонов на отметке до 60 м (работа одновременно снаружи и внутри). "
                    "Компрессоры K-0251 (КЦ), K-1302 (КЦ), K-0101 (КЦ), 20-C-001 (ТЦ): "
                    "плановые ремонты четырёх критически важных компрессоров одновременно. "
                    "Реактор R-104 (ФКК): полная замена основного клапана реактора со станцией гидравлики. "
                    "Теплообменники Т-6, Т-23, Т-26, Т-28 (АВТ-2): полная замена аппаратов и трубопроводов обвязки."
                ),
                "status": ProjectStatus.COMPLETED,
                "start_date": datetime(2022, 9, 1),
                "planned_end_date": datetime(2022, 11, 15),
                "actual_end_date": datetime(2022, 11, 10),
                "total_budget": 4_200_000_000.0,
                "spent_amount": 4_150_000_000.0,
                "location": "АНПЗ, Атырау"
            },
            {
                "name": "ППР АНПЗ — 24 технологических установки (2-й цикл)",
                "description": (
                    "Планово-предупредительный ремонт 24 установок АНПЗ за 31 рабочий день. "
                    "Реакторы CCR R-101 и R-104: модернизация с заменой внутренних устройств. "
                    "Реакторы УДГ Р-1, Р-2, Р-3, Р-4: замена конусных частей, устранение дефектов. "
                    "АВТ-2 Газоотбойник 13-А1-5: комплексная замена аппарата. "
                    "АВТ-2 Печь П-1: замена конвекционной части. "
                    "АВТ-2, АВТ-3 Колонны К-1, К-1 и К-2: замена контактных внутренних устройств. "
                    "Мобилизация персонала: 2220 чел. Рабочих дней: 31. "
                    "Краны: 26 ед.; ДВС, длинномеры: 12 ед.; экскаваторы: 8 ед."
                ),
                "status": ProjectStatus.COMPLETED,
                "start_date": datetime(2023, 9, 1),
                "planned_end_date": datetime(2023, 10, 5),
                "actual_end_date": datetime(2023, 10, 2),
                "total_budget": 3_100_000_000.0,
                "spent_amount": 3_050_000_000.0,
                "location": "АНПЗ, Атырау"
            },
            {
                "name": "Модернизация компрессорной станции КТ-1 АНПЗ",
                "description": (
                    "Модернизация компрессорной станции КТ-1 на АНПЗ: замена морально и физически "
                    "устаревшего оборудования (эксплуатировалось с 1981 г.) на современные "
                    "центробежные компрессоры жирного газа производства Hitachi. "
                    "Оснащение систем АСУ ТП, антипомпажной защитой, диагностикой. "
                    "Интеграция автоматических установок порошкового пожаротушения "
                    "и систем сухого газового уплотнения. "
                    "Прогнозируемая экономия > 120 млн тенге в год. "
                    "Срок: июнь 2023 — июль 2025. "
                    "Повышение надёжности и энергоэффективности производства."
                ),
                "status": ProjectStatus.IN_PROGRESS,
                "start_date": datetime(2023, 6, 1),
                "planned_end_date": datetime(2025, 7, 31),
                "total_budget": 850_000_000.0,
                "spent_amount": 620_000_000.0,
                "location": "АНПЗ, Атырау"
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

        # ---- Tasks for construction projects (indices 0-2) ----
        tasks_project1 = [
            {
                "project_id": projects[0].id,
                "name": "Site Preparation and Excavation",
                "description": "Clear site and excavate foundation",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2025, 9, 1),
                "planned_end_date": datetime(2025, 10, 15),
                "actual_end_date": datetime(2025, 10, 12),
                "progress_percentage": 100.0,
                "assigned_to": "Construction Team A"
            },
            {
                "project_id": projects[0].id,
                "name": "Foundation Construction",
                "description": "Pour concrete foundation",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.CRITICAL,
                "start_date": datetime(2025, 10, 16),
                "planned_end_date": datetime(2025, 11, 30),
                "actual_end_date": datetime(2025, 11, 28),
                "progress_percentage": 100.0,
                "assigned_to": "Foundation Specialists"
            },
            {
                "project_id": projects[0].id,
                "name": "Structural Framework (Floors 1-5)",
                "description": "Build structural columns and beams",
                "status": TaskStatus.IN_PROGRESS,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2025, 12, 1),
                "planned_end_date": datetime(2026, 3, 31),
                "progress_percentage": 65.0,
                "assigned_to": "Structural Team"
            },
            {
                "project_id": projects[0].id,
                "name": "Structural Framework (Floors 6-10)",
                "description": "Build upper floors structure",
                "status": TaskStatus.NOT_STARTED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2026, 4, 1),
                "planned_end_date": datetime(2026, 7, 31),
                "progress_percentage": 0.0,
                "assigned_to": "Structural Team"
            },
            {
                "project_id": projects[0].id,
                "name": "Electrical Systems Installation",
                "description": "Install wiring and electrical panels",
                "status": TaskStatus.NOT_STARTED,
                "priority": TaskPriority.MEDIUM,
                "start_date": datetime(2026, 6, 1),
                "planned_end_date": datetime(2026, 9, 30),
                "progress_percentage": 0.0,
                "assigned_to": "Electrical Team"
            }
        ]

        tasks_project2 = [
            {
                "project_id": projects[1].id,
                "name": "Demolition of Old Structure",
                "description": "Safe demolition and debris removal",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2025, 7, 15),
                "planned_end_date": datetime(2025, 8, 31),
                "actual_end_date": datetime(2025, 8, 28),
                "progress_percentage": 100.0,
                "assigned_to": "Demolition Crew"
            },
            {
                "project_id": projects[1].id,
                "name": "Deep Foundation Work",
                "description": "Pile driving and foundation reinforcement",
                "status": TaskStatus.IN_PROGRESS,
                "priority": TaskPriority.CRITICAL,
                "start_date": datetime(2025, 9, 1),
                "planned_end_date": datetime(2026, 1, 15),
                "progress_percentage": 45.0,
                "assigned_to": "Foundation Specialists"
            }
        ]

        # ---- Tasks for AVC project 3: Теплообменник Е-101А ----
        tasks_project3 = [
            {
                "project_id": projects[3].id,
                "name": "Подготовительные работы и вывод из эксплуатации",
                "description": "Отключение теплообменника, дренаж, продувка, установка заглушек, оформление наряд-допуска",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.CRITICAL,
                "start_date": datetime(2023, 4, 1),
                "planned_end_date": datetime(2023, 4, 5),
                "actual_end_date": datetime(2023, 4, 5),
                "progress_percentage": 100.0,
                "assigned_to": "Бригада подготовки"
            },
            {
                "project_id": projects[3].id,
                "name": "Демонтаж трубного пучка",
                "description": "Извлечение старого трубного пучка краном, транспортировка на площадку",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2023, 4, 6),
                "planned_end_date": datetime(2023, 4, 12),
                "actual_end_date": datetime(2023, 4, 11),
                "progress_percentage": 100.0,
                "assigned_to": "Монтажная бригада"
            },
            {
                "project_id": projects[3].id,
                "name": "Чистка корпуса и межтрубного пространства",
                "description": "Гидроструйная чистка корпуса, удаление отложений, дефектоскопия",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2023, 4, 13),
                "planned_end_date": datetime(2023, 4, 20),
                "actual_end_date": datetime(2023, 4, 19),
                "progress_percentage": 100.0,
                "assigned_to": "Бригада чистки"
            },
            {
                "project_id": projects[3].id,
                "name": "Монтаж нового трубного пучка",
                "description": "Установка нового пучка, развальцовка труб, проверка плотности",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.CRITICAL,
                "start_date": datetime(2023, 4, 21),
                "planned_end_date": datetime(2023, 5, 5),
                "actual_end_date": datetime(2023, 5, 4),
                "progress_percentage": 100.0,
                "assigned_to": "Монтажная бригада"
            },
            {
                "project_id": projects[3].id,
                "name": "Гидроиспытания и ввод в эксплуатацию",
                "description": "Гидроиспытания на 1.25Р, устранение течей, снятие заглушек, пуск",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.CRITICAL,
                "start_date": datetime(2023, 5, 6),
                "planned_end_date": datetime(2023, 5, 18),
                "actual_end_date": datetime(2023, 5, 18),
                "progress_percentage": 100.0,
                "assigned_to": "Бригада испытаний"
            }
        ]

        # ---- Tasks for AVC project 4: Насосный агрегат ЦН-201 ----
        tasks_project4 = [
            {
                "project_id": projects[4].id,
                "name": "Демонтаж насоса и электродвигателя",
                "description": "Отключение от трубопроводов, демонтаж муфты, снятие насоса с фундамента",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2023, 8, 10),
                "planned_end_date": datetime(2023, 8, 15),
                "actual_end_date": datetime(2023, 8, 15),
                "progress_percentage": 100.0,
                "assigned_to": "Слесари-ремонтники"
            },
            {
                "project_id": projects[4].id,
                "name": "Разборка и дефектовка насоса",
                "description": "Полная разборка, замер износа деталей, составление дефектной ведомости",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2023, 8, 16),
                "planned_end_date": datetime(2023, 8, 22),
                "actual_end_date": datetime(2023, 8, 21),
                "progress_percentage": 100.0,
                "assigned_to": "Слесари-ремонтники"
            },
            {
                "project_id": projects[4].id,
                "name": "Замена рабочего колеса и уплотнений",
                "description": "Установка нового рабочего колеса, торцевых уплотнений John Crane, подшипников SKF",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.CRITICAL,
                "start_date": datetime(2023, 8, 23),
                "planned_end_date": datetime(2023, 9, 2),
                "actual_end_date": datetime(2023, 9, 3),
                "progress_percentage": 100.0,
                "assigned_to": "Слесари-ремонтники"
            },
            {
                "project_id": projects[4].id,
                "name": "Балансировка ротора и сборка",
                "description": "Динамическая балансировка на стенде, сборка насоса, центровка с двигателем",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2023, 9, 3),
                "planned_end_date": datetime(2023, 9, 10),
                "actual_end_date": datetime(2023, 9, 12),
                "progress_percentage": 100.0,
                "assigned_to": "Механики"
            }
        ]

        # ---- Tasks for AVC project 5: Трубопровод Ду300 ----
        tasks_project5 = [
            {
                "project_id": projects[5].id,
                "name": "Подготовка трассы и демонтаж старого трубопровода",
                "description": "Снятие изоляции, резка и демонтаж 120м трубопровода Ду300",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2023, 10, 1),
                "planned_end_date": datetime(2023, 10, 15),
                "actual_end_date": datetime(2023, 10, 14),
                "progress_percentage": 100.0,
                "assigned_to": "Монтажники"
            },
            {
                "project_id": projects[5].id,
                "name": "Сварка и монтаж нового трубопровода",
                "description": "Сварка труб 09Г2С, монтаж опор, установка арматуры",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.CRITICAL,
                "start_date": datetime(2023, 10, 16),
                "planned_end_date": datetime(2023, 11, 10),
                "actual_end_date": datetime(2023, 11, 12),
                "progress_percentage": 100.0,
                "assigned_to": "Сварщики + монтажники"
            },
            {
                "project_id": projects[5].id,
                "name": "Контроль сварных соединений (РГК, УЗК)",
                "description": "Радиографический и ультразвуковой контроль 100% стыков",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.CRITICAL,
                "start_date": datetime(2023, 11, 11),
                "planned_end_date": datetime(2023, 11, 18),
                "actual_end_date": datetime(2023, 11, 17),
                "progress_percentage": 100.0,
                "assigned_to": "Лаборатория НК"
            },
            {
                "project_id": projects[5].id,
                "name": "Гидроиспытания и изоляция",
                "description": "Гидроиспытания на 1.25Р, нанесение антикоррозионного покрытия, изоляция минватой 80мм",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2023, 11, 19),
                "planned_end_date": datetime(2023, 12, 1),
                "actual_end_date": datetime(2023, 12, 3),
                "progress_percentage": 100.0,
                "assigned_to": "Изолировщики + испытатели"
            }
        ]

        # ---- Tasks for AVC project 6: Печь П-101 ----
        tasks_project6 = [
            {
                "project_id": projects[6].id,
                "name": "Остановка печи и подготовка к ремонту",
                "description": "Охлаждение печи, пропарка, установка лесов внутри камеры сгорания",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.CRITICAL,
                "start_date": datetime(2024, 2, 5),
                "planned_end_date": datetime(2024, 2, 10),
                "actual_end_date": datetime(2024, 2, 10),
                "progress_percentage": 100.0,
                "assigned_to": "Бригада подготовки"
            },
            {
                "project_id": projects[6].id,
                "name": "Демонтаж старой футеровки",
                "description": "Разборка огнеупорной кладки, вывоз строительного мусора",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2024, 2, 11),
                "planned_end_date": datetime(2024, 2, 20),
                "actual_end_date": datetime(2024, 2, 19),
                "progress_percentage": 100.0,
                "assigned_to": "Огнеупорщики"
            },
            {
                "project_id": projects[6].id,
                "name": "Ревизия и ремонт горелок",
                "description": "Разборка 6 горелок, замена форсунок, чистка газовых каналов",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2024, 2, 15),
                "planned_end_date": datetime(2024, 2, 28),
                "actual_end_date": datetime(2024, 2, 27),
                "progress_percentage": 100.0,
                "assigned_to": "Слесари КИПиА"
            },
            {
                "project_id": projects[6].id,
                "name": "Ремонт змеевика и монтаж новой футеровки",
                "description": "Замена 12 труб змеевика, укладка новой огнеупорной футеровки ШБ-5",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.CRITICAL,
                "start_date": datetime(2024, 2, 21),
                "planned_end_date": datetime(2024, 3, 15),
                "actual_end_date": datetime(2024, 3, 14),
                "progress_percentage": 100.0,
                "assigned_to": "Огнеупорщики + сварщики"
            },
            {
                "project_id": projects[6].id,
                "name": "Сушка футеровки и пуск печи",
                "description": "Плавный разогрев по графику, выход на рабочий режим",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2024, 3, 16),
                "planned_end_date": datetime(2024, 3, 25),
                "actual_end_date": datetime(2024, 3, 22),
                "progress_percentage": 100.0,
                "assigned_to": "Технологи"
            }
        ]

        # ---- Tasks for AVC project 7: Компрессор К-301 ----
        tasks_project7 = [
            {
                "project_id": projects[7].id,
                "name": "Вывод компрессора из работы",
                "description": "Остановка, продувка азотом, отключение от трубопроводов",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.CRITICAL,
                "start_date": datetime(2024, 11, 1),
                "planned_end_date": datetime(2024, 11, 5),
                "actual_end_date": datetime(2024, 11, 5),
                "progress_percentage": 100.0,
                "assigned_to": "Эксплуатация"
            },
            {
                "project_id": projects[7].id,
                "name": "Разборка и дефектовка компрессора",
                "description": "Демонтаж крышки, извлечение ротора, замеры зазоров",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2024, 11, 6),
                "planned_end_date": datetime(2024, 11, 20),
                "actual_end_date": datetime(2024, 11, 22),
                "progress_percentage": 100.0,
                "assigned_to": "Механики"
            },
            {
                "project_id": projects[7].id,
                "name": "Замена уплотнений и подшипников",
                "description": "Замена лабиринтных уплотнений, подшипников скольжения, упорного подшипника",
                "status": TaskStatus.IN_PROGRESS,
                "priority": TaskPriority.CRITICAL,
                "start_date": datetime(2024, 11, 23),
                "planned_end_date": datetime(2025, 1, 15),
                "progress_percentage": 70.0,
                "assigned_to": "Механики"
            },
            {
                "project_id": projects[7].id,
                "name": "Сборка, центровка и обкатка",
                "description": "Сборка компрессора, лазерная центровка с приводом, обкатка на холостом ходу",
                "status": TaskStatus.NOT_STARTED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2025, 1, 16),
                "planned_end_date": datetime(2025, 2, 28),
                "progress_percentage": 0.0,
                "assigned_to": "Механики + КИПиА"
            }
        ]

        # ---- Tasks for AVC project 8: Резервуар РВС-10000 №3 ----
        tasks_project8 = [
            {
                "project_id": projects[8].id,
                "name": "Подготовительные работы. Зачистка и дегазация резервуара",
                "description": "Откачка остатков нефти, промывка, дегазация, оформление нарядов-допусков, установка инвентарных лесов",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.CRITICAL,
                "start_date": datetime(2024, 3, 1),
                "planned_end_date": datetime(2024, 3, 15),
                "actual_end_date": datetime(2024, 3, 14),
                "progress_percentage": 100.0,
                "assigned_to": "Бригада подготовки"
            },
            {
                "project_id": projects[8].id,
                "name": "Демонтаж кровли и понтона",
                "description": "Вырезка и демонтаж кровли резервуара, извлечение понтона, разборка вспомогательных конструкций",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2024, 3, 15),
                "planned_end_date": datetime(2024, 3, 28),
                "actual_end_date": datetime(2024, 3, 27),
                "progress_percentage": 100.0,
                "assigned_to": "Бригада монтажников"
            },
            {
                "project_id": projects[8].id,
                "name": "Замена днища резервуара",
                "description": "Вырезка старого днища, монтаж нового листового днища ст. 09Г2С δ=10 мм, сварка, НК сварных швов",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.CRITICAL,
                "start_date": datetime(2024, 3, 28),
                "planned_end_date": datetime(2024, 4, 18),
                "actual_end_date": datetime(2024, 4, 18),
                "progress_percentage": 100.0,
                "assigned_to": "Сварщики НАКС + слесари"
            },
            {
                "project_id": projects[8].id,
                "name": "Ремонт стенки резервуара. Монтаж кровли",
                "description": "Замена дефектных поясов стенки, установка доборных листов, монтаж новой кровли, сварка и НК",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2024, 4, 18),
                "planned_end_date": datetime(2024, 5, 10),
                "actual_end_date": datetime(2024, 5, 10),
                "progress_percentage": 100.0,
                "assigned_to": "Монтажная бригада + сварщики"
            },
            {
                "project_id": projects[8].id,
                "name": "Антикоррозионная защита внутри резервуара",
                "description": "Дробеструйная очистка Sa 2.5, нанесение эпоксидного покрытия Belzona/Hempel 3 слоя, контроль сухой плёнки",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2024, 5, 10),
                "planned_end_date": datetime(2024, 5, 22),
                "actual_end_date": datetime(2024, 5, 21),
                "progress_percentage": 100.0,
                "assigned_to": "Бригада антикоррозионной защиты"
            },
            {
                "project_id": projects[8].id,
                "name": "Гидравлические испытания и сдача объекта",
                "description": "Заполнение резервуара водой, гидравлическое испытание на прочность и герметичность, устранение замечаний, сдача комиссии",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.CRITICAL,
                "start_date": datetime(2024, 5, 22),
                "planned_end_date": datetime(2024, 5, 30),
                "actual_end_date": datetime(2024, 5, 28),
                "progress_percentage": 100.0,
                "assigned_to": "ИТР + представитель Заказчика"
            },
        ]

        # ---- Tasks for large AVC portfolio projects (indices 9-12) ----
        tasks_project9 = [
            {"project_id": projects[9].id, "name": "Подготовка и вывод установок из эксплуатации",
             "description": "Остановка 23 установок, продувка, дренаж, наряды-допуски", "status": TaskStatus.COMPLETED,
             "priority": TaskPriority.CRITICAL, "start_date": datetime(2022, 4, 1),
             "planned_end_date": datetime(2022, 4, 10), "actual_end_date": datetime(2022, 4, 10),
             "progress_percentage": 100.0, "assigned_to": "ИТР + бригады подготовки"},
            {"project_id": projects[9].id, "name": "Ревизия и ремонт теплообменного оборудования (95 ед.)",
             "description": "Разборка, чистка, замена пучков, ревизия корпусов, сборка 95 теплообменников",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2022, 4, 11), "planned_end_date": datetime(2022, 6, 5),
             "actual_end_date": datetime(2022, 6, 4), "progress_percentage": 100.0,
             "assigned_to": "Слесари-ремонтники, сварщики НАКС"},
            {"project_id": projects[9].id, "name": "Ревизия ёмкостного и колонного оборудования (166 ед.)",
             "description": "ВКО, замена тарелок, уплотнений, дефектоскопия сварных швов",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2022, 4, 11), "planned_end_date": datetime(2022, 6, 15),
             "actual_end_date": datetime(2022, 6, 12), "progress_percentage": 100.0,
             "assigned_to": "Монтажники, сварщики"},
            {"project_id": projects[9].id, "name": "Замена насосного и прочего оборудования",
             "description": "Замена пароперегревателя Е-402, ёмкости Е-102, сепаратора С-302, 6 насосов",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2022, 4, 20), "planned_end_date": datetime(2022, 6, 20),
             "actual_end_date": datetime(2022, 6, 18), "progress_percentage": 100.0,
             "assigned_to": "Монтажники, механики"},
            {"project_id": projects[9].id, "name": "Пуск и испытания установок",
             "description": "Пуско-наладочные работы, гидроиспытания, вывод установок на рабочий режим",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2022, 6, 20), "planned_end_date": datetime(2022, 6, 28),
             "actual_end_date": datetime(2022, 6, 28), "progress_percentage": 100.0,
             "assigned_to": "ИТР, технологи"},
        ]
        tasks_project10 = [
            {"project_id": projects[10].id, "name": "ППР АНПЗ: подготовка и выполнение ремонтов (24 установки)",
             "description": "Одновременный ремонт CCR, ФКК, АВТ-2, компрессоров, реакторов, теплообменников",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2022, 9, 1), "planned_end_date": datetime(2022, 11, 10),
             "actual_end_date": datetime(2022, 11, 10), "progress_percentage": 100.0,
             "assigned_to": "1695 специалистов AVC Group"},
            {"project_id": projects[10].id, "name": "Замена трубопровода DR-201 (нерж. сталь, 152 м)",
             "description": "Установка CCR: демонтаж, сварка, монтаж трубопровода-осушителя Ду20–300 мм",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2022, 9, 10), "planned_end_date": datetime(2022, 10, 20),
             "actual_end_date": datetime(2022, 10, 18), "progress_percentage": 100.0,
             "assigned_to": "Сварщики НАКС, монтажники"},
        ]
        tasks_project11 = [
            {"project_id": projects[11].id, "name": "ППР АНПЗ: мобилизация и плановые ремонты (31 день)",
             "description": "Ремонт 24 установок за 31 рабочий день: CCR, АВТ-2, АВТ-3, УДГ, реакторы",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2023, 9, 1), "planned_end_date": datetime(2023, 10, 2),
             "actual_end_date": datetime(2023, 10, 2), "progress_percentage": 100.0,
             "assigned_to": "2220 специалистов AVC Group"},
            {"project_id": projects[11].id, "name": "Модернизация реакторов R-101, R-104 (CCR)",
             "description": "Замена внутренних устройств на более производительные",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2023, 9, 5), "planned_end_date": datetime(2023, 9, 28),
             "actual_end_date": datetime(2023, 9, 27), "progress_percentage": 100.0,
             "assigned_to": "Монтажники, механики"},
        ]
        tasks_project12 = [
            {"project_id": projects[12].id, "name": "Демонтаж старых компрессоров КТ-1",
             "description": "Остановка и демонтаж морально устаревшего компрессорного оборудования с 1981 г.",
             "status": TaskStatus.COMPLETED, "priority": TaskPriority.HIGH,
             "start_date": datetime(2023, 6, 1), "planned_end_date": datetime(2023, 9, 30),
             "actual_end_date": datetime(2023, 9, 28), "progress_percentage": 100.0,
             "assigned_to": "Монтажники, механики"},
            {"project_id": projects[12].id, "name": "Монтаж и наладка компрессоров Hitachi",
             "description": "Установка центробежных компрессоров жирного газа Hitachi, АСУ ТП, антипомпажная защита",
             "status": TaskStatus.IN_PROGRESS, "priority": TaskPriority.CRITICAL,
             "start_date": datetime(2023, 10, 1), "planned_end_date": datetime(2025, 7, 31),
             "progress_percentage": 75.0, "assigned_to": "Инженеры-механики, КИПиА"},
        ]

        all_tasks = (tasks_project1 + tasks_project2 + tasks_project3 +
                     tasks_project4 + tasks_project5 + tasks_project6 + tasks_project7 +
                     tasks_project8 + tasks_project9 + tasks_project10 +
                     tasks_project11 + tasks_project12)
        for task_data in all_tasks:
            task = Task(**task_data)
            db.add(task)

        db.commit()
        print(f"Created {len(all_tasks)} tasks")

        # ---- Resources for construction projects ----
        resources_project1 = [
            {
                "project_id": projects[0].id,
                "name": "Concrete M300",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 5000.0,
                "unit": "m3",
                "unit_cost": 12000.0,
                "supplier": "Astana Concrete Ltd"
            },
            {
                "project_id": projects[0].id,
                "name": "Steel Reinforcement Bars",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 80000.0,
                "unit": "kg",
                "unit_cost": 250.0,
                "supplier": "Kazakhstan Steel"
            },
            {
                "project_id": projects[0].id,
                "name": "Tower Crane",
                "resource_type": ResourceType.EQUIPMENT,
                "status": ResourceStatus.IN_USE,
                "quantity": 2.0,
                "unit": "units",
                "unit_cost": 150000.0,
                "supplier": "Heavy Equipment Rentals"
            },
            {
                "project_id": projects[0].id,
                "name": "Construction Workers",
                "resource_type": ResourceType.LABOR,
                "status": ResourceStatus.AVAILABLE,
                "quantity": 50.0,
                "unit": "workers",
                "unit_cost": 2500.0,
                "supplier": "BuildForce Agency"
            }
        ]

        resources_project2 = [
            {
                "project_id": projects[1].id,
                "name": "High-Grade Concrete M400",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 8000.0,
                "unit": "m3",
                "unit_cost": 15000.0,
                "supplier": "Premium Concrete Co"
            },
            {
                "project_id": projects[1].id,
                "name": "Excavator CAT 320",
                "resource_type": ResourceType.EQUIPMENT,
                "status": ResourceStatus.IN_USE,
                "quantity": 3.0,
                "unit": "units",
                "unit_cost": 80000.0,
                "supplier": "Heavy Machinery Rental"
            }
        ]

        # ---- Resources for AVC project 3: Теплообменник Е-101А ----
        resources_project3 = [
            {
                "project_id": projects[3].id,
                "name": "Сварщик 5 разряда (НАКС)",
                "resource_type": ResourceType.LABOR,
                "status": ResourceStatus.IN_USE,
                "quantity": 4.0,
                "unit": "чел/дн",
                "unit_cost": 18000.0,
            },
            {
                "project_id": projects[3].id,
                "name": "Слесарь-ремонтник 4 разряда",
                "resource_type": ResourceType.LABOR,
                "status": ResourceStatus.IN_USE,
                "quantity": 6.0,
                "unit": "чел/дн",
                "unit_cost": 12000.0,
            },
            {
                "project_id": projects[3].id,
                "name": "Трубный пучок теплообменника (новый)",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 1.0,
                "unit": "шт",
                "unit_cost": 18_000_000.0,
            },
            {
                "project_id": projects[3].id,
                "name": "Прокладки теплообменника (паронит ПОН-Б)",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 8.0,
                "unit": "шт",
                "unit_cost": 45000.0,
            },
            {
                "project_id": projects[3].id,
                "name": "Автокран 25т",
                "resource_type": ResourceType.EQUIPMENT,
                "status": ResourceStatus.IN_USE,
                "quantity": 1.0,
                "unit": "маш/см",
                "unit_cost": 120000.0,
            },
            {
                "project_id": projects[3].id,
                "name": "Установка гидроструйной чистки",
                "resource_type": ResourceType.EQUIPMENT,
                "status": ResourceStatus.IN_USE,
                "quantity": 1.0,
                "unit": "маш/см",
                "unit_cost": 85000.0,
            },
        ]

        # ---- Resources for AVC project 4: Насос ЦН-201 ----
        resources_project4 = [
            {
                "project_id": projects[4].id,
                "name": "Слесарь-ремонтник 5 разряда",
                "resource_type": ResourceType.LABOR,
                "status": ResourceStatus.IN_USE,
                "quantity": 3.0,
                "unit": "чел/дн",
                "unit_cost": 15000.0,
            },
            {
                "project_id": projects[4].id,
                "name": "Рабочее колесо насоса ЦН-201",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 1.0,
                "unit": "шт",
                "unit_cost": 3_500_000.0,
            },
            {
                "project_id": projects[4].id,
                "name": "Торцевое уплотнение John Crane",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 2.0,
                "unit": "шт",
                "unit_cost": 1_200_000.0,
            },
            {
                "project_id": projects[4].id,
                "name": "Подшипники SKF (комплект)",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 1.0,
                "unit": "комплект",
                "unit_cost": 850_000.0,
            },
            {
                "project_id": projects[4].id,
                "name": "Балансировочный стенд",
                "resource_type": ResourceType.EQUIPMENT,
                "status": ResourceStatus.IN_USE,
                "quantity": 1.0,
                "unit": "маш/см",
                "unit_cost": 65000.0,
            },
        ]

        # ---- Resources for AVC project 5: Трубопровод Ду300 ----
        resources_project5 = [
            {
                "project_id": projects[5].id,
                "name": "Сварщик 6 разряда (НАКС)",
                "resource_type": ResourceType.LABOR,
                "status": ResourceStatus.IN_USE,
                "quantity": 6.0,
                "unit": "чел/дн",
                "unit_cost": 22000.0,
            },
            {
                "project_id": projects[5].id,
                "name": "Монтажник трубопроводов 5 разряда",
                "resource_type": ResourceType.LABOR,
                "status": ResourceStatus.IN_USE,
                "quantity": 4.0,
                "unit": "чел/дн",
                "unit_cost": 15000.0,
            },
            {
                "project_id": projects[5].id,
                "name": "Изолировщик 4 разряда",
                "resource_type": ResourceType.LABOR,
                "status": ResourceStatus.IN_USE,
                "quantity": 3.0,
                "unit": "чел/дн",
                "unit_cost": 12000.0,
            },
            {
                "project_id": projects[5].id,
                "name": "Труба 09Г2С Ду300 ст.10мм",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 120.0,
                "unit": "м",
                "unit_cost": 45000.0,
            },
            {
                "project_id": projects[5].id,
                "name": "Сварочные электроды УОНИ 13/55",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 200.0,
                "unit": "кг",
                "unit_cost": 1500.0,
            },
            {
                "project_id": projects[5].id,
                "name": "Минеральная вата 80мм (изоляция)",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 90.0,
                "unit": "м2",
                "unit_cost": 3500.0,
            },
            {
                "project_id": projects[5].id,
                "name": "Трубоукладчик",
                "resource_type": ResourceType.EQUIPMENT,
                "status": ResourceStatus.IN_USE,
                "quantity": 1.0,
                "unit": "маш/см",
                "unit_cost": 150000.0,
            },
        ]

        # ---- Resources for AVC project 6: Печь П-101 ----
        resources_project6 = [
            {
                "project_id": projects[6].id,
                "name": "Огнеупорщик 5 разряда",
                "resource_type": ResourceType.LABOR,
                "status": ResourceStatus.IN_USE,
                "quantity": 8.0,
                "unit": "чел/дн",
                "unit_cost": 16000.0,
            },
            {
                "project_id": projects[6].id,
                "name": "Сварщик 5 разряда (НАКС)",
                "resource_type": ResourceType.LABOR,
                "status": ResourceStatus.IN_USE,
                "quantity": 4.0,
                "unit": "чел/дн",
                "unit_cost": 18000.0,
            },
            {
                "project_id": projects[6].id,
                "name": "Слесарь КИПиА 5 разряда",
                "resource_type": ResourceType.LABOR,
                "status": ResourceStatus.IN_USE,
                "quantity": 2.0,
                "unit": "чел/дн",
                "unit_cost": 17000.0,
            },
            {
                "project_id": projects[6].id,
                "name": "Кирпич огнеупорный ШБ-5",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 15000.0,
                "unit": "шт",
                "unit_cost": 800.0,
            },
            {
                "project_id": projects[6].id,
                "name": "Труба жаропрочная 15Х5М (змеевик)",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 12.0,
                "unit": "шт",
                "unit_cost": 1_800_000.0,
            },
            {
                "project_id": projects[6].id,
                "name": "Форсунки горелок (комплект)",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 6.0,
                "unit": "шт",
                "unit_cost": 450_000.0,
            },
            {
                "project_id": projects[6].id,
                "name": "Леса строительные (комплект)",
                "resource_type": ResourceType.EQUIPMENT,
                "status": ResourceStatus.IN_USE,
                "quantity": 1.0,
                "unit": "комплект",
                "unit_cost": 350_000.0,
            },
        ]

        # ---- Resources for AVC project 7: Компрессор К-301 ----
        resources_project7 = [
            {
                "project_id": projects[7].id,
                "name": "Механик по компрессорному оборудованию",
                "resource_type": ResourceType.LABOR,
                "status": ResourceStatus.IN_USE,
                "quantity": 4.0,
                "unit": "чел/дн",
                "unit_cost": 25000.0,
            },
            {
                "project_id": projects[7].id,
                "name": "Слесарь-ремонтник 5 разряда",
                "resource_type": ResourceType.LABOR,
                "status": ResourceStatus.IN_USE,
                "quantity": 6.0,
                "unit": "чел/дн",
                "unit_cost": 15000.0,
            },
            {
                "project_id": projects[7].id,
                "name": "Лабиринтные уплотнения (комплект)",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 1.0,
                "unit": "комплект",
                "unit_cost": 12_000_000.0,
            },
            {
                "project_id": projects[7].id,
                "name": "Подшипники скольжения (комплект)",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 1.0,
                "unit": "комплект",
                "unit_cost": 8_500_000.0,
            },
            {
                "project_id": projects[7].id,
                "name": "Упорный подшипник Kingsbury",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 1.0,
                "unit": "шт",
                "unit_cost": 5_200_000.0,
            },
            {
                "project_id": projects[7].id,
                "name": "Лазерная центровочная система",
                "resource_type": ResourceType.EQUIPMENT,
                "status": ResourceStatus.IN_USE,
                "quantity": 1.0,
                "unit": "маш/см",
                "unit_cost": 45000.0,
            },
        ]

        # ---- Resources for AVC project 8: Резервуар РВС-10000 №3 ----
        resources_project8 = [
            {
                "project_id": projects[8].id,
                "name": "Сварщик 6 разряда (НАКС, резервуарная сварка)",
                "resource_type": ResourceType.LABOR,
                "status": ResourceStatus.AVAILABLE,
                "quantity": 8.0,
                "unit": "чел/дн",
                "unit_cost": 20000.0,
            },
            {
                "project_id": projects[8].id,
                "name": "Монтажник металлоконструкций 5 разряда",
                "resource_type": ResourceType.LABOR,
                "status": ResourceStatus.AVAILABLE,
                "quantity": 10.0,
                "unit": "чел/дн",
                "unit_cost": 15000.0,
            },
            {
                "project_id": projects[8].id,
                "name": "Слесарь-ремонтник 4 разряда",
                "resource_type": ResourceType.LABOR,
                "status": ResourceStatus.AVAILABLE,
                "quantity": 6.0,
                "unit": "чел/дн",
                "unit_cost": 12000.0,
            },
            {
                "project_id": projects[8].id,
                "name": "Маляр-изолировщик (антикоррозионная защита)",
                "resource_type": ResourceType.LABOR,
                "status": ResourceStatus.AVAILABLE,
                "quantity": 4.0,
                "unit": "чел/дн",
                "unit_cost": 14000.0,
            },
            {
                "project_id": projects[8].id,
                "name": "Листовой прокат ст. 09Г2С δ=10 мм (днище)",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.AVAILABLE,
                "quantity": 85.0,
                "unit": "т",
                "unit_cost": 520000.0,
            },
            {
                "project_id": projects[8].id,
                "name": "Листовой прокат ст. 09Г2С δ=8 мм (стенка/кровля)",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.AVAILABLE,
                "quantity": 45.0,
                "unit": "т",
                "unit_cost": 500000.0,
            },
            {
                "project_id": projects[8].id,
                "name": "Покрытие антикоррозионное эпоксидное Hempel",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.AVAILABLE,
                "quantity": 6000.0,
                "unit": "кг",
                "unit_cost": 3500.0,
            },
            {
                "project_id": projects[8].id,
                "name": "Автокран 50т",
                "resource_type": ResourceType.EQUIPMENT,
                "status": ResourceStatus.AVAILABLE,
                "quantity": 2.0,
                "unit": "маш/см",
                "unit_cost": 200000.0,
            },
            {
                "project_id": projects[8].id,
                "name": "Дробеструйная установка",
                "resource_type": ResourceType.EQUIPMENT,
                "status": ResourceStatus.AVAILABLE,
                "quantity": 2.0,
                "unit": "маш/см",
                "unit_cost": 90000.0,
            },
            {
                "project_id": projects[8].id,
                "name": "Сварочный полуавтомат ESAB",
                "resource_type": ResourceType.EQUIPMENT,
                "status": ResourceStatus.AVAILABLE,
                "quantity": 4.0,
                "unit": "маш/см",
                "unit_cost": 25000.0,
            },
        ]

        # ---- Resources for large AVC portfolio projects (indices 9-12) ----
        resources_project9 = [
            {"project_id": projects[9].id, "name": "Специалисты инженерных профессий (ИТР)",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 83.0, "unit": "чел/дн", "unit_cost": 30000.0},
            {"project_id": projects[9].id, "name": "Рабочие специальностей (сварщики, слесари, монтажники)",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 1292.0, "unit": "чел/дн", "unit_cost": 14000.0},
            {"project_id": projects[9].id, "name": "Автокраны и грузоподъёмная техника",
             "resource_type": ResourceType.EQUIPMENT, "status": ResourceStatus.AVAILABLE,
             "quantity": 30.0, "unit": "маш/см", "unit_cost": 180000.0},
            {"project_id": projects[9].id, "name": "Спецтехника (экскаваторы, трубоукладчики, ДВС)",
             "resource_type": ResourceType.EQUIPMENT, "status": ResourceStatus.AVAILABLE,
             "quantity": 20.0, "unit": "маш/см", "unit_cost": 120000.0},
        ]
        resources_project10 = [
            {"project_id": projects[10].id, "name": "Специалисты всех профессий (ППР АНПЗ 1-й цикл)",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 1695.0, "unit": "чел/дн", "unit_cost": 15000.0},
            {"project_id": projects[10].id, "name": "Грузоподъёмная и спецтехника",
             "resource_type": ResourceType.EQUIPMENT, "status": ResourceStatus.AVAILABLE,
             "quantity": 69.0, "unit": "маш/см", "unit_cost": 160000.0},
        ]
        resources_project11 = [
            {"project_id": projects[11].id, "name": "Специалисты всех профессий (ППР АНПЗ 2-й цикл)",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.AVAILABLE,
             "quantity": 2220.0, "unit": "чел/дн", "unit_cost": 15000.0},
            {"project_id": projects[11].id, "name": "Краны (26 ед.)",
             "resource_type": ResourceType.EQUIPMENT, "status": ResourceStatus.AVAILABLE,
             "quantity": 26.0, "unit": "маш/см", "unit_cost": 200000.0},
            {"project_id": projects[11].id, "name": "Спецтехника ДВС, длинномеры, экскаваторы (20 ед.)",
             "resource_type": ResourceType.EQUIPMENT, "status": ResourceStatus.AVAILABLE,
             "quantity": 20.0, "unit": "маш/см", "unit_cost": 100000.0},
        ]
        resources_project12 = [
            {"project_id": projects[12].id, "name": "Инженеры-механики и КИПиА",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.IN_USE,
             "quantity": 25.0, "unit": "чел/дн", "unit_cost": 35000.0},
            {"project_id": projects[12].id, "name": "Слесари-монтажники 5–6 разряда",
             "resource_type": ResourceType.LABOR, "status": ResourceStatus.IN_USE,
             "quantity": 40.0, "unit": "чел/дн", "unit_cost": 18000.0},
            {"project_id": projects[12].id, "name": "Компрессоры жирного газа Hitachi (новые)",
             "resource_type": ResourceType.MATERIAL, "status": ResourceStatus.IN_USE,
             "quantity": 2.0, "unit": "шт", "unit_cost": 280_000_000.0},
            {"project_id": projects[12].id, "name": "Автокран 100т",
             "resource_type": ResourceType.EQUIPMENT, "status": ResourceStatus.IN_USE,
             "quantity": 2.0, "unit": "маш/см", "unit_cost": 350000.0},
        ]

        all_resources = (resources_project1 + resources_project2 + resources_project3 +
                         resources_project4 + resources_project5 + resources_project6 +
                         resources_project7 + resources_project8 +
                         resources_project9 + resources_project10 +
                         resources_project11 + resources_project12)
        for resource_data in all_resources:
            resource = Resource(**resource_data)
            resource.calculate_total_cost()
            db.add(resource)

        db.commit()
        print(f"Created {len(all_resources)} resources")

        # ---- Budgets for construction projects ----
        budgets = [
            {
                "project_id": projects[0].id,
                "category": "Materials",
                "description": "Concrete, steel, bricks, etc.",
                "planned_amount": 3500000.0,
                "actual_amount": 1800000.0
            },
            {
                "project_id": projects[0].id,
                "category": "Labor",
                "description": "Construction workers, engineers",
                "planned_amount": 2500000.0,
                "actual_amount": 950000.0
            },
            {
                "project_id": projects[0].id,
                "category": "Equipment",
                "description": "Cranes, excavators, tools",
                "planned_amount": 1500000.0,
                "actual_amount": 450000.0
            },
            {
                "project_id": projects[0].id,
                "category": "Permits and Insurance",
                "description": "Legal and safety requirements",
                "planned_amount": 500000.0,
                "actual_amount": 0.0
            },
            {
                "project_id": projects[1].id,
                "category": "Materials",
                "description": "Premium construction materials",
                "planned_amount": 6000000.0,
                "actual_amount": 2100000.0
            },
            {
                "project_id": projects[1].id,
                "category": "Labor",
                "description": "Specialized construction teams",
                "planned_amount": 4500000.0,
                "actual_amount": 1500000.0
            },
            {
                "project_id": projects[1].id,
                "category": "Equipment",
                "description": "Heavy machinery and tools",
                "planned_amount": 2500000.0,
                "actual_amount": 900000.0
            },
            # ---- Budgets for AVC projects ----
            {
                "project_id": projects[3].id,
                "category": "Материалы",
                "description": "Трубный пучок, прокладки, метизы",
                "planned_amount": 22_000_000.0,
                "actual_amount": 21_500_000.0
            },
            {
                "project_id": projects[3].id,
                "category": "Работа",
                "description": "Сварщики, слесари, дефектоскописты",
                "planned_amount": 15_000_000.0,
                "actual_amount": 14_200_000.0
            },
            {
                "project_id": projects[3].id,
                "category": "Техника",
                "description": "Автокран, установка гидрочистки",
                "planned_amount": 8_000_000.0,
                "actual_amount": 7_500_000.0
            },
            {
                "project_id": projects[4].id,
                "category": "Запчасти",
                "description": "Рабочее колесо, уплотнения, подшипники",
                "planned_amount": 7_500_000.0,
                "actual_amount": 7_750_000.0
            },
            {
                "project_id": projects[4].id,
                "category": "Работа",
                "description": "Слесари, механики, балансировка",
                "planned_amount": 5_000_000.0,
                "actual_amount": 5_350_000.0
            },
            {
                "project_id": projects[5].id,
                "category": "Материалы",
                "description": "Трубы 09Г2С, электроды, изоляция",
                "planned_amount": 12_000_000.0,
                "actual_amount": 12_800_000.0
            },
            {
                "project_id": projects[5].id,
                "category": "Работа",
                "description": "Сварщики, монтажники, изолировщики",
                "planned_amount": 10_000_000.0,
                "actual_amount": 10_500_000.0
            },
            {
                "project_id": projects[5].id,
                "category": "НК и испытания",
                "description": "Радиографический контроль, гидроиспытания",
                "planned_amount": 6_000_000.0,
                "actual_amount": 6_200_000.0
            },
            {
                "project_id": projects[6].id,
                "category": "Материалы",
                "description": "Огнеупорный кирпич, трубы змеевика, форсунки",
                "planned_amount": 40_000_000.0,
                "actual_amount": 38_500_000.0
            },
            {
                "project_id": projects[6].id,
                "category": "Работа",
                "description": "Огнеупорщики, сварщики, КИПиА",
                "planned_amount": 30_000_000.0,
                "actual_amount": 28_500_000.0
            },
            {
                "project_id": projects[6].id,
                "category": "Оборудование и леса",
                "description": "Строительные леса, инструмент, расходники",
                "planned_amount": 15_000_000.0,
                "actual_amount": 15_000_000.0
            },
            {
                "project_id": projects[7].id,
                "category": "Запчасти",
                "description": "Уплотнения, подшипники, упорный подшипник",
                "planned_amount": 55_000_000.0,
                "actual_amount": 30_000_000.0
            },
            {
                "project_id": projects[7].id,
                "category": "Работа",
                "description": "Механики, слесари, наладчики",
                "planned_amount": 45_000_000.0,
                "actual_amount": 25_000_000.0
            },
            {
                "project_id": projects[7].id,
                "category": "Оборудование",
                "description": "Центровочная система, стенды, инструмент",
                "planned_amount": 20_000_000.0,
                "actual_amount": 10_000_000.0
            },
            # ---- Budgets for AVC project 8: Резервуар РВС-10000 №3 ----
            {
                "project_id": projects[8].id,
                "category": "Материалы",
                "description": "Листовой прокат, антикоррозионные покрытия, электроды, расходники",
                "planned_amount": 68_000_000.0,
                "actual_amount": 67_200_000.0
            },
            {
                "project_id": projects[8].id,
                "category": "Работа",
                "description": "Сварщики НАКС, монтажники, слесари, маляры-изолировщики",
                "planned_amount": 32_000_000.0,
                "actual_amount": 31_500_000.0
            },
            {
                "project_id": projects[8].id,
                "category": "Техника и оборудование",
                "description": "Автокраны 50т, дробеструйные установки, сварочное оборудование",
                "planned_amount": 12_000_000.0,
                "actual_amount": 11_800_000.0
            },
            {
                "project_id": projects[8].id,
                "category": "НК и испытания",
                "description": "Радиографический контроль сварных швов, УЗК, гидравлические испытания",
                "planned_amount": 6_000_000.0,
                "actual_amount": 5_200_000.0
            },
            # ---- Budgets for AVC large turnaround projects (9-12) ----
            {"project_id": projects[9].id, "category": "ФОТ и подрядные работы",
             "description": "1375 специалистов, ИТР 83 чел. + рабочие 1292 чел.",
             "planned_amount": 1_800_000_000.0, "actual_amount": 1_790_000_000.0},
            {"project_id": projects[9].id, "category": "Материалы и запчасти",
             "description": "Трубные пучки, прокладки, ЗРА, КИП, сварочные материалы",
             "planned_amount": 450_000_000.0, "actual_amount": 445_000_000.0},
            {"project_id": projects[9].id, "category": "Техника и оборудование",
             "description": "50 ед. спецтехники: краны, трубоукладчики, экскаваторы",
             "planned_amount": 250_000_000.0, "actual_amount": 245_000_000.0},
            {"project_id": projects[10].id, "category": "ФОТ и подрядные работы",
             "description": "1695 специалистов на 24 установках АНПЗ (1-й цикл)",
             "planned_amount": 3_000_000_000.0, "actual_amount": 2_980_000_000.0},
            {"project_id": projects[10].id, "category": "Техника",
             "description": "69 ед. грузоподъёмной и спецтехники",
             "planned_amount": 1_200_000_000.0, "actual_amount": 1_170_000_000.0},
            {"project_id": projects[11].id, "category": "ФОТ (2220 чел., 31 день)",
             "description": "Мобилизация и работа 2220 специалистов",
             "planned_amount": 2_200_000_000.0, "actual_amount": 2_190_000_000.0},
            {"project_id": projects[11].id, "category": "Техника (95 ед.)",
             "description": "26 кранов, 12 ДВС/длинномеров, 8 экскаваторов + прочее",
             "planned_amount": 900_000_000.0, "actual_amount": 860_000_000.0},
            {"project_id": projects[12].id, "category": "Оборудование Hitachi",
             "description": "Центробежные компрессоры жирного газа, АСУ ТП, антипомпажная защита",
             "planned_amount": 700_000_000.0, "actual_amount": 530_000_000.0},
            {"project_id": projects[12].id, "category": "СМР и пуско-наладка",
             "description": "Монтаж, обвязка, пуско-наладочные работы, интеграция пожаротушения",
             "planned_amount": 150_000_000.0, "actual_amount": 90_000_000.0},
        ]

        for budget_data in budgets:
            budget = Budget(**budget_data)
            db.add(budget)

        db.commit()
        print(f"Created {len(budgets)} budget entries")

        # ---- Precompute embeddings for all projects ----
        print("Computing embeddings for projects (this may take a moment)...")
        similarity = SimilarityService(db)
        for proj in projects:
            db.refresh(proj)
        for proj in projects:
            try:
                similarity.index_project(proj)
                print(f"  Indexed: {proj.name[:50]}")
            except Exception as e:
                print(f"  Failed to index {proj.name[:50]}: {e}")

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
