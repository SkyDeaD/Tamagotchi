import asyncio # Асинхронность, для aiogram
import json # "Словари" для сохранения данных в случае перезапуска бота
import os # Для переменных окружения, чтобы не светить токеном бота в коде
import random # Для рандома значений

from datetime import datetime # Для получения текущего времени пользователя

# Все необходимые импорты для aiogram
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Инициализация бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Файлы для сохранения данных
DATA_FILE = "pets_data.json"
PHRASES_FILE = "pet_phrases.json"
DEBATES_FILE = "debates.json"


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


# Загрузка дебатов
def load_debates():
    """Загружает вопросы для дебатов из JSON файла"""
    if os.path.exists(DEBATES_FILE):
        try:
            with open(DEBATES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return create_default_debates()
    else:
        return create_default_debates()


# Создание файла с дебатами по умолчанию
def create_default_debates():
    """Создает файл с дебатами по умолчанию"""
    default_debates = {
        "debates": [
           "Что лучше: горячий лед или холодный огонь?",
            "Пельмени — это суп?",
            "Если дерево упало в лесу, но никто не слышал, издало ли оно звук в параллельной вселенной?",
            "Почему круглая пицца в квадратной коробке режется треугольными кусочками?",
            "Можно ли быть одновременно голодным и сытым?",
            "Что было раньше: курица или яичница?",
            "Если время — деньги, то можно ли купить вчерашний день?",
            "Почему мы говорим 'после дождичка в четверг', если дождь может быть в любой день?",
            "Существует ли цвет, который мы не можем увидеть, но можем попробовать на вкус?",
            "Если бесконечность умножить на ноль, получится ли очень маленькая бесконечность?",
            "Может ли робот мечтать об электрических овцах, если он вегетарианец?",
            "Что происходит с носками, которые исчезают в стиральной машине?",
            "Если Пиноккио скажет 'Мой нос сейчас вырастет', что произойдет?",
            "Почему мы называем это 'быстрая еда', если готовим её медленно?",
            "Можно ли быть уникальным, как все остальные?",
            "Если вампир укусит зомби, кто кем станет?",
            "Почему алфавит расположен именно в таком порядке?",
            "Что тяжелее: килограмм железа или килограмм перьев на Луне?",
            "Если мыло упало на пол, то пол стал чище или мыло грязнее?",
            "Можно ли плакать под водой?",
            "Почему 'сокращение' — такое длинное слово?",
            "Если ничего не прилипает к тефлону, как тефлон прилипает к сковороде?",
            "Что будет, если неудержимая сила встретится с неподвижным объектом?",
            "Почему мы жмём сильнее на пульт, когда батарейки садятся?",
            "Можно ли быть частично беременной философией?",
            "Если бы у рыб были ноги, ходили бы они или продолжали плавать по воздуху?",
            "Почему круглые канализационные люки, а не квадратные?",
            "Что громче: тишина или звук одной хлопающей руки?",
            "Если время лечит, то что лечит время?",
            "Можно ли сидеть на стуле, который находится в твоих мыслях?",
            "Почему мы говорим 'спать как убитый', если мёртвые не спят?",
            "Что было бы, если бы гравитация работала только по выходным?",
            "Можно ли потерять то, что никогда не находил?",
            "Если все уникальны, то никто не уникален?",
            "Почему мы называем это 'здравый смысл', если он встречается так редко?",
            "Что произойдёт, если встретятся два телепата и будут читать мысли друг друга?",
            "Можно ли быть одновременно внутри и снаружи коробки?",
            "Если бы цвета имели вкус, какой вкус у прозрачности?",
            "Почему мы говорим 'включить свет', если мы на самом деле включаем лампочку?",
            "Что более бесконечно: большая бесконечность или маленькая?",
            "Можно ли забыть, как забывать?",
            "Если дождь идёт вверх, то это всё ещё дождь?",
            "Почему мы называем это 'восход солнца', если солнце не движется?",
            "Что было бы, если бы числа были живыми существами?",
            "Можно ли быть левшой правой рукой?",
            "Если бы у времени были часы, который час показывали бы часы времени?",
            "Почему мы говорим 'убить время', если время бессмертно?",
            "Что происходит с идеями, которые никто не думает?",
            "Можно ли наступить в одну и ту же лужу дважды?",
            "Если бы у воздуха был вкус, чем бы он пах?",
            "Почему мы говорим 'сломать лёд', если лёд и так твёрдый?",
            "Что тише: беззвучный звук или звучащая тишина?",
            "Можно ли мечтать о том, что не умеешь воображать?",
            "Если бы у букв были чувства, какая буква была бы самой грустной?",
            "Почему мы говорим 'потерять голову', если голова на месте?",
            "Что быстрее: скорость света или скорость темноты?",
            "Можно ли быть наполовину пустым и наполовину полным одновременно?",
            "Если бы у планет были эмоции, что чувствовала бы Земля?",
            "Почему мы говорим 'мёртвая тишина', если тишина не живая?",
            "Что произойдёт, если параллельные прямые пересекутся?",
            "Можно ли думать о ничём, думая о том, что думаешь о ничём?",
            "Если бы у снов был вес, сколько весил бы кошмар?",
            "Почему мы говорим 'живая очередь', если очередь не дышит?",
            "Что более круглое: квадратный круг или круглый квадрат?",
            "Можно ли слышать цвета в полной темноте?",
            "Если бы у слов был возраст, какое слово было бы самым старым?",
            "Почему мы говорим 'горячая новость', если новости не имеют температуры?",
            "Что произойдёт, если встретятся прошлое и будущее?",
            "Можно ли быть невидимым для самого себя?",
            "Если бы у математики были чувства, что бы она думала о делении на ноль?",
            "Почему мы говорим 'золотая середина', если золото жёлтое?",
            "Что более странно: нормальная странность или странная нормальность?",
            "Можно ли потрогать отражение отражения?",
            "Если бы у дней недели были характеры, кто был бы самым вредным?",
            "Почему мы говорим 'железная логика', если железо не думает?",
            "Что произойдёт, если зеркало посмотрит на себя?",
            "Можно ли быть одновременно здесь и нигде?",
            "Если бы у эмоций был цвет, какого цвета была бы грусть радости?",
            "Почему мы говорим 'холодный расчёт', если математика не мёрзнет?",
            "Что более реально: реальная иллюзия или иллюзорная реальность?",
            "Можно ли услышать тишину, если она очень громкая?",
            "Если бы у пустоты был объём, сколько места она занимала бы?",
            "Почему мы говорим 'слепое пятно', если пятна не видят?",
            "Что произойдёт, если завтра наступит вчера?",
            "Можно ли быть частично отсутствующим?",
            "Если бы у мыслей была скорость, с какой скоростью летали бы глупые мысли?",
            "Почему мы говорим 'живое общение', если общение не дышит?",
            "Что более прозрачно: невидимая прозрачность или прозрачная невидимость?",
            "Можно ли забыть то, что ещё не запомнил?",
            "Если бы у секунд были секунды, сколько времени длилась бы минута?",
            "Почему мы говорим 'мёртвая точка', если точки не умирают?",
            "Что произойдёт, если бесконечность закончится?",
            "Можно ли быть везде и нигде одновременно?",
            "Если бы у вопросов были ответы на другие вопросы, какой вопрос ответил бы на себя?",
            "Почему мы говорим 'чёрная дыра', если она не дыра?",
            "Что более настоящее: прошлое будущее или будущее прошлое?",
            "Можно ли увидеть то, что невозможно не увидеть?",
            "Если бы у противоположностей были противоположности, что было бы противоположностью противоположности?",
            "Почему мы говорим 'белая ночь', если ночь тёмная?",
            "Что произойдёт, если встретятся все возможности?",
            "Можно ли не быть тем, кто ты есть, оставаясь собой?",
            "Если бы у парадоксов была логика, была бы она парадоксальной?",
            "Почему мы говорим 'глухая стена', если стены не слышат?",
            "Что более бесконечно: бесконечность в квадрате или квадратная бесконечность?",
            "Можно ли найти то, что никогда не терял, в том месте, где никогда не искал?",
            "Если бы время шло назад, мы бы молодели или старели в обратную сторону?",
            "Почему кошки мурлыкают именно так, а не по-другому?",
            "Что было бы, если бы гравитация действовала только на живых существ?"
          ]
        }

    with open(DEBATES_FILE, 'w', encoding='utf-8') as f:
        json.dump(default_debates, f, ensure_ascii=False, indent=2)

    return default_debates


# Загрузка фраз питомцев
def load_phrases():
    """Загружает фразы питомцев из JSON файла"""
    if os.path.exists(PHRASES_FILE):
        try:
            with open(PHRASES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return create_default_phrases()
    else:
        return create_default_phrases()


# Создание файла с фразами по умолчанию
def create_default_phrases():
    """Создает файл с фразами по умолчанию"""
    default_phrases = {
        "cat": {
            "talk": [
                "Мяу! 🐱",
                "Мурр-мурр! 😸",
                "Хочу рыбку! 🐟",
                "Погладь меня! ✋",
                "Мне скучно... 😾",
                "Где моя игрушка? 🧶",
                "Мяф-мяф! 😽",
                "Я хочу спать на твоей клавиатуре! ⌨️",
                "Дай мне валерьянки! 🌿",
                "Мурлыкаю только для тебя! 💕"
            ],
            "feed": [
                "Мяу! Наконец-то поел! 😋",
                "Мурр... это было вкусно! 😸",
                "Спасибо за еду, хозяин! 🐱",
                "Можно ещё рыбки? 🐟",
                "Теперь хочется поспать... 😴",
                "Мяу-мяу! Я сыт и доволен! 😊",
                "Ням-ням! Лучшая еда в мире! 🍽️",
                "Теперь у меня есть силы ловить мышей! 🐭"
            ],
            "play": [
                "Мяу! Давай ещё поиграем! 🎾",
                "Это было весело! 😸",
                "Я поймал невидимую мышку! 🐭",
                "Мурр... люблю играть! 🧶",
                "Где моя любимая игрушка? 🎀",
                "Мяу! Я самый ловкий кот! 💪",
                "Поиграем в прятки? 👀",
                "Я великий охотник! 🏹"
            ],
            "sleep": [
                "Мурр... хорошо поспал! 😴",
                "Мне снились рыбки... 🐟",
                "Сон — это лучшее время дня! 💤",
                "Мяу... я выспался! 😊",
                "Во сне я был тигром! 🐅",
                "Теперь полон энергии! ⚡",
                "Я спал 16 часов, это норма! 😸",
                "Сладкие сны о молочке! 🥛"
            ]
        },
        "dog": {
            "talk": [
                "Гав-гав! 🐶",
                "Хочу гулять! 🦴",
                "Ты мой лучший друг! ❤️",
                "Давай играть! 🎾",
                "Дай косточку! 🦴",
                "Я хороший мальчик! 😊",
                "Вуф-вуф! 🐕",
                "Хозяин вернулся! Лучший день! 🎉",
                "Можно погрызть тапок? 👟",
                "Я буду охранять тебя! 🛡️"
            ],
            "feed": [
                "Гав! Как вкусно! 😋",
                "Спасибо за еду! Я самый счастливый пёс! 🐕",
                "Ам-ам-ам! Обожаю покушать! 🍖",
                "Можно ещё косточку? 🦴",
                "Гав-гав! Теперь я сильный! 💪",
                "Это была лучшая еда в моей жизни! ❤️",
                "Хрум-хрум! Вкуснятина! 😋",
                "Теперь готов к долгой прогулке! 🚶"
            ],
            "play": [
                "Гав! Это было супер! 🎾",
                "Я поймал мячик! Я молодец! 🏀",
                "Давай ещё побегаем! 🏃",
                "Ты лучший друг для игр! ❤️",
                "Гав-гав! Обожаю играть! 😄",
                "Я самый быстрый пёс в мире! 🚀",
                "Апорт! Ещё раз! 🎾",
                "Поиграем в догонялки? 🏃‍♂️"
            ],
            "sleep": [
                "Гав... хорошо поспал! 😴",
                "Мне снилось, что я гонял котов! 🐱",
                "Сон восстановил мои силы! 💪",
                "Теперь готов к новым приключениям! 🌟",
                "Гав! Я полон энергии! ⚡",
                "Во сне я был волком! 🐺",
                "Сплю только одним глазом - охраняю! 👁️",
                "Самые сладкие сны о косточках! 🦴"
            ]
        },
        "dragon": {
            "talk": [
                "Рррр! 🐲",
                "Я могучий дракон! 💪",
                "Где мои сокровища? 💎",
                "Хочу полетать! ✈️",
                "Боишься меня? 😈",
                "Я защищу тебя! 🛡️",
                "Грр-грр! Слышишь мой рык? 👹",
                "Мой огонь согреет тебя! 🔥",
                "Принеси мне золото! 💰",
                "Я древний и мудрый! 🧙‍♂️"
            ],
            "feed": [
                "Рррр! Огненная еда! 🔥",
                "Вкусно! Теперь мой огонь сильнее! 🐲",
                "Спасибо, смертный! Ты накормил дракона! 👑",
                "Эта еда достойна короля драконов! 💎",
                "Моё пламя разгорается от сытости! 🔥",
                "Рррр! Я готов к полёту! ✈️",
                "Хрум! Как жареное мясо! 🍖",
                "Моя сила удваивается! ⚡"
            ],
            "play": [
                "Рррр! Отличная тренировка! ⚔️",
                "Я показал свою мощь! 💪",
                "Это было как настоящий бой! 🗡️",
                "Мои крылья стали сильнее! 🦅",
                "Рррр! Я непобедимый дракон! 👑",
                "Спасибо за тренировку, воин! 🛡️",
                "Попробуй догнать меня в полёте! 🌪️",
                "Я дышу огнём от радости! 🔥"
            ],
            "sleep": [
                "Рррр... сон дракона священен! 💤",
                "Мне снились золотые горы! 💰",
                "Во сне я летал над облаками! ☁️",
                "Мой огонь восстановился! 🔥",
                "Теперь я готов к великим свершениям! ⚡",
                "Сон сделал меня мудрее! 🧠",
                "Драконы спят на золоте! 💎",
                "Восстановил свою магическую силу! 🪄"
            ]
        }
    }

    with open(PHRASES_FILE, 'w', encoding='utf-8') as f:
        json.dump(default_phrases, f, ensure_ascii=False, indent=2)

    return default_phrases


# Глобальные переменные для хранения данных
pets_data = load_data()
pet_phrases = load_phrases()
debates_data = load_debates()


# Создание обычной клавиатуры (под строкой ввода)
def get_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Статус"), KeyboardButton(text="🗣️ Поговорить")],
            [KeyboardButton(text="🤔 Абсурдные дебаты"), KeyboardButton(text="🔄 Новый питомец")]
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
            [InlineKeyboardButton(text="🐲 Дракончик", callback_data="type_dragon")]
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

    # Получаем текущее время
    now = datetime.now()
    last_update = datetime.fromisoformat(pet['last_update'])

    # Считаем сколько часов прошло
    hours_passed = (now - last_update).total_seconds() / 3600

    # Уменьшаем показатели (по 2 единицы в час)
    decrease = int(hours_passed * 2)

    if decrease > 0:  # Обновляем только если прошло время
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

    # Эмодзи для типов питомцев
    emoji_map = {
        'cat': '🐱',
        'dog': '🐶',
        'dragon': '🐲'
    }

    pet_emoji = emoji_map.get(pet['type'], '🐱')

    # Создаем полоски для показателей
    def make_bar(value):
        filled = '█' * (value // 10)
        empty = '░' * (10 - value // 10)
        return f"[{filled}{empty}] {value}%"

    status = f"{pet_emoji} {pet['name']}\n\n"
    status += f"🍖 Голод: {make_bar(pet['hunger'])}\n"
    status += f"😊 Настроение: {make_bar(pet['mood'])}\n"
    status += f"⚡ Энергия: {make_bar(pet['energy'])}\n\n"

    # Реакция питомца в зависимости от состояния
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
            status += "🐲 Я могучий и довольный дракон!"
    else:
        status += "😊 Все хорошо!"

    return status


# Получение случайной фразы питомца
def get_random_phrase(pet_type, action="talk"):
    """Возвращает случайную фразу для типа питомца и действия"""
    pet_phrases

    if pet_type in pet_phrases and action in pet_phrases[pet_type]:
        phrases_list = pet_phrases[pet_type][action]
        if phrases_list:  # Проверяем, что список не пустой
            return random.choice(phrases_list)

    # Фразы по умолчанию; в случае ошибки при чтении json-файла
    default_phrases = {
        'cat': {'talk': 'Мяу! 🐱', 'feed': 'Мурр! 😸', 'play': 'Мяф! 🎾', 'sleep': 'Zzz... 😴'},
        'dog': {'talk': 'Гав! 🐶', 'feed': 'Ам-ам! 😋', 'play': 'Вуф! 🎾', 'sleep': 'Храп... 😴'},
        'dragon': {'talk': 'Рррр! 🐲', 'feed': 'Хрум! 🔥', 'play': 'Грр! ⚔️', 'sleep': 'Zzz... 💤'}
    }

    return default_phrases.get(pet_type, {}).get(action, "...")


# Получение случайного вопроса для дебатов
def get_random_debate():
    """Возвращает случайный вопрос для дебатов"""
    if "debates" in debates_data and debates_data["debates"]:
        return random.choice(debates_data["debates"])
    # В случае ошибки при чтении json-файла
    return "Что лучше: горячий лед или холодный огонь?"


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


# Обработчик выбора типа питомца (инлайн кнопки)
@dp.callback_query(F.data.startswith("type_"))
async def choose_pet_type(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if str(user_id) in pets_data:
        await callback.answer("У вас уже есть питомец!")
        return

    pet_type = callback.data.split("_")[1]  # Получаем тип из callback_data

    type_names = {"cat": "котика", "dog": "собачку", "dragon": "дракончика"}

    await callback.message.edit_text(
        f"Отлично! Вы выбрали {type_names[pet_type]} 🎉\n\n"
        f"Теперь введите имя для питомца:"
    )

    # Временно сохраняем тип питомца
    pets_data[f"temp_{user_id}"] = pet_type
    save_data(pets_data)


# Обработчик действий с питомцем (инлайн кнопки)
@dp.callback_query(F.data.startswith("action_"))
async def pet_action(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    action = callback.data.split("_")[1]  # Получаем действие из callback_data

    if str(user_id) not in pets_data:
        await callback.answer("У вас нет питомца!")
        return

    update_pet_stats(user_id)
    pet = pets_data[str(user_id)]

    emoji_map = {'cat': '🐱', 'dog': '🐶', 'dragon': '🐲'}
    pet_emoji = emoji_map.get(pet['type'], '🐱')

    if action == "feed":
        # Кормление: увеличивает голод, немного поднимает настроение
        pet['hunger'] = min(100, pet['hunger'] + 30)
        pet['mood'] = min(100, pet['mood'] + 10)
        phrase = get_random_phrase(pet['type'], 'feed')
        response = f"{pet_emoji} {pet['name']}: {phrase}"

    elif action == "play":
        # Игра: сильно поднимает настроение, но тратит энергию и голод
        if pet['energy'] < 15:
            response = f"{pet_emoji} {pet['name']}: Я слишком устал для игр... 😴"
        else:
            pet['mood'] = min(100, pet['mood'] + 25)
            pet['energy'] = max(0, pet['energy'] - 15)
            pet['hunger'] = max(0, pet['hunger'] - 10)  # Игра тратит энергию
            phrase = get_random_phrase(pet['type'], 'play')
            response = f"{pet_emoji} {pet['name']}: {phrase}"

    elif action == "sleep":
        # Сон: восстанавливает энергию, немного поднимает настроение, тратит немного голода
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

    # Разговор немного тратит энергию
    pet['energy'] = max(0, pet['energy'] - 3)
    pet['mood'] = min(100, pet['mood'] + 5)  # Но поднимает настроение

    # Получаем случайную фразу
    phrase = get_random_phrase(pet['type'], 'talk')

    emoji_map = {'cat': '🐱', 'dog': '🐶', 'dragon': '🐲'}
    pet_emoji = emoji_map.get(pet['type'], '🐱')

    # Сохраняем изменения
    pet['last_update'] = datetime.now().isoformat()
    save_data(pets_data)

    await message.answer(f"{pet_emoji} {pet['name']}: {phrase}")


# Обработчик кнопки "Абсурдные дебаты"
@dp.message(F.text == "🤔 Абсурдные дебаты")
async def absurd_debates(message: types.Message):
    user_id = message.from_user.id

    if str(user_id) not in pets_data:
        await message.answer("У вас нет питомца! Используйте /start")
        return

    update_pet_stats(user_id)
    pet = pets_data[str(user_id)]

    # Дебаты сильно тратят энергию, но поднимают настроение
    pet['energy'] = max(0, pet['energy'] - 8)
    pet['mood'] = min(100, pet['mood'] + 12)

    debate_question = get_random_debate()

    emoji_map = {'cat': '🐱', 'dog': '🐶', 'dragon': '🐲'}
    pet_emoji = emoji_map.get(pet['type'], '🐱')

    # Сохраняем изменения
    pet['last_update'] = datetime.now().isoformat()
    save_data(pets_data)

    # Питомец задаёт вопрос для дебатов
    await message.answer(
        f"{pet_emoji} {pet['name']} предлагает обсудить:\n\n"
        f"🤔 {debate_question}\n\n"
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


# Обработчик ввода имени питомца
@dp.message(F.text)
async def handle_pet_name(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    # Проверяем, создается ли сейчас питомец
    temp_key = f"temp_{user_id}"
    if temp_key in pets_data:
        pet_type = pets_data[temp_key]
        del pets_data[temp_key]

        # Проверяем длину имени
        if len(text) > 15:
            await message.answer("Имя слишком длинное! Максимум 15 символов.")
            return

        if not text.strip():
            await message.answer("Введите нормальное имя!")
            return

        create_pet(user_id, text.strip(), pet_type)

        type_names = {"cat": "котик", "dog": "собачка", "dragon": "дракончик"}
        emoji_map = {"cat": "🐱", "dog": "🐶", "dragon": "🐲"}

        await message.answer(
            f"🎉 Поздравляю! Ваш {type_names[pet_type]} {emoji_map[pet_type]} {text} создан!\n\n"
            f"Все показатели: 100% ✨\n\n"
            f"💡 Совет: Разные действия по-разному влияют на статы:\n"
            f"🍖 Кормление - восстанавливает голод\n"
            f"🎮 Игра - поднимает настроение, но тратит энергию\n"
            f"💤 Сон - восстанавливает энергию\n"
            f"🗣️ Общение и дебаты тоже влияют на питомца!",
            reply_markup=get_keyboard()
        )
    else:
        await message.answer("Не понимаю 🤔\nИспользуйте кнопки или создайте питомца командой /start")


# Запуск бота
async def main():
    print("🚀 Бот запущен!")
    print(f"📁 Данные сохраняются в: {DATA_FILE}")
    print(f"💬 Фразы питомца сохраняются в : {PHRASES_FILE}")
    print(f"🤔 Дебаты сохраняются в: {DEBATES_FILE}")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
