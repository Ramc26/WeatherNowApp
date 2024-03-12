from flask import Flask, render_template, request
from weather import main as getWeather

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])

def index():
    data=None
    if request.method == 'POST':
        print('hi_')
        city = request.form['cityName']
        state = request.form['stateName']
        country = request.form['countryName']
        data= getWeather(city,state,country)
    return render_template('index.html', data=data)

    

if __name__ == "__main__":
    app.run(debug=True, port=3000)