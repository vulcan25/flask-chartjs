from flask import Flask, render_template, jsonify, url_for, request

import datetime as DT

def conv(date_str):
    """ helper function convers epoch to iso format compatible with moment """
    return DT.datetime.strptime(date_str, '%m-%d-%Y').isoformat()

dates = ['01-02-2020', '02-02-2020', '03-03-2020']
prices = [1.4, 2.5, 9.6]

sample_list =[dict(x=conv(date), y=prices[idx]) for idx,date in enumerate(dates)]

app = Flask(__name__)

# Disable caching of staic assets; useful for dev
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1

@app.route('/')
def index():
    ''' Route which renders the chart page.  Pass the endpoint which returns jsonified data '''
    return render_template('index.html', CHART_ENDPOINT = url_for('data'))

@app.route('/data')
def data():
    ''' Endpoint which returns jsonified data '''

    d = {'datasets':
            [
                {'title': 'From Dict',
                 'data': sample_list,
                },
            ],
        }

    return jsonify(d)
