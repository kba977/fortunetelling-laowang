import telebot
import requests
import urllib
import json

API_TOKEN = '7453098624:AAHviGO2xyaDzNFHZ4_Z_XaZ6Hjmb0FE2YU'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
  bot.reply_to(message, '你好!')

@bot.message_handler(content_types=['voice', 'audio'])
def handle_docs_audio(message):
  try:
    # 获取文件 ID
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    
    # 构建文件的下载链接
    file_path = file_info.file_path
    file_url = f'https://api.telegram.org/file/bot{API_TOKEN}/{file_path}'
    
    # 发送文件下载链接给用户
    bot.reply_to(message, f"你的语音文件链接是: {file_url}")
  except Exception as e:
    bot.reply_to(message, f"发生错误: {str(e)}")

@bot.message_handler(content_types=['photo'])
def handle_docs_image(message):
  print(message)
  try:
    file_id = message.photo[-1].file_id
    file_idfile_info = bot.get_file(file_id)
    file_url = f'https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}'
    bot.reply_to(message, file_url)
  except Exception as e:
    bot.reply_to(message, f"发生错误: {str(e)}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
  try:
    encoded_text = urllib.parse.quote(message.text)
    response = requests.post('http://localhost:8000/chat?query='+encoded_text, timeout=100)
    if response.status_code == 200:
      bot.reply_to(message, json.loads(response.text)['output'])
    else:
      bot.reply_to(message, "对不起, 我不知该如何回答你")
  except requests.RequestException as e:
    bot.reply_to(message, f"发生错误: {str(e)}")


bot.infinity_polling()