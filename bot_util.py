import httplib
import urllib2

__author__ = 'Ilya'

TOKEN_FILENAME = 'token'
PREVIOUS_UPDATE_DATE_FILENAME = 'previous_update_date'


def urlopen(url, data=None):
    try:
        if data is not None:
            urllib2.urlopen(url, data)
            return True
        else:
            return urllib2.urlopen(url, data).read()
    except urllib2.HTTPError, e:
        print "HTTPError", e
    except urllib2.URLError, e:
        print "URLError",  e
    except httplib.HTTPException, e:
        print "HTTPException", e
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


def read_token():
    return read_one_string_file(TOKEN_FILENAME)


def read_previous_update_date():
    u = read_one_string_file(PREVIOUS_UPDATE_DATE_FILENAME)
    if u == '' or None == u:
        return 0
    return int(u)


def write_previous_update_date(d):
    open(PREVIOUS_UPDATE_DATE_FILENAME, 'w').write(str(d))
