import re
import requests
from django.http import HttpResponse
from django.shortcuts import redirect
from bs4 import BeautifulSoup
from django.views.generic.base import View

SYMBOL = "™"


def index(request):
    return redirect('/habr')


class Habr(View):
    @staticmethod
    def post(request):
        return redirect('/habr')

    @staticmethod
    def get(request):
        r = requests.get("https://habr.com/")
        if r.status_code != 200:
            return redirect('/habr')

        html = ReplaceContent(r).get_html
        return HttpResponse(html)


class HabrPost(View):
    @staticmethod
    def post(request):
        return redirect('/habr')

    @staticmethod
    def get(request):
        url = request.GET.get('url', None)
        if url is None:
            return redirect('/habr')

        r = requests.get(url)
        if r.status_code != 200:
            return redirect('/habr')

        html = ReplaceContent(r).get_html
        return HttpResponse(html)


class ReplaceContent(object):
    soup = None

    def __init__(self, r):
        self.r = r

    @property
    def get_html(self) -> BeautifulSoup:
        self.__do_parse()
        return self.soup.prettify()

    def __do_parse(self):
        soup = BeautifulSoup(self.r.content, "html.parser")
        for a in soup.find_all("a"):
            try:
                a['href'] = f'/habr/post/?url={a["href"]}'
                a['target'] = str()
            except KeyError:
                continue

        for tag in soup.find_all(text=True):
            try:
                tag.string.replace_with(self._replace_word(tag))
            except AttributeError:
                continue
        self.soup = soup

    @staticmethod
    def _replace_word(text) -> str:

        words = re.split(r"[\s\.,\?]+", text)
        for word in words:
            if len(word) == 6:
                text = text.replace(word, word + SYMBOL)
        return text
