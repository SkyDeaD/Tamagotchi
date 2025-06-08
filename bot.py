import asyncio
import json
import os
import random
import re
import time
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Импортируем данные из отдельных файлов
from data.debates import DEBATES
from data.cities import CITIES
from data.pet_phrases import PET_PHRASES

# Инициализация бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Файлы для сохранения данных
DATA_FILE = "pets_data.json"
DEBATES_FILE = "debates.json"
CITIES_GAME_FILE = "cities_game_data.json"

# Загрузка данных из файла
def load_data():
    """Загружает данные питомцев из JSON файла"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

# Сохранение данных в файл
def save_data(data):
    """Сохраняет данные питомцев в JSON файл"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Загрузка данных игры в города
def load_cities_game_data():
    """Загружает данные игры в города из JSON файла"""
    if os.path.exists(CITIES_GAME_FILE):
        try:
            with open(CITIES_GAME_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

# Сохранение данных игры в города
def save_cities_game_data(data):
    """Сохраняет данные игры в города в JSON файл"""
    with open(CITIES_GAME_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Нормализация названия города
def normalize_city_name(city):
    """Нормализует название города (убирает лишние символы, приводит к нижнему регистру)"""
    normalized = re.sub(r'[^\w\s-]', '', city.strip().lower())
    normalized = normalized.replace('ё', 'е')
    return normalized

# Получение последней буквы для игры
def get_last_letter(city):
    """Получает последнюю букву города для игры (обрабатывает исключения)"""
    city = city.strip().lower().replace('ё', 'е')
    if not city:
        return None
    excluded_letters = {'ь', 'ъ', 'ы'}
    for i in range(len(city) - 1, -1, -1):
        letter = city[i]
        if letter.isalpha() and letter not in excluded_letters:
            return letter
    return None

# Получение первой буквы города
def get_first_letter(city):
    """Получает первую букву города"""
    city = city.strip().lower().replace('ё', 'е')
    if city and city[0].isalpha():
        return city[0]
    return None

# Проверка города в списке
def is_valid_city(city, cities_list):
    """Проверяет, есть ли город в списке"""
    normalized_input = normalize_city_name(city)
    for valid_city in cities_list:
        if normalize_city_name(valid_city) == normalized_input:
            return True, valid_city
    return False, None

# Поиск города на букву
def find_city_starting_with(letter, cities_list, used_cities):
    """Находит город, начинающийся на указанную букву"""
    available_cities = []
    for city in cities_list:
        if (get_first_letter(city) == letter and
                normalize_city_name(city) not in used_cities):
            available_cities.append(city)
    if available_cities:
        return random.choice(available_cities)
    return None

# Инициализация игры в города
def start_cities_game(user_id):
    """Начинает новую игру в города"""
    first_city = random.choice(CITIES)
    game_data = {
        str(user_id): {
            'active': True,
            'cities_used': [normalize_city_name(first_city)],
            'last_city': first_city,
            'last_letter': get_last_letter(first_city),
            'score': 0,
            'start_time': time.time()
        }
    }
    cities_game_data = load_cities_game_data()
    cities_game_data.update(game_data)
    save_cities_game_data(cities_game_data)
    return True, first_city

# Обработка хода игрока
def process_player_move(user_id, city):
    """Обрабатывает ход игрока в игре городов"""
    cities_game_data = load_cities_game_data()
    if str(user_id) not in cities_game_data or not cities_game_data[str(user_id)]['active']:
        return False, "Игра не активна!"
    game = cities_game_data[str(user_id)]
    is_valid, correct_city_name = is_valid_city(city, CITIES)
    if not is_valid:
        return False, f"Город '{city}' не найден в списке!"
    normalized_city = normalize_city_name(correct_city_name)
    if normalized_city in game['cities_used']:
        return False, f"Город '{correct_city_name}' уже был назван!"
    required_letter = game['last_letter']
    first_letter = get_first_letter(correct_city_name)
    if first_letter != required_letter:
        return False, f"Город должен начинаться на букву '{required_letter.upper()}'!"
    game['cities_used'].append(normalized_city)
    game['last_city'] = correct_city_name
    game['last_letter'] = get_last_letter(correct_city_name)
    game['score'] += 1
    bot_city = find_city_starting_with(game['last_letter'], CITIES, game['cities_used'])
    if bot_city:
        game['cities_used'].append(normalize_city_name(bot_city))
        game['last_city'] = bot_city
        game['last_letter'] = get_last_letter(bot_city)
        save_cities_game_data(cities_game_data)
        return True, {
            'player_city': correct_city_name,
            'bot_city': bot_city,
            'next_letter': game['last_letter'],
            'score': game['score']
        }
    else:
        game_time = time.time() - game['start_time']
        final_score = game['score']
        game['active'] = False
        save_cities_game_data(cities_game_data)
        return True, {
            'player_city': correct_city_name,
            'game_won': True,
            'final_score': final_score,
            'game_time': game_time
        }

# Завершение игры
def end_cities_game(user_id):
    """Завершает игру в города"""
    cities_game_data = load_cities_game_data()
    if str(user_id) not in cities_game_data:
        return False, 0, 0
    game = cities_game_data[str(user_id)]
    if not game['active']:
        return False, 0, 0
    game_time = time.time() - game['start_time']
    final_score = game['score']
    game['active'] = False
    save_cities_game_data(cities_game_data)
    return True, final_score, game_time

# Проверка активной игры
def is_cities_game_active(user_id):
    """Проверяет, активна ли игра в города у пользователя"""
    cities_game_data = load_cities_game_data()
    return (str(user_id) in cities_game_data and
            cities_game_data[str(user_id)].get('active', False))

# Глобальные переменные для хранения данных
pets_data = load_data()

# Создание обычной клавиатуры
def get_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Статус"), KeyboardButton(text="🗣️ Поговорить")],
            [KeyboardButton(text="🏙️ Играть в города"), KeyboardButton(text="🤔 Филосовские вопросы")],
            [KeyboardButton(text="🔄 Новый питомец")]
        ],
        resize_keyboard=True
    )
    return keyboard

# Клавиатура для игры в города
def get_cities_game_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚪 Закончить игру")]
        ],
        resize_keyboard=True
    )
    return keyboard

# Создание инлайн клавиатуры для выбора типа питомца
def get_pet_type_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🐱 Котик", callback_data="type_cat")],
            [InlineKeyboardButton(text="🐶 Собачка", callback_data="type_dog")],
            [InlineKeyboardButton(text="🦜 Попуг", callback_data="type_parrot")]
        ]
    )
    return keyboard

# Создание инлайн клавиатуры для действий с питомцем
def get_actions_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🍖 Покормить", callback_data="action_feed")],
            [InlineKeyboardButton(text="🎮 Поиграть", callback_data="action_play")],
            [InlineKeyboardButton(text="💤 Спать", callback_data="action_sleep")]
        ]
    )
    return keyboard

# Обновление характеристик питомца по времени
def update_pet_stats(user_id):
    """Обновляет характеристики питомца в зависимости от прошедшего времени"""
    if str(user_id) not in pets_data:
        return
    pet = pets_data[str(user_id)]
    now = datetime.now()
    last_update = datetime.fromisoformat(pet['last_update'])
    hours_passed = (now - last_update).total_seconds() / 3600
    decrease = int(hours_passed * 2)
    if decrease > 0:
        pet['hunger'] = max(0, pet['hunger'] - decrease)
        pet['mood'] = max(0, pet['mood'] - decrease)
        pet['energy'] = max(0, pet['energy'] - decrease)
        pet['last_update'] = now.isoformat()
        save_data(pets_data)

# Создание нового питомца
def create_pet(user_id, name, pet_type):
    """Создает нового питомца для пользователя"""
    pets_data[str(user_id)] = {
        'name': name,
        'type': pet_type,
        'hunger': 100,
        'mood': 100,
        'energy': 100,
        'last_update': datetime.now().isoformat()
    }
    save_data(pets_data)

# Получение статуса питомца
def get_pet_status(user_id):
    """Возвращает строку со статусом питомца"""
    if str(user_id) not in pets_data:
        return None
    update_pet_stats(user_id)
    pet = pets_data[str(user_id)]
    emoji_map = {'cat': '🐱', 'dog': '🐶', 'parrot': '🦜'}
    pet_emoji = emoji_map.get(pet['type'], '🐱')
    def make_bar(value):
        filled = '█' * (value // 10)
        empty = '░' * (10 - value // 10)
        return f"[{filled}{empty}] {value}%"
    status = f"{pet_emoji} {pet['name']}\n\n"
    status += f"🍖 Голод: {make_bar(pet['hunger'])}\n"
    status += f"😊 Настроение: {make_bar(pet['mood'])}\n"
    status += f"⚡ Энергия: {make_bar(pet['energy'])}\n\n"
    if pet['hunger'] < 20:
        status += "😫 Я очень голоден!"
    elif pet['mood'] < 20:
        status += "😢 Мне грустно..."
    elif pet['energy'] < 20:
        status += "😴 Я очень устал..."
    elif pet['hunger'] > 80 and pet['mood'] > 80 and pet['energy'] > 80:
        if pet['type'] == 'cat':
            status += "😻 Мяу! Я счастлив!"
        elif pet['type'] == 'dog':
            status += "🐕 Гав! Я очень рад!"
        else:
            status += "🦜 Чирик! Я очень счастлив!"
    else:
        status += "😊 Все хорошо!"
    return status

# Получение случайной фразы питомца
def get_random_phrase(pet_type, action="talk"):
    """Возвращает случайную фразу для типа питомца и действия"""
    if pet_type in PET_PHRASES and action in PET_PHRASES[pet_type]:
        phrases_list = PET_PHRASES[pet_type][action]
        if phrases_list:
            return random.choice(phrases_list)

# Получение случайного вопроса для "филосовских вопросов"
def get_random_debate():
    """Возвращает случайный вопрос для 'филосовских вопросов'"""
    return random.choice(DEBATES)

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    user_id = message.from_user.id
    if str(user_id) in pets_data:
        await message.answer("У вас уже есть питомец!", reply_markup=get_keyboard())
        return
    await message.answer(
        "🎉 Добро пожаловать в мир Тамагочи!\n\n"
        "Выберите тип питомца:",
        reply_markup=get_pet_type_keyboard()
    )

# Обработчик выбора типа питомца
@dp.callback_query(F.data.startswith("type_"))
async def choose_pet_type(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if str(user_id) in pets_data:
        await callback.answer("У вас уже есть питомец!")
        return
    pet_type = callback.data.split("_")[1]
    type_names = {"cat": "котика", "dog": "собачку", "parrot": "попуга"}
    await callback.message.edit_text(
        f"Отлично! Вы выбрали {type_names[pet_type]} 🎉\n\n"
        f"Теперь введите имя для питомца:"
    )
    pets_data[f"temp_{user_id}"] = pet_type
    save_data(pets_data)

# Обработчик действий с питомцем
@dp.callback_query(F.data.startswith("action_"))
async def pet_action(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    action = callback.data.split("_")[1]
    if str(user_id) not in pets_data:
        await callback.answer("У вас нет питомца!")
        return
    update_pet_stats(user_id)
    pet = pets_data[str(user_id)]
    emoji_map = {'cat': '🐱', 'dog': '🐶', 'parrot': '🦜'}
    pet_emoji = emoji_map.get(pet['type'], '🐱')
    if action == "feed":
        pet['hunger'] = min(100, pet['hunger'] + 30)
        pet['mood'] = min(100, pet['mood'] + 10)
        phrase = get_random_phrase(pet['type'], 'feed')
        response = f"{pet_emoji} {pet['name']}: {phrase}"
    elif action == "play":
        if pet['energy'] < 15:
            response = f"{pet_emoji} {pet['name']}: Я слишком устал для игр... 😴"
        else:
            pet['mood'] = min(100, pet['mood'] + 25)
            pet['energy'] = max(0, pet['energy'] - 15)
            pet['hunger'] = max(0, pet['hunger'] - 10)
            phrase = get_random_phrase(pet['type'], 'play')
            response = f"{pet_emoji} {pet['name']}: {phrase}"
    elif action == "sleep":
        pet['energy'] = min(100, pet['energy'] + 40)
        pet['mood'] = min(100, pet['mood'] + 5)
        pet['hunger'] = max(0, pet['hunger'] - 10)
        phrase = get_random_phrase(pet['type'], 'sleep')
        response = f"{pet_emoji} {pet['name']}: {phrase}"
    pet['last_update'] = datetime.now().isoformat()
    save_data(pets_data)
    await callback.answer()
    await callback.message.answer(response)

# Обработчик кнопки "Поговорить с питомцем"
@dp.message(F.text == "🗣️ Поговорить")
async def talk_to_pet(message: types.Message):
    user_id = message.from_user.id
    if str(user_id) not in pets_data:
        await message.answer("У вас нет питомца! Используйте /start")
        return
    update_pet_stats(user_id)
    pet = pets_data[str(user_id)]
    emoji_map = {'cat': '🐱', 'dog': '🐶', 'parrot': '🦜'}
    pet_emoji = emoji_map.get(pet['type'], '🐱')
    if pet['energy'] < 10:
        response = f"{pet_emoji} {pet['name']}: Я слишком устал для разговоров... 😴"
        await message.answer(response)
        return
    if pet['hunger'] < 10:
        response = f"{pet_emoji} {pet['name']}: Я голоден! 😖"
        await message.answer(response)
        return
    pet['energy'] = max(0, pet['energy'] - 3)
    pet['mood'] = min(100, pet['mood'] + 5)
    pet['hunger'] = max(0, pet['hunger'] - 5)
    phrase = get_random_phrase(pet['type'], 'talk')
    emoji_map = {'cat': '🐱', 'dog': '🐶', 'parrot': '🦜'}
    pet_emoji = emoji_map.get(pet['type'], '🐱')
    pet['last_update'] = datetime.now().isoformat()
    save_data(pets_data)
    await message.answer(f"{pet_emoji} {pet['name']}: {phrase}")

# Обработчик кнопки "Филосовские вопросы"
@dp.message(F.text == "🤔 Филосовские вопросы")
async def absurd_debates(message: types.Message):
    user_id = message.from_user.id
    if str(user_id) not in pets_data:
        await message.answer("У вас нет питомца! Используйте /start")
        return
    update_pet_stats(user_id)
    pet = pets_data[str(user_id)]
    emoji_map = {'cat': '🐱', 'dog': '🐶', 'parrot': '🦜'}
    pet_emoji = emoji_map.get(pet['type'], '🐱')
    if pet['energy'] < 10:
        response = f"{pet_emoji} {pet['name']}: Я слишком устал для разговоров... 😴"
        await message.answer(response)
        return
    if pet['hunger'] < 10:
        response = f"{pet_emoji} {pet['name']}: Я голоден! 😖"
        await message.answer(response)
        return
    pet['energy'] = max(0, pet['energy'] - 8)
    pet['mood'] = min(100, pet['mood'] + 12)
    pet['hunger'] = max(0, pet['hunger'] - 10)
    debate_question = get_random_debate()
    pet['last_update'] = datetime.now().isoformat()
    save_data(pets_data)
    await message.answer(
        f"{pet_emoji} {pet['name']} предлагает обсудить:\n\n"
        f"🤔 {debate_question}\n\n"
    )

# Обработчик кнопки "Играть в города"
@dp.message(F.text == "🏙️ Играть в города")
async def start_cities_game_handler(message: types.Message):
    user_id = message.from_user.id
    if str(user_id) not in pets_data:
        await message.answer("У вас нет питомца! Используйте /start")
        return
    pet = pets_data[str(user_id)]
    emoji_map = {'cat': '🐱', 'dog': '🐶', 'parrot': '🦜'}
    pet_emoji = emoji_map.get(pet['type'], '🐱')
    if pet['energy'] < 10:
        response = f"{pet_emoji} {pet['name']}: Я слишком устал для игр... 😴"
        await message.answer(response)
        return
    if pet['hunger'] < 10:
        response = f"{pet_emoji} {pet['name']}: Я голоден! 😖"
        await message.answer(response)
        return
    if is_cities_game_active(user_id):
        await message.answer(
            "У вас уже есть активная игра в города! 🏙️\n"
            "Завершите текущую игру или назовите город.",
            reply_markup=get_cities_game_keyboard()
        )
        return
    success, result = start_cities_game(user_id)
    if not success:
        await message.answer(f"Ошибка при запуске игры: {result}")
        return
    await message.answer(
        f"🏙️ **Игра в города началась!**\n\n"
        f"🤖 Я начинаю: **{result}**\n\n"
        f"🎯 Ваш ход! Назовите город на букву **'{get_last_letter(result).upper()}'**\n\n"
        f"📋 **Правила:**\n"
        f"• Города не должны повторяться\n"
        f"• Если город заканчивается на Ь, Ъ, Ы - берём предыдущую букву\n"
        f"• Е и Ё считаются одной буквой\n\n"
        f"Удачи! 🍀",
        reply_markup=get_cities_game_keyboard(),
        parse_mode="Markdown"
    )

# Обработчик завершения игры в города
@dp.message(F.text == "🚪 Закончить игру")
async def end_cities_game_handler(message: types.Message):
    user_id = message.from_user.id
    if not is_cities_game_active(user_id):
        await message.answer(
            "У вас нет активной игры в города! 🤷‍♂️",
            reply_markup=get_keyboard()
        )
        return
    success, score, game_time = end_cities_game(user_id)
    if success:
        minutes = int(game_time // 60)
        seconds = int(game_time % 60)
        await message.answer(
            f"🏁 **Игра завершена!**\n\n"
            f"📊 **Статистика:**\n"
            f"🏆 Правильных ответов: **{score}**\n"
            f"⏱ Время игры: **{minutes}м {seconds}с**\n\n"
            f"Спасибо за игру! 😊",
            reply_markup=get_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            "Произошла ошибка при завершении игры.",
            reply_markup=get_keyboard()
        )

# Обработчик кнопки "Статус"
@dp.message(F.text == "📊 Статус")
async def show_status(message: types.Message):
    user_id = message.from_user.id
    if str(user_id) not in pets_data:
        await message.answer("У вас нет питомца! Используйте /start")
        return
    status = get_pet_status(user_id)
    await message.answer(status, reply_markup=get_actions_keyboard())

# Обработчик кнопки "Новый питомец"
@dp.message(F.text == "🔄 Новый питомец")
async def new_pet(message: types.Message):
    user_id = message.from_user.id
    if str(user_id) in pets_data:
        del pets_data[str(user_id)]
        save_data(pets_data)
    await message.answer(
        "Создадим нового питомца! 🎉\n\n"
        "Выберите тип питомца:",
        reply_markup=get_pet_type_keyboard()
    )

# Обработчик ввода текста
@dp.message(F.text)
async def handle_text_messages(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    if is_cities_game_active(user_id):
        success, result = process_player_move(user_id, text)
        if not success:
            await message.answer(
                f"❌ {result}\n\nПопробуйте еще раз!",
                reply_markup=get_cities_game_keyboard()
            )
            return
        if isinstance(result, dict):
            if result.get('game_won'):
                minutes = int(result['game_time'] // 60)
                seconds = int(result['game_time'] % 60)
                await message.answer(
                    f"🎉 **Поздравляю! Вы победили!**\n\n"
                    f"✅ Ваш город: **{result['player_city']}**\n"
                    f"🤖 Я не смог найти город на эту букву!\n\n"
                    f"📊 **Итоговая статистика:**\n"
                    f"🏆 Правильных ответов: **{result['final_score']}**\n"
                    f"⏱ Время игры: **{minutes}м {seconds}с**\n\n"
                    f"Отличная игра! 🥳",
                    reply_markup=get_keyboard(),
                    parse_mode="Markdown"
                )
            else:
                await message.answer(
                    f"✅ **{result['player_city']}** - принято!\n\n"
                    f"🤖 Мой ход: **{result['bot_city']}**\n\n"
                    f"🎯 Ваш ход! Назовите город на букву **'{result['next_letter'].upper()}'**\n\n"
                    f"📊 Правильных ответов: **{result['score']}**",
                    reply_markup=get_cities_game_keyboard(),
                    parse_mode="Markdown"
                )
        return
    temp_key = f"temp_{user_id}"
    if temp_key in pets_data:
        pet_type = pets_data[temp_key]
        del pets_data[temp_key]
        if len(text) > 15:
            await message.answer("Имя слишком длинное! Максимум 15 символов.")
            return
        if not text.strip():
            await message.answer("Введите нормальное имя!")
            return
        create_pet(user_id, text.strip(), pet_type)
        type_names = {"cat": "котик", "dog": "собачка", "parrot": "попуг"}
        emoji_map = {"cat": "🐱", "dog": "🐶", "parrot": "🦜"}
        await message.answer(
            f"🎉 Поздравляю! Ваш {type_names[pet_type]} {emoji_map[pet_type]} {text} создан!\n\n"
            f"Все показатели: 100% ✨\n\n"
            f"💡 Совет: Разные действия по-разному влияют на статы:\n"
            f"🍖 Кормление - восстанавливает голод\n"
            f"🎮 Игра - поднимает настроение, но тратит энергию\n"
            f"💤 Сон - восстанавливает энергию\n"
            f"🗣️ Общение и 'фиолосовские вопросы' тоже влияют на питомца!",
            reply_markup=get_keyboard()
        )
    else:
        await message.answer("Не понимаю 🤔\nИспользуйте кнопки или создайте питомца командой /start")

# Запуск бота
async def main():
    print("🚀 Бот запущен!")
    print(f"📁 Данные сохраняются в: {DATA_FILE}")
    print(f"🎮 Данные игры в города сохраняются в: {CITIES_GAME_FILE}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())