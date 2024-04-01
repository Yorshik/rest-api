from flask import Flask, render_template, jsonify
from requests import get

from data.db_session import global_init
from data import jobs_api
from data import users_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/users_show/<int:user_id>')
def index(user_id):
    cur_user = get(f'http://localhost:5000/api/users/{user_id}').json()
    if cur_user['status'] != 200:
        return jsonify(
            {
                'error': 'User not Found',
                'status': 404
            }
        )
    geocode = get(f'https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&'
                  f'format=json&geocode={cur_user["user"]["city"]}')
    if not geocode:
        return jsonify(
            {
                'error': str(geocode.status_code) + ' ' + geocode.request
            }
        )
    js = geocode.json()
    toponym = js["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    ll = ','.join(toponym['Point']['pos'].split())
    req = get(f'http://static-maps.yandex.ru/1.x/?l=sat&ll={ll}&z=11')
    if not req:
        return jsonify(
            {
                'error': str(req.status_code) + ' ' + req.reason,
                'status': req.status_code,
                'url': req.url
            }
        )
    with open('static/img/map.png', 'wb') as img:
        img.write(req.content)
    return render_template('users_show.html', city=cur_user['user']['city'],
                           name=f"{cur_user['user']['name']} {cur_user['user']['surname']}")


if __name__ == '__main__':
    global_init("db/db.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run('127.0.0.1', 5000)