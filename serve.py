import sys, json, threading, time, os

import flask

import config

app = flask.Flask(__name__)
port = int(sys.argv[1]) if len(sys.argv) == 2 else 80

class g:
  daily_counts = []

def load_data():
  while True:
    with open(os.path.expanduser(config.config_dict['out_path'])) as f:
      json_text = f.read()

    g.daily_counts = json.loads('[' + json_text[:-2] + ']')
    time.sleep(60 * 60 * 24)

t = threading.Thread(target=load_data)
t.daemon = True
t.start()

@app.route('/')
def index():
  return flask.render_template('index.html')

@app.route('/daily_counts')
def daily_counts():
  print 'daily_counts:', g.daily_counts[0]
  return flask.jsonify(g.daily_counts)


@app.route('/voronoi_test')
def voroni_test():
  return flask.render_template('voronoi_test.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=(port != 80))

