Usage
=====

You can have one route which renders the page containing the chart:
```
@app.route('/')
def index():
    return render_template('index.html', CHART_ENDPOINT = url_for('data'))
```
`CHART_ENDPOINT` in this case will be `/data` which corresponds to another route which returns the JSON.  I also have a helper function which converts epoch times to a ISO 8601 compatible format, which works with moment.
```
import datetime as DT
def conv(epoch):
    return DT.datetime.utcfromtimestamp(epoch).isoformat()

@app.route('/data')
def data():
    d = {'datasets':
            [
                {'title': 'From Dict',
                 'data': [ {'x': conv(1588745371), 'y': 400},
                           {'x': conv(1588845371), 'y': 500},
                           {'x': conv(1588946171), 'y': 800} ]
                },
            ]
         }

    return jsonify(d)
```
Now in the template you can place the chart's canvas element with `data-endpoint` attribute:

    <canvas id="canvas" data-endpoint='{{CHART_ENDPOINT}}'></canvas>

Then I've implemented two JS functions which in that same template allow you to create the chart, and load the data from the previous endpoint:

```
<script type='text/javascript'>
    var ctx = document.getElementById('canvas');

    myChart = create_chart(ctx);

    window.onload = function () { 
      load_data(myChart)
    };
</script>
```
In the `create_chart` function the endpoint is obtained from the `data-endpoint` attrib, and added to the `config` object before it is assigned to that chart [(credit)](https://stackoverflow.com/a/44840756/2052575):

>     config.endpoint = ctx.dataset.endpoint;
>     return new Chart(ctx.getContext('2d'), config);

---

You can also set the [time units](https://www.chartjs.org/docs/latest/axes/cartesian/time.html#time-units) when creating the chart:

    myChart = create_chart(ctx, 'hour') # defaults to 'day'

I've found this usually needs to be tweaked depending on your data range.

It would be trivial to modify that code to obtain this in the same manner as the endpoint, within the `create_chart` function.  Something like `config.options.scales.xAxes[0].time.unit = ctx.datasets.unit` if the attribute was `data-unit`.  This could also be done for other variables.

---
You can also pass a string from the frontend when loading data (say `dynamicChart` is another chart, created with the method above):

    load_data(dynamicChart, 'query_string')

This would make `query_string` available in the flask function as `request.args.get('q')`

This is useful if you want to implement (for example) a text input field which sends the string to the backend, so the backend can process it somehow and return a customised dataset which is rendered on the chart.  The `/dynamic` route in the repo kind of demonstrates this.

Here's what it looks like rendered:

[![rendered chart][1]][1]

As you can see it's possible then to have multiple charts on one page also.

  [1]: https://i.stack.imgur.com/c6ABc.png
