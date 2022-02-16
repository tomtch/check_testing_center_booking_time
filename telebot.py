import os
import telebot

API_KEY = os.getenv('API_TOKEN')
bot = telebot.TeleBot('',parse_mode=None)

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.reply_to(message, 'Hey! hows it going?')

bot.polling()