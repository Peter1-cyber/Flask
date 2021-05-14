# -*- coding: utf-8 -*-
""" Программа использует flask и запускает веб-сервер. 
При запросе к этому серверу он возвращает текст "Привет, Мир!" """
from flask import Flask, redirect, url_for, session, request, render_template
from db_scripts import *
import os 
from random import shuffle
folder = os.getcwd()



def save_answers():
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')
    session['last_question'] = quest_id
    session['total'] += 1
    if check_answer(quest_id, answer):
        session['answers'] += 1
    

def question_form(question):
    alist=[question[2], question[3], question[4], question[5]]
    shuffle(alist)
    return render_template("test.html", question=question[1], quest_id=question[0], answers_list=alist)



def start_quiz(quiz_id):
    session['quiz']= quiz_id
    session['last_question'] = 0
    session["total"] = 0
    session["answers"] = 0

def index():
    """ Функция возвращает текст документа """
    if request.method == 'GET':
        start_quiz(-1)
        return quiz_form()
    if request.method == 'POST':
        quest_id = request.form.get('quiz')
        start_quiz(quest_id)

        return redirect(url_for("test"))

def quiz_form():
    q_list = get_quizes()
    return render_template("start.html", q_list = q_list)
    




def test():
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for("index"))
    else:
        if request.method == 'POST':
            save_answers()
        a = get_question_after(session ['last_question'], session ['quiz'])
        if a is None or len(a) == 0:
            return redirect(url_for("result")) 
        else:
            return question_form(a)


def result():


    return render_template("result.html", answers = session["answers"], total = session["total"])




# Создаём объект веб-приложения:
app = Flask(__name__, template_folder=folder, static_folder=folder)   # параметр - имя модуля для веб-приложения
                        # значение __name__ содержит корректное имя модуля для текущего файла 
                        # в нём будет значение "__main__", если модуль запускается непосредственно
                        # и другое имя, если модуль подключается

app.add_url_rule('/', 'index', index, methods = ["POST", "GET"])   # создаёт правило для URL: 
                                        # при получении GET-запроса на адрес '/' на этом сайте
                                        # будет запускаться функция index (указана третьим параметром)
                                        # и её значение будет ответом на запрос.
                                        # Второй параметр - endpoint, "конечная точка", -
                                        # это строка, которая содержит имя данного правила. 
                                        # Обычно endpoint рекомендуют делать идентичным имени функции, 
                                        # но в сложных приложениях может быть несколько функций с одним именем в разных модулях, 
                                        # и для различения их в пределах всего сайта можно указывать разные endpoint.
app.add_url_rule('/test', 'test', test, methods = ["POST", "GET"]) 
app.add_url_rule('/result', 'result', result)
app.config['SECRET_KEY'] = "Strong_key"
if __name__ == "__main__":
    # Запускаем веб-сервер:
    app.run(host=('192.168.55.224'))
