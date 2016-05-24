from flask import Flask, render_template, request, redirect, url_for
from bokeh.plotting import figure
from bokeh.charts import TimeSeries
from bokeh.embed import components
import pandas as pd
import requests
import os
import datetime

#api_key = os.environ['API_KEY']
api_key = 'PzaxdxNpHYtDUFzSuMbk'
app = Flask(__name__)
app.jinja_env.autoescape = False

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/graph', methods=['POST'])
def graph():
  # Get form info
  ticker = request.form['ticker'].upper()
  features = request.form.getlist('features')
  print features
  
  now = datetime.datetime.now()
  start_date = (now + datetime.timedelta(-30)).strftime('%Y-%m-%d')
  end_date = now.strftime('%Y-%m-%d')
  api_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s/data.json?api_key=%s&start_date=%s&end_date=%s' % (ticker, api_key, start_date, end_date)
  session = requests.Session()
  session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))
  raw_data = session.get(api_url)
  
  temp_df = pd.DataFrame(raw_data.json())
  
  df = pd.DataFrame(data=temp_df['dataset_data']['data'],columns=temp_df['dataset_data']['column_names'])
  
  print df

  plot = TimeSeries(df,
              title='Data from Quandle WIKI set for ' + ticker,
              x='Date', y=features, legend=True)

  script, div = components(plot)
  return render_template('graph.html', script=script, div=div, ticker=ticker)


if __name__ == '__main__':
  app.run(port=33507, debug=True)
