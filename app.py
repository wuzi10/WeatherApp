from flask import Flask, render_template, url_for, request, redirect
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city')
    return redirect(url_for('show_weather', city=city))

@app.route('/weather')
def show_weather():
    city = request.args.get('city')
    return render_template('weather.html', src="http://" + parse(city)[1], result=parse(city)[0], weathercity=city)


def parse(city):
    url = f"https://ua.sinoptik.ua/погода-{city}"
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    t = soup.find("p", class_="today-temp").get_text()
    time = soup.find("p", class_="today-time").get_text()
    descriptions = soup.findAll("div", class_="description")
    desc = ""
    for des in descriptions:
        desc += f'{des.text[1:]}\n'

    image = soup.find("div", class_="img").find('img')['src'][2:]
    infoDay = soup.find("div", class_="infoDaylight").get_text()[1:]
    infoVal = soup.find("p", class_="infoHistoryval").get_text()[1:]
    text = f"{time}\n\nТемпература: {t}\n\n{infoDay}\n\n{infoVal}\n\n{desc}"
    result = [text, image]
    return result

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
