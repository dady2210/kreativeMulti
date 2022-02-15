from __future__ import unicode_literals 
import requests
import json
import base64
import wget
from jsonpath_ng import jsonpath, parse
from telebot import TeleBot
import youtube_dl
import requests
import json
import time
import os
import base64
import shutil, sys
from zipfile import ZipFile
from shutil import rmtree
from os.path import basename
from jsonpath_ng import jsonpath, parse
TOKEN = os.environ['TOKEN']
bot = TeleBot(TOKEN)
# Handle '/start' and '/help'
@bot.message_handler(commands=['crehana'])
def send_usuario(message):
    user_id = str(message.from_user.id)
    user_first_name = str(message.chat.first_name) 
    msg = bot.reply_to(message, f"Hey! Bienvenido a Crehana {user_first_name} tu id es : {user_id} \n Ingresa ID del curso")
    chat_id = message.chat.id
    lista_cursos = message.text
    #prueba guardar y verificar en base de datos#
    #prueba guardar y verificar en base de datos#
    bot.register_next_step_handler(msg, process_name_step)
def process_name_step(message):
    try:
        chat_id = message.chat.id
        lista_cursos = message.text
        msg = bot.send_message(chat_id, 'Estamos bajando el curso!')
    except Exception as e:
        bot.reply_to(message, 'oooops')

    for num1 in lista_cursos.split(','):
        dictionary = {
        "query": "query course($courseId: String!) {course(id: $courseId) {title attachmentSet{edges{node{attachment}}} modules{videoLectureSet{edges{node{title  subtitleList{subtitleFile} videoLectureSource{provider desktopPlaylists{url}}}}}} }}",
        "operationName": "course",
    "variables": {
            "courseId": int(num1)
        }
        }
        print("Descargando : "+num1)
        jsonString = json.dumps(dictionary)
        url = "https://www.crehana.com/api/v2/graph/"
        headers = {
                "content-type": "application/json",
                "creh-platform-type": "desktop",
                "authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InJhbmRvbWN1cnNlc3BybzEyMzQ1NkB5b3BtYWlsLmNvbSIsImV4cCI6MTY0NjA4MTkzMywianRpIjoiYzA3NWM4OGE4ZDBmMTFlY2I0NmEwMjQyYWMxMTAwMDMiLCJvcmlnSWF0IjoxNjQ0Nzg1OTMzfQ.XGhbTyBM_nZSqETQz0fgOjScKJtymMO2wAQmBO2R8FU",
                "Accept-Language": "es",
                "x-requested-with": "XMLHttpRequest"
            }

        response = requests.post(url, data=jsonString, headers=headers)

        json_data = json.loads(response.text)
        file = open(num1+"-wtemp.txt", "w")
        file.write(response.text)
        file.close()
    #capturo titulo
        with open(num1+"-wtemp.txt", 'r', encoding="latin-1") as json_file:
            json_data = json.load(json_file)
        jsonpath_expression = parse('data.course.title')
        for tits in jsonpath_expression.find(json_data):
                curstitle = tits.value
                print (curstitle)
    #fin captura titulo
    #inicio captura files links
        with open(num1+"-wtemp.txt", 'r', encoding="latin-1") as json_file:
            json_data = json.load(json_file)
        jsonpath_expression = parse('data.course.attachmentSet.edges[*].node.attachment')
        for filesdmk in jsonpath_expression.find(json_data):
                print(filesdmk.value,file=open(num1+"-files.txt","a"))
     #inicio captura files links          
        with open(num1+"-wtemp.txt", 'r', encoding="latin-1") as json_file:
            json_data = json.load(json_file)
        jsonpath_expression = parse('data.course.modules.[*].videoLectureSet.edges.[*].node.videoLectureSource.[0].desktopPlaylists.[*].url')
        for match1 in jsonpath_expression.find(json_data):
                print(match1.value,file=open(num1+".txt","a"))
        if os.path.isfile(num1+'.txt') ==True :
            pass
        else :
            with open(num1+"-wtemp.txt", 'r', encoding="latin-1") as json_file:
                json_data = json.load(json_file)
            jsonpath_expression = parse('data.course.modules.[*].videoLectureSet.edges.[*].node.videoLectureSource.[*].desktopPlaylists.[*].url')
            for match2 in jsonpath_expression.find(json_data):
                print(match2.value,file=open(num1+".txt","a"))
    file="./"+num1+".txt"
    filezip="./"+num1+"-files.txt"
    bot.send_message(chat_id, "Te estamos enviando el curso: "+curstitle)
    bot.send_document(chat_id, document=open(file, 'rb'))
    bot.send_message(chat_id, "Te estamos enviando los descargables")
    bot.send_document(chat_id, document=open(filezip, 'rb'))
    os.remove(num1+"-wtemp.txt")
    os.remove(num1+"-files.txt")
    os.remove(num1+".txt")
@bot.message_handler(commands=['skillshare'])
def send_usuarioSK(message):
    user_id = str(message.from_user.id)
    user_first_name = str(message.chat.first_name) 
    msg = bot.reply_to(message, f"Hey! Bienvenido a Skillshare {user_first_name} tu id es : {user_id} \n Ingresa ID del curso")
    chat_id = message.chat.id
    lista_cursos = message.text
    #prueba guardar y verificar en base de datos#
    #prueba guardar y verificar en base de datos#
    bot.register_next_step_handler(msg, process_name_stepSK)
def process_name_stepSK(message):
    try:
        chat_id = message.chat.id
        lista_cursos = message.text
        msg = bot.send_message(chat_id, 'Estamos bajando el curso!')
    except Exception as e:
        bot.reply_to(message, 'oooops')
    namesub=int(0)
    for num1SK in lista_cursos.split(','):
        url = "https://api.skillshare.com/classes/"+num1SK
        headers = {
            "content-type": "application/json",
            "Accept-Charset": "latin-1",
            "Accept-Language": "es",
            "cookie": "skillshare_user_=3a9a0f3d5bf04b4a67fefae94c59dd5cdec10465a%3A4%3A%7Bi%3A0%3Bs%3A8%3A%2224612416%22%3Bi%3A1%3Bs%3A19%3A%22ba3daniel%40gmail.com%22%3Bi%3A2%3Bi%3A7776000%3Bi%3A3%3Ba%3A4%3A%7Bs%3A8%3A%22username%22%3Bs%3A9%3A%22726396372%22%3Bs%3A10%3A%22login_time%22%3Bs%3A19%3A%222022-02-15%2000%3A05%3A07%22%3Bs%3A10%3A%22touch_time%22%3Bs%3A19%3A%222022-02-15%2000%3A05%3A14%22%3Bs%3A5%3A%22roles%22%3Bs%3A0%3A%22%22%3B%7D%7D",
        }
        response = requests.get(url, headers=headers)
        json_data = json.loads(response.text)
        file = open(num1SK+".txt", "w")
        file.write(response.text)
        file.close()
    with open(num1SK+".txt", 'r', encoding="latin-1") as json_file:
        json_data = json.load(json_file)
    jsonpath_expression = parse('_embedded.sessions._embedded.sessions[*].video_hashed_id')
    for match in jsonpath_expression.find(json_data):
              bccode=match.value
              bccode=bccode.replace('b', '')
              bccode=bccode.replace('c', '')
              bccode=bccode.replace(':', '')
              print(bccode,file=open("output.txt","a+"))           

    f = open ('output.txt','r')
    mensaje = f.readlines()
    for men in mensaje:
        men=men.replace('\n','')
        url = "https://edge.api.brightcove.com/playback/v1/accounts/3695997568001/videos/"+men
        headers = {
                "Accept": "application/json;pk=BCpkADawqM2OOcM6njnM7hf9EaK6lIFlqiXB0iWjqGWUQjU7R8965xUvIQNqdQbnDTLz0IAO7E6Ir2rIbXJtFdzrGtitoee0n1XXRliD-RH9A-svuvNW9qgo3Bh34HEZjXjG4Nml4iyz3KqF",
            }
        response = requests.get(url, headers=headers)
        json_data = json.loads(response.text)
        file = open("videoURL"+men+".txt", "w")
        file.write(response.text)
        file.close()
        with open("videoURL"+men+".txt", 'r', encoding="latin-1") as json_file:
            json_data = json.load(json_file)
        jsonpath_expression = parse('text_tracks.[2].sources.[*].src')
        os.makedirs('./subs/'+num1SK+'/', exist_ok=True)
        for matchSUBS in jsonpath_expression.find(json_data):
              url = matchSUBS.value
              r = requests.get(url, allow_redirects=True)
              namesub = int(namesub) + 1
              namesub1 = str(namesub)
              zerofill = namesub1.zfill(5)
              open('./subs/'+num1SK+'/'+str(zerofill)+'.vtt', 'wb').write(r.content)    
        with open("videoURL"+men+".txt", 'r', encoding="latin-1") as json_file:
            json_data = json.load(json_file)
        jsonpath_expression = parse('sources.[6].src')
        for matchURL in jsonpath_expression.find(json_data):
                    print(matchURL.value,file=open(num1SK+"-Videos.txt","a+"))   
        os.remove("videoURL"+men+".txt")
        f.close()
    dst = './'+num1SK # where to save
    src = './subs/'+num1SK+'/' # directory to be zipped
    print ("Estamos comprimiendo su archivo ZIP")
    path_to_archive = shutil.make_archive(dst,'zip',src)
    filezipSK="./"+num1SK+"-Videos.txt"
    fileSK="./"+num1SK+".zip"
    bot.send_message(chat_id, "Te estamos enviando el curso")
    bot.send_document(chat_id, document=open(fileSK, 'rb'))
    bot.send_message(chat_id, "Te estamos enviando los subtitulos")
    bot.send_document(chat_id, document=open(filezipSK, 'rb'))
    rmtree('./subs')
    os.remove("./"+num1SK+"-Videos.txt")
    os.remove("./output.txt")
    os.remove(num1SK+".txt")
    os.remove(num1SK+".zip")


###########################################LIMPIEZA#
bot.polling()


