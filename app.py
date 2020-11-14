import json

from flask import Flask, render_template, request

from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import InputRequired, Length

import data
from functions import random_teachers as rt, free_time as ft


class BookingForm(FlaskForm):
    name = StringField("Вас зовут:", [InputRequired(message="Введите имя!")])
    phone = StringField("Ваш телефон:", [Length(min=12, max=12, message="Неправильный формат телефона, убедитесь, "
                                                                        "что вы вводите +7...")])
    submit = SubmitField("Записаться на пробный урок")


class RequestForm(FlaskForm):
    name = StringField("Вас зовут:", [InputRequired(message="Введите имя!")])
    phone = StringField("Ваш телефон:", [Length(min=12, max=12, message="Неправильный формат телефона, убедитесь,"
                                                                        " что вы вводите +7...")])
    time = RadioField("Сколько времени есть?", choices=[("1-2", "1-2 часа в неделю"), ("3-5", "3-5 часов в неделю"),
                                                        ("5-7", "5-7 часов в неделю"), ("7-10", "7-10 часов в неделю")])
    goal = RadioField("Какая цель занятий?", choices=[("work", "Для работы"), ("move", "Для переезда"),
                                                      ("learn", "Для школы"), ("travel", "Для путешествий")])
    submit = SubmitField("Найдите мне преподавателя")


with open("data.json", "w") as f:
    json.dump(data.teachers, f)

app = Flask(__name__)
app.secret_key = 'kukulidi'


@app.route("/")
def render_main():
    random = rt(data.teachers)
    return render_template("index.html", teachers=data.teachers, goals=data.goals, random=random)


@app.route("/goals/<goal>/")
def render_goals(goal):
    return render_template("goals.html", teachers=data.teachers, goal=goal)


@app.route("/teachers/")
def render_teachers():
    return render_template("teachers.html", teachers=data.teachers, goals=data.goals)


@app.route("/profile/<id_teacher>/")
def render_profiles(id_teacher):
    id_t = int(id_teacher)
    time = ft(data.teachers, id_t)
    return render_template("profile.html", teachers=data.teachers, id=id_t, time=time)


@app.route("/request/")
def render_request():
    form = RequestForm()
    return render_template("request.html", form=form)


@app.route("/request_done/", methods=["POST"])
def render_request_done():
    form = RequestForm()
    if request.method == "POST":
        name = form.name.data
        phone = form.phone.data
        time = form.time.data
        goal = form.goal.data
        submit = form.submit.data
        with open("request.json", "r") as r:
            requests = json.load(r)
        requests.append({"goal": goal, "time": time, "name": name, "phone": phone})
        with open("request.json", "w") as w:
            json.dump(requests, w)
        return render_template("request_done.html", name=name, phone=phone, time=time, goal=goal, submit=submit)


@app.route("/booking/<id_teacher>/<day>/<time>/")
def render_booking(id_teacher, day, time):
    form = BookingForm()
    id_t = int(id_teacher)
    return render_template("booking.html", teachers=data.teachers, id=id_t, day=day, time=time, form=form)


@app.route("/booking_done/<day>/<time>/", methods=['POST'])
def render_booking_done(day, time):
    form = BookingForm()
    if request.method == "POST":
        name = form.name.data
        phone = form.phone.data
        with open("booking.json", "r") as r:
            booking = json.load(r)
        booking.append({"day": day, "time": time, "name": name, "phone": phone})
        with open("booking.json", "w") as w:
            json.dump(booking, w)
        return render_template("booking_done.html", day=day, time=time, name=name, phone=phone)


@app.errorhandler(404)
def render_not_found(error):
    return render_template("error.html", error=error), 404


@app.errorhandler(500)
def render_server_error(error):
    return render_template("error.html", error=error), 500


if __name__ == '__main__':
    app.run()
