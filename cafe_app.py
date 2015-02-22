from flask import Flask, render_template, redirect, url_for
import arrow

app = Flask(__name__)

@app.route("/")
def index():
        with open('next_coffee') as fd:
                next_coffee_stamp = fd.read()
        del fd
        next_coffee = arrow.get(next_coffee_stamp)
        now = utcnow()
        when = next_coffee.humanize(now)
        return render_template('index.html', *locals())

@app.route("/set/<when>")
def set_next_coffee(when):
        next_coffee = arrow.get(when)
        with open("next_coffe") as fd:
                fd.write(next_coffee.timestamp)
        del fd
        return redirect(url_for('index'))



application = app

if __name__ == "__main__":
        app.run()
