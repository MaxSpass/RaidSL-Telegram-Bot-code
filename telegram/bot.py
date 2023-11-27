import telebot

TELEGRAM_BOT_ACCESS_TOKEN = '6722044970:AAGZ5EtkQPVFpSzHqhKeAiCf3sXD-PRX6_w'

bot = telebot.TeleBot(TELEGRAM_BOT_ACCESS_TOKEN, parse_mode=None) # Y

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")