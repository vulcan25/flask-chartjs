from flask import Flask, render_template, jsonify, url_for, request

import datetime as DT
def conv(epoch):
    """ helper function convers epoch to iso format compatible with moment """
    return DT.datetime.utcfromtimestamp(epoch).isoformat()

sample_csv = '''2020-05-05,103
                2020-05-06,143
                2020-05-07,184
                2020-05-08,244
                2020-05-09,280
                2020-05-10,324
                2020-05-11,387
                2020-05-12,491
                2020-05-13,645
                2020-05-14,925'''

sample_list = [ {'x': conv(1588745371), 'y': 400},
                {'x': conv(1588845371), 'y': 500},
                {'x': conv(1588946171), 'y': 800}]

def csv_to_points(data):
    """ Convert CSV string to list of dictionaries compatible with chart data obj """
    data = data.split('\n')
    data = [d.split(',') for d in data]
    return [ dict(x = d[0], y = d[1]) for d in data]

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

                {'title': 'From CSV',
                 'data': csv_to_points(sample_csv)
                }
            ],
        }

    return jsonify(d)

@app.route('/dynamic')
def dynamic():
    """ This route is an example of receiving data from the frontend """

    q = request.args.get('q')

    print (q)

    # You could dynamically build the following result now
    # based on the value of `q` which is passed from the frontend.
    # Here we just set that to the title.

    d = {'datasets':
            [
                {'title': q,
                 'data': sample_list,
                },
            ],
        }

    return jsonify(d)
