## Содержание
1. [О боте](#о-боте)
2. [Использование JSON для хранения данных](#использование-json-для-хранения-данных)
   - [Чтение данных с помощью `json.load`](#чтение-данных-с-помощью-jsonload)
   - [Запись данных с помощью `json.dump`](#запись-данных-с-помощью-jsondump)
   - [Зачем это нужно?](#зачем-это-нужно)
3. [Использование `aiogram` для создания бота](#использование-aiogram-для-создания-бота)
   - [Инициализация бота](#инициализация-бота)
   - [Обработка команды `/start`](#обработка-команды-start)
   - [Создание клавиатур](#создание-клавиатур)
   - [Обработка callback-запросов](#обработка-callback-запросов)
   - [Обработка текстовых сообщений](#обработка-текстовых-сообщений)
   - [Запуск бота](#запуск-бота)
4. [Установка и запуск](#установка-и-запуск)

---

Этот гайд описывает **Telegram-бота**, написанного на Python с использованием библиотеки `aiogram`. Бот позволяет пользователям создавать и заботиться о виртуальных питомцах, управлять их характеристиками, взаимодействовать с ними через действия, участвовать в "абсурдных дебатах" и играть в игру "Города". В гайде объясняется функциональность бота, использование JSON для сохранения данных и реализация `aiogram` на конкретных примерах из кода.

---

## О боте

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)

**Telegram-бот "Tamagotchi"** — это интерактивный бот для Telegram, который позволяет:
- Создавать виртуального питомца (кот 🐱, собака 🐶 или попугай 🦜) и давать ему имя.
- Следить за характеристиками питомца: голод (🍖), настроение (😊) и энергия (⚡).
- Выполнять действия: кормить, играть или укладывать спать, каждое из которых по-разному влияет на характеристики питомца.
- Участвовать в "филосовских вопросах" — отвечать на случайные философские или забавные вопросы, предложенные питомцем.
- Играть в "Города" с ботом, называя города по очереди в соответствии с правилами.
- Сбрасывать текущего питомца и создавать нового.

Данные о питомцах и состоянии игры в города сохраняются в JSON-файлах, что обеспечивает персистентность между запусками бота. Характеристики питомца (голод, настроение, энергия) автоматически уменьшаются со временем, добавляя реалистичности игровому процессу.

---

## Использование JSON для хранения данных

JSON (JavaScript Object Notation) используется для сохранения данных о питомцах и состоянии игры в города. Это позволяет боту загружать данные при старте и сохранять их при изменениях. В коде используются два JSON-файла:
- `pets_data.json`: хранит информацию о питомцах пользователей (имя, тип, характеристики, время последнего обновления).
- `cities_game_data.json`: хранит состояние игры в города (использованные города, текущий счет, последняя буква).

### Чтение данных с помощью `json.load`

Функция `json.load(f)` читает данные из JSON-файла и преобразует их в Python-объект (обычно словарь). Она используется в функциях `load_data()` и `load_cities_game_data()` для загрузки данных из соответствующих файлов.

**Пример** (функция `load_data()`):
```python
def load_data():
    """Загружает данные питомцев из JSON файла"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}
```
- `os.path.exists(DATA_FILE)` проверяет, существует ли файл `pets_data.json`.
- `open(DATA_FILE, 'r', encoding='utf-8')` открывает файл в режиме чтения (`'r'`) с кодировкой UTF-8 для поддержки русских символов.
- `as f` создает файловый объект `f`, который передается в `json.load(f)` для чтения JSON и преобразования его в словарь.
- Если файл не существует или поврежден, возвращается пустой словарь `{}`.

**Результат**: Если в `pets_data.json` хранится:
```json
{
  "12345": {
    "name": "Мурзик",
    "type": "cat",
    "hunger": 80,
    "mood": 90,
    "energy": 70,
    "last_update": "2025-06-04T13:58:00"
  }
}
```
`json.load(f)` возвращает эквивалентный Python-словарь.

### Запись данных с помощью `json.dump`

Функция `json.dump(data, f, ensure_ascii=False, indent=2)` записывает Python-объект (обычно словарь) в JSON-файл. Она используется в функциях `save_data()` и `save_cities_game_data()`.

**Пример** (функция `save_data()`):
```python
def save_data(data):
    """Сохраняет данные питомцев в JSON файл"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```
- `data`: Python-словарь, содержащий данные (например, информацию о питомцах).
- `open(DATA_FILE, 'w', encoding='utf-8')`: открывает файл `pets_data.json` в режиме записи (`'w'`), перезаписывая его содержимое.
- `f`: файловый объект, в который записываются данные.
- `ensure_ascii=False`: сохраняет русские символы (например, "Мурзик") без преобразования в ASCII-коды (например, `\u041c`).
- `indent=2`: форматирует JSON с отступами в 2 пробела для удобства чтения.

**Результат**: Если `data` — это:
```python
{
    "12345": {
        "name": "Мурзик",
        "type": "cat",
        "hunger": 80,
        "mood": 90,
        "energy": 70,
        "last_update": "2025-06-04T13:58:00"
    }
}
```
В файле `pets_data.json` появится:
```json
{
  "12345": {
    "name": "Мурзик",
    "type": "cat",
    "hunger": 80,
    "mood": 90,
    "energy": 70,
    "last_update": "2025-06-04T13:58:00"
  }
}
```

### Зачем это нужно?
- **Персистентность**: JSON-файлы сохраняют данные между запусками бота.
- **Читаемость**: `indent=2` делает файлы удобными для отладки.
- **Поддержка Unicode**: `ensure_ascii=False` и `encoding='utf-8'` обеспечивают корректную работу с русским текстом.
- **Гибкость**: JSON легко расширять, например, для добавления новых данных о пользователях или играх.

---

## Использование `aiogram` для создания бота

Библиотека `aiogram` используется для обработки сообщений и callback-запросов в Telegram. Бот реализует команды, кнопки (обычные и инлайн) и логику взаимодействия с питомцами и игрой в города.

### Инициализация бота

Бот инициализируется с использованием токена, хранящегося в переменной окружения `BOT_TOKEN`.

**Пример**:
```python
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения!")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
```
- `os.getenv("BOT_TOKEN")`: получает токен бота из переменных окружения для безопасности.
- `Bot(token=BOT_TOKEN)`: создает объект бота.
- `Dispatcher()`: создает диспетчер для обработки входящих сообщений и callback-запросов.

### Обработка команды `/start`

Команда `/start` запускает процесс создания питомца или уведомляет, что питомец уже существует.

**Пример**:
```python
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
```
- `@dp.message(Command("start"))`: декоратор, связывающий функцию с командой `/start`.
- `message.from_user.id`: получает ID пользователя.
- Если питомец уже существует, отображается клавиатура с действиями (`get_keyboard()`).
- Если питомца нет, показывается инлайн-клавиатура для выбора типа питомца (`get_pet_type_keyboard()`).

### Создание клавиатур

Бот использует два типа клавиатур:
1. **Обычная клавиатура** (ReplyKeyboardMarkup): отображается под строкой ввода.
2. **Инлайн-клавиатура** (InlineKeyboardMarkup): отображается в сообщении для выбора действий.

**Пример (обычная клавиатура)**:
```python
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
```
- Создает клавиатуру с пятью кнопками для основных действий.
- `resize_keyboard=True`: адаптирует размер клавиатуры под экран.

**Пример (инлайн-клавиатура)**:
```python
def get_pet_type_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🐱 Котик", callback_data="type_cat")],
            [InlineKeyboardButton(text="🐶 Собачка", callback_data="type_dog")],
            [InlineKeyboardButton(text="🦜 Попуг", callback_data="type_dragon")]
        ]
    )
    return keyboard
```
- Создает инлайн-клавиатуру для выбора типа питомца.
- `callback_data`: данные, отправляемые при нажатии кнопки, используются для определения действия.

### Обработка callback-запросов

Callback-запросы обрабатываются для выбора типа питомца и выполнения действий (кормление, игра, сон).

**Пример (выбор типа питомца)**:
```python
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
```
- `@dp.callback_query(F.data.startswith("type_"))`: обрабатывает нажатия на инлайн-кнопки с `callback_data`, начинающимся на `type_`.
- `callback.data.split("_")[1]`: извлекает тип питомца (например, `cat` из `type_cat`).
- `callback.message.edit_text`: изменяет сообщение, чтобы запросить имя питомца.
- Временное сохранение типа питомца в `pets_data`.

**Пример (действия с питомцем)**:
```python
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
    ...
    pet['last_update'] = datetime.now().isoformat()
    save_data(pets_data)
    await callback.answer()
    await callback.message.answer(response)
```
- Обрабатывает действия (например, `action_feed`).
- Обновляет характеристики питомца (`hunger`, `mood`, `energy`) в зависимости от действия.
- Сохраняет изменения в `pets_data.json` с помощью `save_data()`.

### Обработка текстовых сообщений

Текстовые сообщения обрабатываются для ввода имени питомца, хода в игре "Города" или обработки неизвестных команд.

**Пример**:
```python
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
        type_names = {"cat": "котик", "dog": "собачка", "dragon": "дракончик"}
        emoji_map = {"cat": "🐱", "dog": "🐶", "parrot": "🦜"}
        await message.answer(
            f"🎉 Поздравляю! Ваш {type_names[pet_type]} {emoji_map[pet_type]} {text} создан!\n\n"
            f"Все показатели: 100% ✨\n\n"
            f"💡 Совет: Разные действия по-разному влияют на статы:\n..."
        )
    else:
        await message.answer("Не понимаю 🤔\nИспользуйте кнопки или создайте питомца командой /start")
```
- Проверяет, активна ли игра в города (`is_cities_game_active()`), и если да, обрабатывает ход игрока.
- Если ожидается ввод имени питомца (`temp_key`), создает нового питомца.
- Иначе сообщает, что команда неизвестна.

### Запуск бота

Бот запускается с использованием `asyncio` для асинхронной обработки.

**Пример**:
```python
async def main():
    print("🚀 Бот запущен!")
    print(f"📁 Данные сохраняются в: {DATA_FILE}")
    print(f"🎮 Данные игры в города сохраняются в: {CITIES_GAME_FILE}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```
- `dp.start_polling(bot)`: запускает опрос новых сообщений от Telegram.
- `asyncio.run(main())`: выполняет асинхронную функцию `main()`.

---

## Установка и запуск

1. **Установка зависимостей**:
   - Убедитесь, что установлен Python 3.7+.
   - Установите зависимости из файла `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

2. **Настройка токена**:
   - Получите токен бота от `@BotFather` в Telegram.
   - **Рекомендуемый способ**: Используйте переменную окружения `BOT_TOKEN` для безопасности, чтобы не указывать токен напрямую в коде:
     ```bash
     export BOT_TOKEN="ваш_токен"
     ```
   - **Альтернативный способ**: Укажите токен напрямую в коде, заменив:
     ```python
     BOT_TOKEN = os.getenv("BOT_TOKEN")
     if not BOT_TOKEN:
         raise ValueError("BOT_TOKEN не найден в переменных окружения!")
     ```
     на:
     ```python
     BOT_TOKEN = "ваш_токен"
     ```
     **Внимание**: Указание токена в коде небезопасно. Всегда используйте переменные окружения для продакшн-версий.

3. **Запуск бота**:
   - Убедитесь, что все файлы (`bot.py`, `cities.py`, `debates.py`, `pet_phrases.py`) находятся в правильной структуре папок:
     ```bash
     project_name/
      ├── bot.py               # Основной файл бота
      ├── data/
      │    ├── cities.py        # Список городов
      │    ├── debates.py       # Абсурдные дебаты
      │    └── pet_phrases.py   # Фразы питомцев
      ├── pets_data.json       # Файл данных питомцев
      └── cities_game_data.json # Файл данных игры в города
     ```
     Если файлов `pets_data.json` и `cities_game_data.json` - они создадутся автоматически при первом запуске бота.
   - Запустите:
     ```bash
     python bot.py
     ```

4. **Отладка**:
   - JSON-файлы (`pets_data.json`, `cities_game_data.json`) создаются автоматически при первом запуске.
   - Логи выводятся в консоль, включая пути к файлам данных.
