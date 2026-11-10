from decimal import Decimal
from typing import Literal

from fluent_compiler.types import FluentType
from typing_extensions import TypeAlias

PossibleValue: TypeAlias = str | int | float | Decimal | bool | FluentType

class TranslatorRunner:
    def get(self, path: str, **kwargs: PossibleValue) -> str: ...
    admin: Admin
    user: User

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
    def price() -> Literal["""💵 Изменить Цену"""]: ...
    @staticmethod
    def leave() -> Literal["""🚪 Выйти"""]: ...

class AdminMenu:
    button: AdminMenuButton

    @staticmethod
    def text(*, price: PossibleValue) -> Literal["""&lt;b&gt;Добро пожаловать в админ-панель бота!&lt;/b&gt;

Цена для продукта: { $price } ₽"""]: ...

class AdminMetricsGeneral:
    @staticmethod
    def text(*, alive: PossibleValue, dead: PossibleValue, paid: PossibleValue, users: PossibleValue) -> Literal["""&lt;b&gt;За все время:&lt;/b&gt;

👥 Пользователей: { $users } чел.
🤑 Купили: { $paid } чел.
🟢 Активных: { $alive } чел.
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

class AdminMailingSendtext:
    @staticmethod
    def text() -> Literal["""Введите текст рассылки"""]: ...

class AdminMailingSendmedia:
    @staticmethod
    def text() -> Literal["""Отправьте фото|видео|кружок (не более 30 Мб)"""]: ...

class AdminMailingExamle:
    @staticmethod
    def text() -> Literal["""Каждому пользователю без доступа в клуб будет отправлено следующее ⬇️"""]: ...

class AdminMailingConfirm:
    @staticmethod
    def text() -> Literal["""&lt;b&gt;&lt;i&gt;Подтвердить??&lt;/i&gt;&lt;/b&gt;"""]: ...

class AdminMailingStarted:
    @staticmethod
    def text(*, mailing_id: PossibleValue) -> Literal["""✅ Рассылка всем пользователям без доступа в клуб началась. По мере ее обработки вам будут приходить уведомления.
⚙️ ID рассылки: { $mailing_id }

⬇️ Нажмите на кнопку ниже для возвращения в меню"""]: ...

class AdminMailing:
    sendtext: AdminMailingSendtext
    sendmedia: AdminMailingSendmedia
    examle: AdminMailingExamle
    confirm: AdminMailingConfirm
    started: AdminMailingStarted

class AdminPriceWindow:
    @staticmethod
    def text() -> Literal["""Задайте цену для товара, обязательно укажите копейки после точки! Формат: Р.КК"""]: ...

class AdminPrice:
    window: AdminPriceWindow

class AdminNotify:
    @staticmethod
    def buy(*, user_id: PossibleValue, username: PossibleValue) -> Literal["""{ $username } (user_id=&lt;code&gt;{ $user_id }&lt;/code&gt;) купил(а) доступ в бота!"""]: ...

class Admin:
    button: AdminButton
    menu: AdminMenu
    metrics: AdminMetrics
    mailing: AdminMailing
    price: AdminPrice
    notify: AdminNotify

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
    def text() -> Literal["""текст 3"""]: ...
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

class UserDelayed1:
    @staticmethod
    def text() -> Literal["""«А если я сделаю миник, а его никто не купит?»

Вот поэтому я и предлагаю сначала разобраться с темой.

Перед записью уроков нужно понять:

Кому это нужно?
В какой ситуации?
Что человек уже пробовал?
За какое решение он готов заплатить?

Потому что можно неделю выбирать шрифты для обложки, а потом выяснить, что вы вообще не можете объяснить, зачем покупать ваш продукт.

Обидно. Зато шрифт красивый 🫠

В «Мини-продукте с AI» начинаем с вашего опыта, аудитории и проверки темы. Потом переходим к материалам и оформлению.

Если именно на выборе темы вы сейчас застряли, посмотрите программу ещё раз 👇🏻"""]: ...
    @staticmethod
    def button() -> Literal["""Посмотреть программу"""]: ...

class UserDelayed2:
    @staticmethod
    def text() -> Literal["""Давайте хотя бы сдвинем вашу идею с места.

Откройте заметки и допишите:

«Я могу помочь [кому] решить [какую задачу], чтобы человек смог [что сделать]».

Без «раскрыть потенциал» и прочего тумана. Так, как объяснили бы знакомому.

Получилось? Уже есть идея, которую можно проверить.

Не получилось? Значит, сначала нужно разобраться с аудиторией и задачей. Это тоже полезно понять.

Если хотите пройти весь путь по урокам, забирайте «Мини-продукт с AI» за 2 990 ₽.

Будем выбирать тему, собирать материалы, упаковывать и готовить ваш продукт к продаже."""]: ...
    @staticmethod
    def button() -> Literal["""Хочу собрать свой миник"""]: ...

class UserMailing:
    @staticmethod
    def button() -> Literal["""Хочу собрать свой миник"""]: ...

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
    delayed1: UserDelayed1
    delayed2: UserDelayed2
    mailing: UserMailing
    spam: UserSpam
    invoice: UserInvoice

    @staticmethod
    def paid() -> Literal["""Похоже, у вас уже есть доступ! Просто перейдите в бота @mini_product_ai"""]: ...
    @staticmethod
    def buy() -> Literal["""Успешная оплата! Скорее начинай проходить уроки в @mini_product_ai"""]: ...
