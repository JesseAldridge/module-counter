import re, json, time, traceback, sys
from datetime import datetime

import requests

def pull_all(testing):
  name_to_count = {}

  with open('trackers.json') as f:
    trackers_str = f.read()
  tracker_dicts = json.loads(trackers_str)
  if testing:
    tracker_dicts = tracker_dicts[:2]

  for d in tracker_dicts:
    try:
      pull_count(name_to_count, **d)
    except Exception as e:
      print (u'exception: {}; {}'.format(type(e).__name__, e.message)).encode('utf8')
      traceback.print_exc()
      continue

  out_dict = {'date': datetime.utcnow(), 'name_to_count': name_to_count}

  def dt_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj
  out_str = json.dumps(out_dict, default=dt_handler, indent=2) + ',\n'

  with open('out.txt', 'a') as f:
    f.write(out_str)

def pull_count(name_to_count, name=None, url=None, regex=None, key=None, is_full_list=None):
  print 'getting url:', url
  resp = requests.get(url, timeout=10)

  if is_full_list:
    count = len(json.loads(resp.content))
  elif regex:
    count = re.search(regex, resp.content).group(1)
  else:
    count = json.loads(resp.content).get(key)
  if isinstance(count, basestring):
    count = count.replace(',', '')
    count = re.sub("&#?\w+;", '', count)
  name_to_count[name] = int(count)
  print 'count:', count

if __name__ == '__main__':
  while True:
    testing = (sys.platform == "darwin")
    pull_all(testing)
    time.sleep(1 if testing else 60 * 60 * 24)
