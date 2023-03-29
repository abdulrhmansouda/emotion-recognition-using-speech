import telebot
from decouple import config
import os
from DealingWithModel import test_9_emotions
import time
import random
import subprocess

def ogg2wav(src_filename, dest_filename):
    process = subprocess.run(['ffmpeg', '-i', src_filename, dest_filename])
    if process.returncode != 0:
        raise Exception("Something went wrong")


BOT_TOKEN = config('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


# @bot.message_handler(commands=['start', 'help'])
# def welcome(message):
#     bot.send_message(message.chat.id, 'wellcome hi hellow')


# @bot.message_handler(commands=['abd'])
# def abd(message):
#     bot.send_message(message.chat.id, 'abd')

rec = test_9_emotions()
print('ready')

def nine_emotions(file_info,prefix=''):
    downloaded_file = bot.download_file(file_info.file_path)
    with open(os.path.dirname(__file__)+'\\temp\\'+'a.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)
    src_filename ='a.ogg'
    dest_filename = str(int(time.time())) +'_'+ str(int(random.random()*9999999999))+'.wav'
    ogg2wav('temp/'+ src_filename, 'temp/'+ dest_filename)
    emotion , score = str(rec.predict('temp/'+ dest_filename)),rec.test_score() 
    os.rename('temp/'+ dest_filename,'temp/'+  prefix+'_'+emotion+'_'+dest_filename)
    return emotion,score


@bot.message_handler(content_types=['audio', 'voice'])
def replay(message):
    bot.reply_to(message, 'The voice under processing please calm down.')
    bot.reply_to(message, 'Baby calm down🙂.')
    file_info = bot.get_file(message.voice.file_id)
    emotion ,score= nine_emotions(file_info,message.from_user.username)
    bot.reply_to(message, 'The Emotion Is: '+str(emotion))
    bot.reply_to(message, 'The Score Is: '+str(score))
    print(emotion)
    match emotion:
        case "neutral":
            bot.reply_to(message, '🙂')
        case "happy":
            bot.reply_to(message, '😄')
        case "sad":
            bot.reply_to(message, '🥹')
        case "angry":
            bot.reply_to(message, '😡')
        case "ps":
            bot.reply_to(message, '😲')
        case "calm":
            bot.reply_to(message, '😌')
        case "fear":
            bot.reply_to(message, '😱')
        case "disgust":
            bot.reply_to(message, '🤢')
        case "boredom":
            bot.reply_to(message, '🥱')

    

@bot.message_handler(content_types=['document'])
def replay(message):
    file_info = bot.get_file(message.document.file_id)
    emotion ,score= nine_emotions(file_info)
    # emotion ,score= five_emotions(file_info)
    bot.reply_to(message, 'The Emotion Is: '+str(emotion))
    bot.reply_to(message, 'The Score Is: '+str(score))
    print(emotion)
    match emotion:
        case "neutral":
            bot.reply_to(message, '🙂')
        case "happy":
            bot.reply_to(message, '😄')
        case "sad":
            bot.reply_to(message, '🥹')
        case "angry":
            bot.reply_to(message, '😡')
        case "ps":
            bot.reply_to(message, '😲')
        case "calm":
            bot.reply_to(message, '😌')
        case "fear":
            bot.reply_to(message, '😱')
        case "disgust":
            bot.reply_to(message, '🤢')
        case "boredom":
            bot.reply_to(message, '🥱')


bot.polling()