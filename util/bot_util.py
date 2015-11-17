from functools import partial
import httplib
import json
import os
import urllib
import urllib2

__author__ = 'Ilya'


def urlopen(url, data=None):
    try:
        if data is not None:
            data = urllib.urlencode(data)
            urllib2.urlopen(url, data)
            return True
        else:
            return urllib2.urlopen(url, data).read()
    except urllib2.HTTPError as e:
        print "HTTPError", e, url, data
    except urllib2.URLError as e:
        print "URLError", e, url, data
    # except httplib.HTTPException as e:
    #     print "HTTPException", e
    return False


def read_one_string_file(filename):
    try:
        f = open(filename, 'r')
        s = f.read()
        s = s.replace('\n', '')
        s = s.replace('\r', '')
        return s
    except IOError:
        return None


def check_file_for_string(filename, string):
    if not os.path.exists(filename):
        return True
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        if line == string:
            return False
    return True


def create_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_json_file(filename):
    json_f = open(filename, 'r')
    j = json_f.read()
    json_f.close()
    json_obj = json.loads(j)
    return json_obj


json_pretty_dumps = partial(
    json.dumps,
    sort_keys=True,
    indent=4,
    separators=(',', ': ')
)


def save_json_file(filename, data):
    json_txt = json_pretty_dumps(data)
    json_f = open(filename, 'w')
    json_f.write(json_txt)
    json_f.close()
