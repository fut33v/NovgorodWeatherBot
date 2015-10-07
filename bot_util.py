import httplib
import urllib2

__author__ = 'Ilya'

TOKEN_FILENAME = 'token'
PREVIOUS_UPDATE_DATE_FILENAME = 'previous_update_date'


def urlopen(url, data=None):
    try:
        if data is not None:
            urllib2.urlopen(url, data)
        else:
            return urllib2.urlopen(url, data).read()
    except urllib2.HTTPError, e:
        print "HTTPError", e
    except urllib2.URLError, e:
        print "URLError",  e
    except httplib.HTTPException, e:
        print "HTTPException", e
    return None


def read_one_string_file(filename):
    f = open(filename, 'r')
    s = f.read()
    s = s.replace('\n', '')
    s = s.replace('\r', '')
    return s


def read_token():
    return read_one_string_file(TOKEN_FILENAME)


def read_previous_update_date():
    try:
        u = read_one_string_file(PREVIOUS_UPDATE_DATE_FILENAME)
        if u == '':
            return 0
        return int(u)
    except IOError:
        return 0


def write_previous_update_date(d):
    open(PREVIOUS_UPDATE_DATE_FILENAME, 'w').write(str(d))
