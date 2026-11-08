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
admin-menu-button-user = 👥 Найти
admin-menu-button-price = 💵 Цена
admin-menu-button-leave = 🚪 Выйти


admin-metrics-general-text =
    <b>За все время:</b>

    👥 Пользователей: { $users } чел.
    🤑 Купили: { $paid } чел.
    🟢 Активных: { $active } чел.
    🔴 Неактивных: { $dead } чел.

admin-metrics-general-button = 📆 За период
admin-metrics-sendleft-text = Введите левую границу периода (дата в формате ДД.ММ.ГГГГ).
admin-metrics-sendright-text = Введите правую границу периода (дата в формате ДД.ММ.ГГГГ).
admin-metrics-invalid-text = Правая граница периода не может быть больше левой!

admin-metrics-period-text =
    <b>С { $left } по { $right }:</b>

    👥 Запустили бота впервые: { $first_starts } чел.
    🤑 Купили: { $buys } чел.
