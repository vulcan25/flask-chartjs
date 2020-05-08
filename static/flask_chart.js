function getConfig() {
  return {
    type: 'line',
    data: {
      datasets: []
    },
    options: {
      scales: {
        xAxes: [{
          type: 'time',
          time: {
            unit: 'day'
          },
        }, ],
        yAxes: [{
          display: true,
          // type: 'logarithmic',
        }]
      },
      responsive: true
    }
  };
}
////

Array.prototype.convertData = function() {
  /// Function which convers X values to moment object
  for (i = 0; i < this.length; i++) {
    this[i] = {
      'x': moment(this[i].x),
      'y': this[i].y
    }
  }
  return this;
}

function getRandomColor() {
  // Function to generate random color for the lines.
  var letters = '0123456789ABCDEF'.split('');
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

function create_chart(ctx, unit = 'day') {

  config = getConfig()

  // Set unit
  config.options.scales.xAxes[0].time.unit = unit;

  // Assign endpoint from 'data-endpoint' attrib to config object
  config.endpoint = ctx.dataset.endpoint;

  return new Chart(ctx.getContext('2d'), config);
}

function load_data(chart, q = false) {

  var url = new URL("http://" + window.location.host + chart.config.endpoint),
    params = {
      'q': q
    }

  // If q is provided, add this to the URL
  if (q != false) {
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
  }

  // Run the API call.
  fetch(url)
    .then((response) => {
      return response.json();
    })
    .then((resp_data) => {

      // Push this data to the config object of this chart.
      resp_data.datasets.forEach((dataSet) => {
        chart.data.datasets.push({
          label: dataSet['title'],
          data: dataSet['data'].convertData(),
          fill: false,
          backgroundColor: getRandomColor(),
        })
      });

      // Finally update that visual chart
      chart.update();

    });
};