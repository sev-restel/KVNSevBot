from aiogram import Router, F
from aiogram.types import Message, FSInputFile, BufferedInputFile
from PIL import Image, ImageDraw, ImageFont
from data.database import DB_Users as db
from keyboard.reply import menu
import io

router = Router()

@router.message(F.text == "/ticket")
async def send_ticket(message: Message):
    # Получаем имя пользователя
    user_name = await db.select_name(message.from_user.id)
    
    photo = await edit_ticket(user_name)
    
    # Отправляем пользователю
    await message.answer_photo(photo=photo, caption=f"Вот ваш билет, {user_name}!")


@router.message(F.text == "🎟️Билет")
async def menu_d(message: Message):
    user_name = await db.select_name(message.from_user.id)
    photo = await edit_ticket(user_name)

    await message.answer_photo(photo=photo, caption=f"Вот ваш билет, {user_name}!")
    
    
@router.message(F.text == "📍Локация")
async def send_map(message: Message):
    img = Image.open("data/photo/map.png").convert("RGB")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)

    photo = BufferedInputFile(buffer.read(), filename="ticket.jpg")
    
    await message.answer_photo(photo=photo, caption=f"Вот инструкция как добраться к нам!",
                               reply_markup=menu)


async def edit_ticket(user_name):
    # Загружаем шаблон билета
    img = Image.open("data/photo/ticket.png").convert("RGB")

    # Подготавливаем рисование
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("utils/Archive.ttf", 80)  # Укажи путь к .ttf шрифту
    
    # Получаем размеры текста
    text_bbox = draw.textbbox((0, 0), user_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    # text_height = text_bbox[3] - text_bbox[1]

    image_width, image_height = img.size
    x = (image_width - text_width) // 2
    # y = (image_height - text_height) // 2
    
    # Позиция текста (можно подстроить) (1471, 398)
    text_position = (x, 1511)
    draw.text(text_position, user_name, font=font, fill=(0, 0, 0))

    # Сохраняем в буфер
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)

    # Создаем BufferedInputFile
    photo = BufferedInputFile(buffer.read(), filename="ticket.jpg")
    
    return photo