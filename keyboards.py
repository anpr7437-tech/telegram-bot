"""Клавиатуры бота."""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_keyboard(channel_url: str = "") -> InlineKeyboardMarkup:
    """Клавиатура после /start: Подписаться, Проверить подписку."""
    builder = InlineKeyboardBuilder()
    if channel_url:
        builder.row(
            InlineKeyboardButton(text="Подписаться", url=channel_url)
        )
    builder.row(
        InlineKeyboardButton(text="Проверить подписку", callback_data="check_subscription")
    )
    return builder.as_markup()


def admin_main_keyboard() -> InlineKeyboardMarkup:
    """Главное меню админки."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
        InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast")
    )
    builder.row(
        InlineKeyboardButton(text="📢 Каналы подписки", callback_data="admin_channels"),
        InlineKeyboardButton(text="🔄 Обновить", callback_data="admin_refresh")
    )
    return builder.as_markup()


def admin_stats_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔄 Обновить статистику", callback_data="admin_stats_refresh")
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Назад", callback_data="admin_back")
    )
    return builder.as_markup()


def admin_back_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="◀️ Назад", callback_data="admin_back"))
    return builder.as_markup()


def admin_channels_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="➕ Добавить канал", callback_data="admin_channel_add"),
        InlineKeyboardButton(text="Вкл/Выкл проверку", callback_data="admin_channel_toggle")
    )
    builder.row(InlineKeyboardButton(text="◀️ Назад", callback_data="admin_back"))
    return builder.as_markup()


def broadcast_confirm_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Отправить", callback_data="broadcast_confirm"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="admin_back")
    )
    return builder.as_markup()
