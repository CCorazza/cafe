from flask import Flask, render_template, redirect, url_for
import arrow

app = Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')


def get_coffee_time():
    try:
        with open('next_coffee') as fd:
            next_coffee_stamp = fd.read()
        next_coffee = arrow.get(next_coffee_stamp)
    except:
        set_coffee_time(4242)
        return get_coffee_time()
    return next_coffee.to('Europe/Paris')


def set_coffee_time(hour, minute=None):
    if (minute is None):
        next_coffee = arrow.get(hour)
    else:
        next_coffee = arrow.now('Europe/Paris').replace(hour=hour, minute=minute, second=0)
    with open("next_coffee", 'w+') as fd:
        fd.write(str(next_coffee.timestamp))


@app.route("/")
def index_view():
    coffee_time = get_coffee_time().to('local')
    now = arrow.now('Europe/Paris')
    humanized = coffee_time.humanize(now, locale='fr_FR')
    coffee_time = coffee_time.format("HH:mm:ss")
    now = now.format("HH:mm:ss")
    return render_template('index.jade', **locals())

@app.route("/set/<int:hour>:<int:minute>")
def set_view(hour, minute):
    set_coffee_time(hour, minute)
    return redirect(url_for('index_view'))

application = app

if __name__ == "__main__":
        app.run(debug=True)
