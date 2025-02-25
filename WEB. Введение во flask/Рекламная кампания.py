from flask import Flask

app = Flask(__name__)


@app.route('/')
def countdown():
    return "Миссия Колонизация Марса"


@app.route('/index')
def index():
    return 'И на Марсе будут яблони цвести!'


@app.route('/promotion')
def promotion():
    return '''<b>Человечество вырастает из детства.<br>
                Человечеству мала одна планета.<br>
                Мы сделаем обитаемыми безжизненные пока планеты.<br>
                И начнем с Марса!<br>
                Присоединяйся!</b>'''




if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
