from flask import Flask, render_template, request, redirect, url_for
from bokeh.plotting import figure
from bokeh.charts import TimeSeries
from bokeh.embed import components
import pandas as pd
import requests
import os
import datetime

api_key = os.environ['API_KEY']
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
  
  if len(features) == 0:
    return render_template('graph.html', div='Please check at least one feature.')

  # Get the current date
  now = datetime.datetime.now()

  # Go back one month to get the start date
  start_date = (now + datetime.timedelta(-30)).strftime('%Y-%m-%d')

  # Today is the end date
  end_date = now.strftime('%Y-%m-%d')
  api_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s/data.json?api_key=%s&start_date=%s&end_date=%s' % (ticker, api_key, start_date, end_date)
  session = requests.Session()
  session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))
  raw_data = session.get(api_url)

  # Temporary data frame to parse out data and column names
  temp_df = pd.DataFrame(raw_data.json())
  
  # Some error checking
  if 'dataset_data' not in temp_df:
    return render_template('graph.html', div='Quandl error. Incorrect ticker input?')
  
  df = pd.DataFrame(data=temp_df['dataset_data']['data'],columns=temp_df['dataset_data']['column_names'])
  
  # Plot the data given the features checked by the user
  plot = TimeSeries(df,
              title='Data from Quandle WIKI set for ' + ticker,
              x='Date', y=features, legend=True)

  script, div = components(plot)
  return render_template('graph.html', script=script, div=div, ticker=ticker)


if __name__ == '__main__':
  app.run(port=33507)
