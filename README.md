# Bot for Advertising

This Python code provides

### Setup instrictions:
#### 1. Create a virtual environment:

`python -m venv env`

#### 2. Enter to the virtual environment (On Windows):

`env\Scripts\activate`

#### 3. Install dependencies into the virtual environment:
```shell
pip install -r  requirements.txt
```
#### 4. Insert your Telegram API Token.
Create file .env and add there `TELEGRAM_TOKEN` with your Telegram API Token.

#### 5. Run the application:
Run the code: 

`python app.py`

#### 6. Enter start command in the bot telegram chanel:
```sh
/start
```
#### 7. Enter command for communicate with bot in the bot telegram chanel:
```sh
/add_ad
```

#### 7. Enter data for posting an advertisement in the bot telegram channel, e.g.:
```sh
Hello, I am selling a bike
###
Kyiv
###
200
```

### Logging:

The script records its operations and any errors in the bot_info.log file for debugging and monitoring

# Tasks
[X] 1. юзер відкрив діалог з ботом і натиснув кнопку додати оголошення (кнопка інлайн чи тг клавіатура)

[X] 2. бот юзеру віповів шаблоном оголошення, і написав що шаблон треба відредагувати та відправити боту назад

[X] 3. юзер відправляє відредагований шаблон оголошення

[-] 4. бот валідує оголошення, текст оголошення більше 0 символів, більше 5 слів, меньше 2048 символів

[-] 5. якщо валідація не пройшла, відправляємо юзеру повідомлення де саме у нього помилка, якщо валідація пройшла, то відправляємо повідомлення що тепер треба відправити фото оголошення, від 1 до 10

[-] 6. юзер відправляє фото

[-] 7. якщо це дійсно фото і їх більше 0 та меньше 10, переходимо на наступний крок, якщо ні то відправляємо помилку

[-] 8. фото пройшли, показуємо фінальний текст оголошення разом з фото і питаємо у юзера "видалити" чи "опублікувати"

[-] 9. якщо видалити - видаляємо, якщо опублікувати - публікуємо у тг канал з оголошеннями (створити будь який для тесту)

[X] 10. після публікації зберігаємо текст оголошення у папку з назвою YY-MM-DD_tguserid, текст в файл post.json (в форматі json), фото кладемо поряд з цим файлом