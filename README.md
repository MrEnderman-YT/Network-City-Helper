<div align="center">
<img src="data/banner%20standart%20github.png">

<h1>Network City Helper</h1>

<img alt="Static Badge" src="https://img.shields.io/badge/tag-v1.0.0-blue?logo=codenewbie&logoColor=007EC6">

<img alt="Static Badge" src="https://img.shields.io/badge/python-v3.11.9-yellow?logo=python&logoColor=FBDE02&labelColor=gray&color=FFE100">
<img alt="Static Badge" src="https://img.shields.io/badge/bot-Network%20City%20Helper-12C427?logo=dependabot&logoColor=12C427">
<img alt="Static Badge" src="https://img.shields.io/badge/license-MIT-12C4C4?style=flat&logo=gitbook&logoColor=12C4C4">

</div>
⠀

> [!CAUTION]
> Бот не имеет отношения к «ИрТеху»
⠀
## 📌 Description
⠀

**Network City Helper** — это ваш персональный телеграм-бот, созданный для оказания помощи ученикам в учебном процессе. Он взаимодействует с платформой "Сетевой город", предлагает широкий спектр функций, направленных на упрощение организации учебного времени и управления задачами. Бот может отправлять итоговые оценки и уведомления о просроченных заданиях, а также делиться актуальным расписанием и домашним заданием на завтрашний день.

_Тем не менее, стоит отметить, что предоставленный код нуждается в доработке. В текущем виде он может содержать избыточные участки кода, которые могут быть оптимизированы для повышения производительности и улучшения читаемости._

⠀
## 🔓 Bot .env
⠀

| Environment Variable Name | Description                                                                                                                                                                                                                                                                                                                 | Recommend Value                                                     |
|---------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| WEBHOOK_PATH              | The path to the webhook where Telegram servers send requests for bot updates. It is not recommended to change it if only one bot will be deployed. In case several bots will be deployed on the same server, it will be necessary to change it, because there will be path collision (Does not apply to the multibot case). | "" (empty string)                                                   |
| WEBAPP_HOST               | Hostname for Telegram bot, it is not recommended to change in case you use docker-compose.                                                                                                                                                                                                                                  | For docker-compose="0.0.0.0".<br/>For local deployment="localhost". |
| WEBAPP_PORT               | Port for Telegram bot, if you plan to deploy several bots on the same server, you will need to assign a different port to each one (Not relevant to the multibot case).                                                                                                                                                     | No recommended value                                                |
| TOKEN                     | Token from your Telegram bot, you can get it for free in Telegram from the bot of all bots with the username @botfather.                                                                                                                                                                                                    | No recommended value                                                |
| NGROK_TOKEN               | Token from your NGROK profile, it is needed for port forwarding to the Internet. The main advantage of using NGROK is that NGROK assigns the HTTPS certificate for free.                                                                                                                                                    | No recommended value                                                |
| ADMIN_ID_LIST             | List of Telegram id of all admins of your bot. This list is used to check for access to the admin menu.                                                                                                                                                                                                                     | No recommended value                                                |
| SUPPORT_LINK              | A link to the Telegram profile that will be sent by the bot to the user when the “Help” button is pressed.                                                                                                                                                                                                                  | https://t.me/${YOUR_USERNAME_TG}                                    |
| DB_NAME                   | The name of the SQLite database file.                                                                                                                                                                                                                                                                                       | database.db                                                         |
| PAGE_ENTIRES              | The number of entries per page. Serves as a variable for pagination.                                                                                                                                                                                                                                                        | 8                                                                   |
| BOT_LANGUAGE              | The name of the .json file with the l10n localization. At the moment only English localization is supplied out of the box, but you can make your own if you create a file in the l10n folder with the same keys as in l10n/en.json.                                                                                         | "en"                                                                |
| MULTIBOT                  | Experimental functionality, allows you to raise several bots in one process. And there will be one main bot, where you can create other bots with the command “/add $BOT_TOKEN”. Accepts string parameters “true” or “false”.                                                                                               | "false"                                                             |
| DB_PASS                   | Only works in the feature/sqlalchemy-sqlcipher branch. The password that will be used to encrypt your SQLite database.                                                                                                                                                                                                      | No recommended value                                                |


⠀
## 💻 Bot setup
⠀

asddsa

⠀
## 📋 Todo List
⠀

- [x] Создать данный Todo list ♥
- [ ] Сделать функцию просмотра оценок на неделю
- [ ] Сделать калькулятор оценок
- [ ] Сделать возможность входа через гос-услуги

⠀
## 💼 Credits
⠀

[netschoolapi](https://github.com/nm17/netschoolapi) - асинхронный клиент для «Сетевого города»

[netschoolapi](https://github.com/nm17/netschoolapi) - мой форк асинхронного клиента для «Сетевого города»

[schedule](https://github.com/dbader/schedule?tab=readme-ov-file) - планировщик задач.

[aiogram](https://github.com/aiogram/aiogram) - асинхронная библиотека для API Telegram Bot.

⠀
## 👤 Author of Network City Helper
**© Алексеев Роман**
