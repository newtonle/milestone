from flask import Flask, render_template, request, redirect, url_for
from bokeh.plotting import figure
from bokeh.charts import TimeSeries
from bokeh.embed import components


app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(port=33507)
