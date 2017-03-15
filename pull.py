import re, json
from datetime import datetime

import requests

name_to_count = {}
for d in [
  {
    'name': "Hex.pm (Elixir/Erlang)",
    'url': "https://hex.pm/packages",
    'regex': ">(\\d+) Results Found"
  },
  {
    'name': "DUB (dlang)",
    'url': "https://code.dlang.org",
    'regex': "<p>Found (\d+) packages.<\/p>"
  },
  {
    'name': "npm (node.js)",
    'url': "https://skimdb.npmjs.com/registry",
    'key': "doc_count"
  },
  {
    'name': "Rubygems.org",
    'url': "https://rubygems.org/stats",
    'regex': "Total gems[^<]*<[^<]*stat__count\">([0-9,]+)<"
  },
  {
    'name': "Drupal (php)",
    'url': "https://www.drupal.org/project/project_module",
    'regex': ">([0-9,]+) Modules match your search"
  },
  {
    'name': "Perl 6 Ecosystem (perl 6)",
    'url': "http://modules.perl6.org/total",
    'regex': "(\\d+)"
  },
  {
    'name': "nuget (.NET)",
    'url': "http://www.nuget.org/stats/totals",
    'key': "UniquePackages"
  },
  {
    'name': "LuaRocks (Lua)",
    'url': "https://luarocks.org/m/root",
    'regex': '<span class="header_count">\((\d+)\)</span>'
  },
  {
    'name': "Packagist (PHP)",
    'url': "http://packagist.org/statistics",
    'regex': "Packages registered<\\/dt>[^>]+>(\\d[^<]+)<\\/dd"
  },
  {
    'name': "Crates.io (Rust)",
    'url': "https://crates.io/summary",
    'key': "num_crates"
  },
  {
    'name': "CRAN (R)",
    'url': "http://cran.r-project.org/web/packages/",
    'regex': "features\\s+([\\d,]+)\\s+available packages"
  },
  {
    'name': "Hackage (Haskell)",
    'url': "http://hackage.haskell.org/packages/.json",
    'is_full_list': True
  },
  {
    'name': "Melpa (Emacs)",
    'url': "http://melpa.milkbox.net/recipes.json",
    'is_full_list': True
  },
  {
    'name': "Maven Central (Java)",
    'url': "http://search.maven.org/quickstats",
    'key': "gaNumber"
  },
  {
    'name': "Clojars (Clojure)",
    'url': "http://clojars.org/projects",
    'regex': "Displaying projects <b>.*</b> of <b>\s*(\d+)\s*</b>\s*</div>"
  },
  {
    'name': "CPAN (search)",
    'url': "http://search.cpan.org",
    'regex': ",\\s+(\\d+)\\sDistributions"
  },
  {
    'name': "PyPI",
    'url': "http://pypi.python.org/pypi",
    'regex': "currently\\s*<strong>([\\d,]+)</strong>\\s*packages"
  }
]:
  name, url, regex, key, is_full_list = (
    d.get('name'), d.get('url'), d.get('regex'), d.get('key'), d.get('is_full_list'))

  print 'getting url:', url

  try:
    resp = requests.get(url, timeout=10)
  except Exception:
    continue

  if is_full_list:
    count = len(json.loads(resp.content))
  elif regex:
    count = re.search(regex, resp.content).group(1)
  else:
    count = json.loads(resp.content).get(key)
  if isinstance(count, basestring):
    count = count.replace(',', '')
    count = re.sub("&#?\w+;", '', count)
  print 'count:', count
  name_to_count[name] = int(count)

out_dict = {'date': datetime.utcnow(), 'name_to_count': name_to_count}

def dt_handler(obj):
  return obj.isoformat() if hasattr(obj, 'isoformat') else obj
out_str = json.dumps(out_dict, default=dt_handler, indent=2) + ',\n'

with open('out.txt', 'a') as f:
  f.write(out_str)
