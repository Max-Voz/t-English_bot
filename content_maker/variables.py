from typing import Dict, List

back_icon = "\U0001F519"
balloon_icon = "\U0001f4ad"
books_icon = "\U0001F4DA"
checkbox_icon = "\u2705"
checkmark_icon = "\u2714"
house_icon = "\U0001F3E0"
pencil_icon = "\U0001F4DD"
phone_icon = "\U0001F4F1"
pin_icon = "\U0001F4CC"
question_icon = "\u2754"
world_icon = "\U0001F310"

COURSES: Dict[str, str] = {
    "Для девов":
        f"Курс для девов:\n\n"
        f"{pin_icon} Коммуникативный курс, индивидуальный или в паре;\n"
        f"{pin_icon} Как описывать технические решения или проблемы;\n"
        f"{pin_icon} Общение с заказчиком и членами удаленной команды;\n"
        f"{pin_icon} Демо и релизы;\n"
        f"{pin_icon} Участие в Scrum-митингах.\n",
    "Для QA":
        f"Курс для QA:\n\n"
        f"{pin_icon}Коммуникативный курс, индивидуальный или в паре;\n"
        f"{pin_icon}Написание и презентация тест-кейсов и тест-планов;\n"
        f"{pin_icon}Общение с удаленной командой разработчиков;\n"
        f"{pin_icon}Обсуждение “багов”;\n"
        f"{pin_icon}Работа с документацией.\n",
    "Подготовка к интервью":
        f"Курс Подготовка к интервью:\n\n"
        f"{pin_icon} Индивидуальный коммуникативный курс;\n"
        f"{pin_icon} Как пройти техническое интервью;\n"
        f"{pin_icon} Самопрезентация;\n"
        f"{pin_icon} Ответы на кейсовые/ситуационные вопросы;\n"
        f"{pin_icon} Как структурировать свои мысли и идеи.\n",
    "Для IT-менеджеров":
        f"Курс для IT-менеджеров:\n\n"
        f"{pin_icon} Коммуникативный курс, индивидуальный или в паре;\n"
        f"{pin_icon} Для BA, PM, Product менеджеров, Scrum-мастеров;\n"
        f"{pin_icon} Scrum митинги, созвоны с заказчиком;\n"
        f"{pin_icon} Проектная коммуникация;\n"
        f"{pin_icon} Планирование, целеполагание, эстимация;\n"
        f"{pin_icon} Менеджмент задач и команды.\n",
    "Для UI/UX":
        f"Курс для UI/UX:\n\n"
        f"{pin_icon} Описание и оценка требований пользователя;\n"
        f"{pin_icon} Как иллюстрировать идеи, используя сториборд, "
        f"карты тех.процесса и Sitemap;\n"
        f"{pin_icon} Презентация драфтов и прототипов для стейкхолдеров;\n"
        f"{pin_icon} Описание UX-проблем и поиск решений;\n"
        f"{pin_icon} Презентация и обсуждение customer journey map, "
        f"создание сценариев, design research;\n"
        f"{pin_icon} Работа с веб-аналитикой и презентация "
        f"результатов тестирования.\n",
    "Для свитчеров":
        f"Курс для свитчеров:\n\n"
        f"{pin_icon} 30 часов занятий в группе до 5 человек;\n"
        f"{pin_icon} Преподаватели с опытом работы в ИТ;\n"
        f"{pin_icon} Практические задания с реальными кейсами "
        f"вместо домашки;\n"
        f"{pin_icon} Social learning;\n"
        f"{pin_icon} Лонгриды и видео для глубокого погружения;\n"
        f"{pin_icon} Удобный график для каждой группы.\n",
}

RESOURCES: Dict[str, str] = {
    "telegram": "https://t.me/TiEnglish",
    "youtube": "https://www.youtube.com/channel/UCVqPkDCpmh7banukNyKMkGg",
    "instagram": "https://www.instagram.com/t.english4it/",
}
main_menu_buttons: List[List[str]] = [
    [f"{books_icon} Курсы", "courses"],
    [f"{checkbox_icon}{pencil_icon} Оставить заявку", "leave_application"],
    [f"{world_icon} Ресурсы по английскому для IT", "resources"],
]

courses_buttons_choose: List[List[str]] = [
    [f"{checkmark_icon} {course}", f"{course}|ch"] for course in COURSES
]
courses_buttons_choose.append(
    [f"{question_icon} Я пока не уверен в выборе курса", "Не уверен|ch"]
)

courses_buttons: List[List[str]] = [
    [f"{checkmark_icon} {course}", course] for course in COURSES
]
courses_buttons.append(
    [f"{house_icon} Вернуться в главное меню", "main_menu"]
)
one_course_buttons: List[List[str]] = [
    [f"{back_icon} К выбору курса", "courses"],
    [f"{checkbox_icon}{pencil_icon} Оставить заявку", "leave_application"],
    [f"{house_icon} В главное меню", "main_menu"],
]
resources_buttons: List[List[str]] = [
    [f"Telegram", f'{RESOURCES["telegram"]}'],
    [f"Youtube", f'{RESOURCES["youtube"]}'],
    [f"Instagram", f'{RESOURCES["instagram"]}'],
    [f"{house_icon} В главное меню", "main_menu"],
]

home_apply_buttons: List[List[str]] = [
    [
        f"{checkbox_icon}{pencil_icon}"
        f" Оставить заявку",
        "leave_application",
    ],
    [f"{house_icon} В главное меню", "main_menu"],
]

single_home_button: List[List[str]] = [
    [f"{house_icon} В главное меню", "main_menu"]
]

finish_buttons: List[List[str]] = [
    [f"Да", "apply_yes"],
    [f"Нет", "apply_no"],
]
