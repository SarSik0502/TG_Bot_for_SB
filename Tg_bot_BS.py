import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
import openpyxl

BOT_TOKEN = ""

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
storage = MemoryStorage()

# Определение состояний для FSM
class RegistrationStates(StatesGroup):
    fio = State()
    birth_date = State()
    phone_number = State()

# Функция для записи данных в Excel
def save_to_excel(fio, birth_date, phone_number):
    file_path = "spisok.xlsx"
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    sheet.append([fio, birth_date, phone_number])
    workbook.save("spisok.xlsx")

# Начало регистрации
@dp.message(F.text == "Регистрация")
async def start_registration(message: types.Message, state: FSMContext):
    await message.answer("Введите ваше ФИО:")
    await state.set_state(RegistrationStates.fio)

# Сохранение ФИО и запрос даты рождения
@dp.message(RegistrationStates.fio)
async def ask_birth_date(message: types.Message, state: FSMContext):
    await state.update_data(fio=message.text)  # Сохраняем ФИО
    await message.answer("Введите вашу дату рождения (в формате ДД.ММ.ГГГГ):")
    await state.set_state(RegistrationStates.birth_date)

# Сохранение даты рождения и запрос номера телефона
@dp.message(RegistrationStates.birth_date)
async def ask_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(birth_date=message.text)  # Сохраняем дату рождения
    await message.answer("Введите ваш номер телефона:")
    await state.set_state(RegistrationStates.phone_number)

# Сохранение номера телефона и завершение регистрации
@dp.message(RegistrationStates.phone_number)
async def finish_registration(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)  # Сохраняем номер телефона

    # Получаем все данные пользователя
    user_data = await state.get_data()
    fio = user_data.get("fio")
    birth_date = user_data.get("birth_date")
    phone_number = user_data.get("phone_number")

    save_to_excel(fio, birth_date, phone_number)

    # Выводим данные пользователю и завершаем состояние
    await message.answer(
        f"Спасибо за регистрацию! Вот ваши данные:\n"
        f"ФИО: {fio}\n"
        f"Дата рождения: {birth_date}\n"
        f"Номер телефона: {phone_number}"
    )
    await state.clear()  # Завершаем FSM

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(f"Здравствуйте, {message.from_user.first_name}! Добро пожаловать в наш бот!")
    await how_find(message)

# Обработчик кнопки "Пропустить"
@dp.message(F.text == "Пропустить")
async def skip(message: types.Message):
    await skidka(message)

# Предложения скидки
async def skidka(message: types.Message):
    list = [[KeyboardButton(text="Да")], [KeyboardButton(text="Нет")]]
    keyboard = ReplyKeyboardMarkup(keyboard=list, resize_keyboard=True)
    text = 'Спасибо, что выбрали "City Nails", Вам доступна скидка 20%.\nХотите ее использовать сейчас?'
    await message.answer(text, reply_markup=keyboard)

# Обработчик кнопки "Да"
@dp.message(F.text == "Да")
async def skip(message: types.Message, state: FSMContext):
    await start_registration(message, state)

# Обработчик кнопки "Нет"
@dp.message(F.text == "Нет")
async def skip(message: types.Message):
    await main_menu(message)

# Обработчик кнопки "Контакты"
@dp.message(F.text == "Контакты")
async def send_contact(message: types.Message):
    address = "🏠Адрес: Никольская ул., 25 • м. Лубянка, этаж 5\n\n"
    telephone = "📱+7 (499) 686-18-66 \n"
    inst = "📸Instagram: \nhttps://www.instagram.com/citynails_moscow?igsh=MWZkanpyeTVyMHVjeA==\n\n"
    timew = "🕛 Время работы:\n ПН-ВС: 10:00-22:00"
    text = address + telephone + inst + timew
    latitude = 55.759148
    longitude = 37.624625
    await message.answer(text)
    await message.answer_location(latitude, longitude)

# Обработчик кнопки "О разработчике"
@dp.message(F.text == "О разработчике")
async def send_developer_info(message: types.Message):
    text = "💻BSC - разработчик IT продуктов для вашего бизнеса\n📞 +7 (965) 340-17-02\n✉️bussupcom@yandex.ru"
    await message.answer(text)

# Обработчик кнопки "Оставить отзыв"
@dp.message(F.text == "Оставить отзыв")
async def feedback(message: types.Message):
    list = [[KeyboardButton(text="Yandex карты"), KeyboardButton(text="2ГИС карты"),
             KeyboardButton(text="Сообщение администрации")], [KeyboardButton(text="Вернуться назад")]]
    keyboard = ReplyKeyboardMarkup(keyboard=list, resize_keyboard=True)
    await message.answer(
        "Вы можете оставить отзыв на картах Yandex и 2ГИС.\n\nТакже вы можете написать напрямую администрации👮",
        reply_markup=keyboard
    )

# Обработчик кнопки "Наш салон"
@dp.message(F.text == "Наш салон")
async def feedback(message: types.Message):
    list = [[KeyboardButton(text="Какие услуги предоставляем"), KeyboardButton(text="Наши мастера")],
             [KeyboardButton(text="Вернуться назад")]]
    keyboard = ReplyKeyboardMarkup(keyboard=list, resize_keyboard=True)
    await message.answer("Что хотите узнать?", reply_markup=keyboard)

# Обработчик кнопки "Программа лояльности"
@dp.message(F.text == "Программа лояльности")
async def feedback(message: types.Message):
    list = [[KeyboardButton(text="Регистрация"), KeyboardButton(text="Система скидок")],
            [KeyboardButton(text="Накопленные бонусы"), KeyboardButton(text="Пригласить друга")],
             [KeyboardButton(text="Вернуться назад")]]
    keyboard = ReplyKeyboardMarkup(keyboard=list, resize_keyboard=True)
    await message.answer("Что хотите узнать?", reply_markup=keyboard)

# Обработчик кнопки "Фирменные идеи"
@dp.message(F.text == "Фирменные идеи")
async def feedback(message: types.Message):
    list = [[KeyboardButton(text="Маникюр"), KeyboardButton(text="Педикюр")],
             [KeyboardButton(text="Вернуться назад")]]
    keyboard = ReplyKeyboardMarkup(keyboard=list, resize_keyboard=True)
    await message.answer("Выберите услугу:", reply_markup=keyboard)

# Обработчик кнопки "Маникюр"
@dp.message(F.text == "Маникюр")
async def feedback(message: types.Message):
    list = [[KeyboardButton(text="Готовые идеи"), KeyboardButton(text="Конструктор")],
             [KeyboardButton(text="Вернуться назад")]]
    keyboard = ReplyKeyboardMarkup(keyboard=list, resize_keyboard=True)
    await message.answer("Выберите вариант:", reply_markup=keyboard)

# Обработчик кнопки "Педикюр"
@dp.message(F.text == "Педикюр")
async def feedback(message: types.Message):
    list = [[KeyboardButton(text="Готовые идеи"), KeyboardButton(text="Конструктор")],
             [KeyboardButton(text="Вернуться назад")]]
    keyboard = ReplyKeyboardMarkup(keyboard=list, resize_keyboard=True)
    await message.answer("Выберите вариант:", reply_markup=keyboard)

# Обработчик кнопки "Yandex карты"
@dp.message(F.text == "Yandex карты")
async def yandex(message: types.Message):
    linkY = "https://yandex.ru/maps/-/CDx3jMY-"
    await message.answer(linkY)

# Обработчик кнопки "2ГИС карты"
@dp.message(F.text == "2ГИС карты")
async def twoG(message: types.Message):
    linkG = "https://go.2gis.com/phrhv"
    await message.answer(linkG)

# Обработка кнопки "Оставить чаевые мастеру"
@dp.message(F.text == "Оставить чаевые мастеру")
async def tips(message):
    link = "https://netmonet.co/"
    await message.answer(link)

# Обработчик кнопки "Вернуться назад"
@dp.message(F.text == "Вернуться назад")
async def go_back(message: types.Message):
    await main_menu(message)

# Обработка кнопки "Прайс лист"
@dp.message(F.text == "Прайс лист")
async def price_list(message):
    image_path = "D:/Job/list.jfif"
    photo = FSInputFile(image_path)
    await bot.send_photo(message.chat.id, photo)

# Как нашли
async def how_find(message: types.Message):
    list = [[KeyboardButton(text="Instagram"), KeyboardButton(text="Яндекс карты"),
             KeyboardButton(text="ВКонтакте")], [KeyboardButton(text="Telegram-рассылка"),
             KeyboardButton(text="От друзей"), KeyboardButton(text="Увидел на улице")],
            [KeyboardButton(text="Пропустить")]]
    keyboard = ReplyKeyboardMarkup(keyboard=list, resize_keyboard=True)
    await message.answer("Как Вы узнали о нас?", reply_markup=keyboard)

# Главное меню
async def main_menu(message: types.Message):
    list = [[KeyboardButton(text="Записаться"), KeyboardButton(text="Контакты"),
             KeyboardButton(text="Оставить отзыв")], [KeyboardButton(text="Оставить чаевые мастеру"),
             KeyboardButton(text="Прайс лист")], [KeyboardButton(text="Фирменные идеи"),
             KeyboardButton(text="Наш салон")], [KeyboardButton(text="О разработчике"),
             KeyboardButton(text="Программа лояльности")]]
    keyboard = ReplyKeyboardMarkup(keyboard=list, resize_keyboard=True)
    await message.answer("Вы в главном меню, выберите действие:", reply_markup=keyboard)

# Обработчик неизвестных сообщений
@dp.message()
async def unknown_command(message: types.Message):
    await message.answer("Извините, я не понимаю эту команду. Попробуйте выбрать из меню.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
