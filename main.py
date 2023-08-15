python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import telebot

# Ваши учетные данные для отправки почты
smtp_server = 'SMTP_SERVER'
smtp_port = 587
smtp_login = 'SMTP_LOGIN'
smtp_password = 'SMTP_PASSWORD'

# Ваши учетные данные для телеграмм бота
telegram_token = 'TELEGRAM_TOKEN'
telegram_chat_id = 'TELEGRAM_CHAT_ID'

# Создаем экземпляр бота
bot = telebot.TeleBot(telegram_token)

@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    instructions = "Привет! Отправь мне письмо, и я перешлю его на указанный адрес электронной почты."
    bot.reply_to(message, instructions)

@bot.message_handler(func=lambda message: True)
def forward_email(message):
    # Получаем текст сообщения от пользователя
    user_message = message.text

    # Создаем объект MIMEMultipart для формирования письма
    email_message = MIMEMultipart()
    email_message['From'] = smtp_login
    email_message['To'] = 'EMAIL_RECIPIENT'
    email_message['Subject'] = 'Forwarded Email'

    # Добавляем текст сообщения в письмо
    email_message.attach(MIMEText(user_message, 'plain'))

    # Создаем SMTP-соединение и отправляем письмо
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_login, smtp_password)
        server.send_message(email_message)

    # Отправляем подтверждение пользователю через телеграмм
    confirmation_message = "Ваше письмо успешно отправлено!"
    bot.reply_to(message, confirmation_message)

# Запускаем бота
bot.polling()