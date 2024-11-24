from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="/telegram",
    tags=["Telegram"]
)

# Настройки бота
TELEGRAM_BOT_USERNAME = "bigas_notification_bot"  # Замените на имя вашего бота
AUTH_URL = "https://cybergarden.leganyst.ru/auth/telegram"  # URL для обработки данных Telegram

@router.get("/widget", response_class=HTMLResponse)
async def get_telegram_widget():
    """
    Генерация HTML-кода Telegram Login Widget.
    """
    try:
        widget_html = f"""
        <script async src="https://telegram.org/js/telegram-widget.js?22"
                data-telegram-login="{TELEGRAM_BOT_USERNAME}"
                data-size="large"
                data-auth-url="{AUTH_URL}"
                data-request-access="write"></script>
        """
        return widget_html
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации виджета: {e}")