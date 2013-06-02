import httplib
import urllib
from StringIO import StringIO
from lxml import etree
from lxml.etree import fromstring
from lxml.cssselect import CSSSelector

username = ""
password = ""

login_url = "/icok/LoginCheck.action"
balance_url = "/icok/MvnoPakiety.action"
host = "icok.cyfrowypolsat.pl"

HEADERS = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "Connection": "keep-alive"}


def fix_html(html):
    """
    Returns fixed HTML.

    :param html:
    :return:
    """
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)
    return etree.tostring(tree.getroot(), pretty_print=True, method="html")


def login(username, password):
    """
    Returns cookie with session id if authentication is successful.

    :param username:
    :param password:
    :return:
    """
    params = urllib.urlencode({'login': username, 'password': password, 'Zaloguj': ''})
    conn = httplib.HTTPSConnection(host)
    conn.request("POST", login_url, params, HEADERS)
    response = conn.getresponse()
    return response.getheader('set-cookie')


def get_balance_request(cookie):
    """
    Returns body of the website with balance information.

    :param cookie:
    :return:
    """
    headers = HEADERS.copy()
    headers.update({"Cookie": cookie})
    conn = httplib.HTTPSConnection(host)
    conn.request("GET", balance_url, {}, headers)
    response = conn.getresponse()
    return response.read()


def print_balance(html):
    """
    Prints current balance and expiration date.

    :param html:
    """
    sel = CSSSelector('table.cpIcokInfo')
    h = fromstring(fix_html(html))
    print sel(h)[0][1][0][1][0].tail, sel(h)[0][1][0][2][0].tail


cookie = login(username, password)
balance_site = get_balance_request(cookie)
print_balance(balance_site)
