admin-button-back = ⬅️ Назад
admin-button-skip = ➡️ Пропустить
admin-button-confirm = ✅ Подтвердить


admin-menu-text =
    <b>Добро пожаловать в админ-панель бота!</b>

    {$price ->
        [no] ⚠️ Не задана цена для продукта
        *[other] Цена для продукта: { $price } ₽
    }

admin-menu-button-metrics = 📊 Метрика
admin-menu-button-mailing = ✉️ Рассылка
admin-menu-button-price = 💵 Изменить Цену
admin-menu-button-leave = 🚪 Выйти


admin-metrics-general-text =
    <b>За все время:</b>

    👥 Пользователей: { $users } чел.
    🤑 Купили: { $paid } чел.
    🟢 Активных: { $alive } чел.
    🔴 Неактивных: { $dead } чел.

admin-metrics-general-button = 📆 За период
admin-metrics-sendleft-text = Введите левую границу периода (дата в формате ДД.ММ.ГГГГ).
admin-metrics-sendright-text = Введите правую границу периода (дата в формате ДД.ММ.ГГГГ).
admin-metrics-invalid-text = Правая граница периода не может быть больше левой!

admin-metrics-period-text =
    <b>С { $left } по { $right }:</b>

    👥 Запустили бота впервые: { $first_starts } чел.
    🤑 Купили: { $buys } чел.


admin-mailing-sendtext-text = Введите текст рассылки
admin-mailing-sendmedia-text = Отправьте фото|видео|кружок (не более 30 Мб)
admin-mailing-examle-text = Каждому пользователю без доступа в клуб будет отправлено следующее ⬇️
admin-mailing-confirm-text = <b><i>Подтвердить??</i></b>
admin-mailing-started-text =
    ✅ Рассылка всем пользователям без доступа в клуб началась. По мере ее обработки вам будут приходить уведомления.
    ⚙️ ID рассылки: { $mailing_id }

    ⬇️ Нажмите на кнопку ниже для возвращения в меню


admin-price-window-text = Задайте цену для товара, обязательно укажите копейки после точки! Формат: Р.КК

admin-notify-buy = {$username ->
        [no] ( username отсутствует )
        *[other] { $username }
    } (user_id=<code>{ $user_id }</code>) купил(а) доступ в бота!
