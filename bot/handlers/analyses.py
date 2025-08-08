from aiogram import Router, F
from aiogram.types import Message
from bot.services.db_service import DatabaseService

analyses_router = Router()

@analyses_router.message(F.text == "Получить анализы")
async def get_analyses(message: Message, db: DatabaseService):
    patient_id = message.from_user.id
    analyses = await db.fetch_all(
        "SELECT analysis_type, result_file, analysis_date FROM medical_analyses WHERE patient_id = ?",
        (patient_id,)
    )
    if not analyses:
        await message.answer("У вас нет загруженных анализов.")
        return

    # Отправляем каждый анализ пользователю
    for analysis in analyses:
        analysis_type = analysis["analysis_type"]
        analysis_date = analysis["analysis_date"]
        result_file = analysis["result_file"]  # Предполагается, что это BLOB
        await message.answer_document(
            document=result_file,
            caption=f"Анализ: {analysis_type}\nДата: {analysis_date}"
        )