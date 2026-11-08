from decimal import Decimal
from typing import Literal

from fluent_compiler.types import FluentType
from typing_extensions import TypeAlias

PossibleValue: TypeAlias = str | int | float | Decimal | bool | FluentType

class TranslatorRunner:
    def get(self, path: str, **kwargs: PossibleValue) -> str: ...
    user: User
    admin: Admin

class UserMenuWindow1:
    @staticmethod
    def text() -> Literal["""Вы тоже давно хотите сделать свой мини-продукт, как у крупных блогеров? Но что-то мешает? 

То тему выбрать не можете.
То кажется, что знаний недостаточно.
То начинаете прикидывать, сколько всего нужно записать, оформить, настроить…

И думаете: ладно, потом 🫠

А потом снова работа, клиенты, контент. До своего продукта руки так и не доходят.

Я тоже откладывала, а потом села и сделала за вечер. 
Я продавала миник по созданию AI-аватара. 

Здесь хочу разобрать, как вы можете собрать продукт из своих знаний. И как подключить ChatGPT, чтобы не сидеть над каждым текстом до пенсии.

Сначала покажу свой пример 👇🏻"""]: ...
    @staticmethod
    def button() -> Literal["""Смотреть пример"""]: ...

class UserMenuWindow2:
    @staticmethod
    def text() -> Literal["""Вот оплаты моего миника по созданию AI-аватара ☝🏻

Я продавала один мини-продукт. Взяла конкретную тему, которую знаю и с которой могу помочь.

Человеку понятно, зачем ему такое обучение: он хочет создать своего аватара.

С вашим продуктом нужно найти такую же конкретику.

Что человек хочет сделать?
В чём застревает?
Что вы умеете объяснить или показать, чтобы у него получилось?

Вот отсюда и начинаем.

Потому что в голове у вас может быть десять лет опыта. Но покупателю ещё нужно понять, как этот опыт поможет лично ему.

Давайте покажу, как подойти к своему минику 👇🏻"""]: ...
    @staticmethod
    def button() -> Literal["""Хочу посмотреть шаги"""]: ...

class UserMenuWindow3:
    @staticmethod
    def text() -> Literal["""С чего начать свой миник 👇🏻

1️⃣ Посмотрите, о чём вас уже спрашивают

В личке, на консультациях, в комментариях.

Что вы постоянно объясняете? С чем к вам обращаются? Где человек сам разобраться не может, а вы понимаете, что делать?

Выпишите эти вопросы. Здесь могут быть темы для вашего продукта.

Но сам вопрос ещё не означает, что за ответ готовы платить. Это дальше проверяем.

2️⃣ Решите, что человек получит

Прямо закончите фразу:

«После моего миника человек сможет…»

Создать аватара. Собрать резюме под вакансию. Составить меню на неделю.


3️⃣ Выберите формат, который сможете сделать

Возможно, вам хватит нескольких коротких уроков. Или инструкции с примерами. Или шаблона и видео, где вы показываете, как им пользоваться.

4️⃣ Подключите ChatGPT

С его помощью можно разобрать ваши знания, собрать структуру, подготовить черновики уроков, задания и описание продукта.

Но свой опыт и примеры добавляете вы. И содержание проверяете тоже вы.


5️⃣ Соберите предложение и покажите людям

Для кого продукт? Что поможет сделать? Что внутри? Сколько стоит? Как получить доступ?

Расскажите о нём подходящей аудитории. Посмотрите, что спрашивают, на что откликаются, покупают ли.

6️⃣ Подготовьте материал и определитесь где его разместите.

7️⃣ Настройте автоматическую выдачу в боте и оплату. 



Если хотите пройти эти шаги со мной, я собрала уроки и промпты для работы над миником 👇🏻"""]: ...
    @staticmethod
    def button() -> Literal["""Что внутри?"""]: ...

class UserMenuWindow4:
    @staticmethod
    def text() -> Literal["""«Мини-продукт с AI»

Для тех, кто хочет наконец собрать свой миник, но пока буксует на теме, структуре или вечном «я не понимаю, с чего начать».

Внутри 7 уроков с демонстрацией на конкретном примере. 

Вот что будем делать:

1️⃣ Разберём ваш опыт
На какие знания, навыки и результаты можно опереться при создании продукта.

2️⃣ Выберем аудиторию и задачу
Кому вы можете помочь, что этим людям нужно и как проверить интерес к теме.

3️⃣ Соберём структуру
Какой результат даёте, что для этого положить внутрь и какой формат выбрать.

4️⃣ Подготовим содержание с AI
Материалы, объяснения, задания. Чтобы вы не зависали перед пустым документом.

5️⃣ Запишем и соберём продукт
Разберём, как превратить заготовки в материалы, которыми человек сможет пользоваться.

6️⃣ Упакуем и определим цену
Чтобы вы могли понятно рассказать, что продаёте, кому и за сколько.

7️⃣ Подготовим размещение и запуск
Где выдавать продукт и с каких действий начать продажи.

Промпты используете по ходу работы. Прошли шаг, поработали над своим продуктом, двигаетесь дальше."""]: ...
    @staticmethod
    def button(*, price: PossibleValue) -> Literal["""Купить за { $price } ₽"""]: ...

class UserMenu:
    window1: UserMenuWindow1
    window2: UserMenuWindow2
    window3: UserMenuWindow3
    window4: UserMenuWindow4

class UserSpam:
    @staticmethod
    def warning() -> Literal["""Осторожно, не отправляйте сообщения так часто!"""]: ...
    @staticmethod
    def notify() -> Literal["""Вы были заблокированы за спам."""]: ...

class UserInvoice:
    @staticmethod
    def title() -> Literal["""Заголовок счета"""]: ...
    @staticmethod
    def description() -> Literal["""Описание счета на оплату."""]: ...

class User:
    menu: UserMenu
    spam: UserSpam
    invoice: UserInvoice

    @staticmethod
    def paid() -> Literal["""Похоже, у вас уже есть доступ! Просто перейдите в бота @mini_product_ai"""]: ...

class AdminButton:
    @staticmethod
    def back() -> Literal["""⬅️ Назад"""]: ...
    @staticmethod
    def skip() -> Literal["""➡️ Пропустить"""]: ...
    @staticmethod
    def confirm() -> Literal["""✅ Подтвердить"""]: ...

class AdminMenuButton:
    @staticmethod
    def metrics() -> Literal["""📊 Метрика"""]: ...
    @staticmethod
    def mailing() -> Literal["""✉️ Рассылка"""]: ...
    @staticmethod
    def user() -> Literal["""👥 Найти"""]: ...
    @staticmethod
    def price() -> Literal["""💵 Цена"""]: ...
    @staticmethod
    def leave() -> Literal["""🚪 Выйти"""]: ...

class AdminMenu:
    button: AdminMenuButton

    @staticmethod
    def text(*, price: PossibleValue) -> Literal["""&lt;b&gt;Добро пожаловать в админ-панель бота!&lt;/b&gt;

Цена для продукта: { $price } ₽"""]: ...

class AdminMetricsGeneral:
    @staticmethod
    def text(*, active: PossibleValue, dead: PossibleValue, paid: PossibleValue, users: PossibleValue) -> Literal["""&lt;b&gt;За все время:&lt;/b&gt;

👥 Пользователей: { $users } чел.
🤑 Купили: { $paid } чел.
🟢 Активных: { $active } чел.
🔴 Неактивных: { $dead } чел."""]: ...
    @staticmethod
    def button() -> Literal["""📆 За период"""]: ...

class AdminMetricsSendleft:
    @staticmethod
    def text() -> Literal["""Введите левую границу периода (дата в формате ДД.ММ.ГГГГ)."""]: ...

class AdminMetricsSendright:
    @staticmethod
    def text() -> Literal["""Введите правую границу периода (дата в формате ДД.ММ.ГГГГ)."""]: ...

class AdminMetricsInvalid:
    @staticmethod
    def text() -> Literal["""Правая граница периода не может быть больше левой!"""]: ...

class AdminMetricsPeriod:
    @staticmethod
    def text(*, buys: PossibleValue, first_starts: PossibleValue, left: PossibleValue, right: PossibleValue) -> Literal["""&lt;b&gt;С { $left } по { $right }:&lt;/b&gt;

👥 Запустили бота впервые: { $first_starts } чел.
🤑 Купили: { $buys } чел."""]: ...

class AdminMetrics:
    general: AdminMetricsGeneral
    sendleft: AdminMetricsSendleft
    sendright: AdminMetricsSendright
    invalid: AdminMetricsInvalid
    period: AdminMetricsPeriod

class Admin:
    button: AdminButton
    menu: AdminMenu
    metrics: AdminMetrics
