import sys, json, threading, time

import flask

app = flask.Flask(__name__)
port = int(sys.argv[1]) if len(sys.argv) == 2 else 80

class g:
  daily_counts = []

def load_data():
  while True:
    with open('out.txt') as f:
      json_text = f.read()

    g.daily_counts = json.loads('[' + json_text[:-2] + ']')
    time.sleep(60 * 60 * 24)

t = threading.Thread(target=load_data)
t.daemon = True
t.start()

@app.route('/')
def index():
  # TODO: add graph
  return json.dumps(g.daily_counts, indent=2)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=(port != 80))

