#! /usr/bin/env python
# ================== USE CONDA ==================
from bs4 import BeautifulSoup
import requests
import argparse
import functools
import re

# ------------------------- Argumentos do script -------------------------
# Copied from 'https://github.com/jarun/googler'
# Start GooglerArgumentParser
class MyArgumentParser(argparse.ArgumentParser):
    # Type guards
    @staticmethod
    def positive_int(arg):
        """Try to convert a string into a positive integer."""
        try:
            n = int(arg)
            assert n > 0
            return n
        except (ValueError, AssertionError):
            raise argparse.ArgumentTypeError('%s is not a positive integer' % arg)

    @staticmethod
    def nonnegative_int(arg):
        """Try to convert a string into a nonnegative integer."""
        try:
            n = int(arg)
            assert n >= 0
            return n
        except (ValueError, AssertionError):
            raise argparse.ArgumentTypeError('%s is not a non-negative integer' % arg)

    @staticmethod
    def is_duration(arg):
        """Check if a string is a valid duration accepted by Google.

        A valid duration is of the form dNUM, where d is a single letter h
        (hour), d (day), w (week), m (month), or y (year), and NUM is a
        non-negative integer.
        """
        try:
            if arg[0] not in ('h', 'd', 'w', 'm', 'y') or int(arg[1:]) < 0:
                raise ValueError
        except (TypeError, IndexError, ValueError):
            raise argparse.ArgumentTypeError('%s is not a valid duration' % arg)
        return arg

    @staticmethod
    def is_date(arg):
        """Check if a string is a valid date/month/year accepted by Google."""
        if re.match(r'^(\d+/){0,2}\d+$', arg):
            return arg
        else:
            raise argparse.ArgumentTypeError('%s is not a valid date/month/year; '
                                             'use the American date format with slashes')
# End GooglerArgumentParser

parser = MyArgumentParser(description='Faz um web scrapping')
addarg = parser.add_argument
addarg('-dp', '--dump-html', dest='dump_html', action='store_true',
    help='Se deve jogar o html da página pega'
)
addarg('-d', '--debug', dest='debug', action='store_true',
    help='Se deve habilitar prints de debug'
)
addarg('-ps', '--pg-start', dest='pg_start', type=parser.nonnegative_int, default=0,
    metavar='N', help='Começa busca no N-ézimo resultado'
)
addarg('-pc', '--pg-count', dest='pg_num', type=parser.positive_int,
    default=10, metavar='N', help='Número de resultados máximos (padrão 10)'
)
addarg('search_keywords', metavar='KEYWORD', type=str, nargs='+',
    help='Palavras chave para realizar a busca'
)
addarg('-t', '--time', dest='duration', type=parser.is_duration,
       metavar='dN', help='Em até quanto tempo atrás buscar resultado. Deve ser em inglês a sigla [h5 (5 horas), d5 (5 dias), w5 (5 semanas), m5 (5 mêses), y5 (5 anos)]')
addarg('--from', dest='from_t', type=parser.is_date,
    help="data/mês/ano inicial do intervalo de datas; deve usar o formato de data americano com barras, por exemplo, 24/02/2020, 20/02/2020, 2020; pode ser usado em conjunto com --to, e substitui -t, --time"
)
addarg('--to', dest='to_t', type=parser.is_date,
    help='data/mês/ano final do intervalo de datas; veja --from'
)
parsed_args = parser.parse_args()
# ------------------------- Argumentos do script -------------------------


# ------------------------- Configuração de pesquisa -------------------------
URL = 'https://www.google.com/search'

HEADERS = {
	'Accept' : '*/*',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
}
# ------------------------- Configuração de pesquisa -------------------------

# ------------------------- Configurações de Debug -------------------------
def debug(func):
    def wrap(*args, **kwargs):
        if parsed_args.debug:
            res = func(*args, **kwargs)
            return res
    return wrap

@debug
def debug_print(*args, **kwargs):
    print('DEBUG: --------------------------')
    print(*args, **kwargs)
    print('DEBUG: --------------------------')

# ------------------------- Configurações de Debug -------------------------

def build_parameters():
    param = {
        'q': ' '.join(parsed_args.search_keywords),
        # Coloquei 'uk' para ter os mesmos resultados no browser e na saida do script
        'gl': 'uk',
    }

    # 10 é padrão, não precisa colocar
    if parsed_args.pg_num != 10:
        param['num'] = parsed_args.pg_num
    # 0 é padrão, não precisa colocar
    if parsed_args.pg_start != 0:
        param['start'] = parsed_args.pg_start

    # Adaptado de https://github.com/jarun/googler
    # Argumento 'duration', 'from_t' e 'to_t' já vem no formato aceito pelo Google
    if parsed_args.duration:
        param['tbs'] = f'qdr:{parsed_args.duration}'

    if parsed_args.from_t or parsed_args.to_t:
        cd_min = parsed_args.from_t or ''
        cd_max = parsed_args.to_t or ''
        param['tbs'] = f'cdr:1,cd_min:{cd_min},cd_max:{cd_max}'

    debug_print(f'{param=}')
    return param

class OrganicResults:
    def __init__(self, title, url, site_name, date, details):
        self.title = title
        self.url = url
        self.site_name = site_name
        self.date = date
        self.details = details

    def __repr__(self):
        a  = f'Title: {self.title}\n'
        a += f'\t{self.site_name=}\n'
        a += f'\t{self.url=}\n'
        a += f'\t{self.date=}\n'
        a += f'\t{self.details=}'
        return a

    @staticmethod
    def parse(html_og_result):
        # O atributo data-snhf ajuda a dizer qual parte dos ados estamos utilizando
        # Para achar eu explorei o código html de retorno
        info_p0 = html_og_result.select_one('div.yuRUbf')
        info_p1 = html_og_result.select_one('div[data-sncf="1"]')

        title = info_p0.find('h3').get_text()
        url = info_p0.find('a')['href']
        # Achei qual classes deve ser explorando o html retornado
        site_name = info_p0.select_one('span.VuuXrf').get_text()

        # Mesma coisa, explorei o html e achei esse caminho para pegar a data
        date = info_p1.select_one('span.LEwnzc.Sqrs4e')
        if date != None:
            date = date.get_text()

        # Mesma coisa, explorei o html e achei esse caminho para pegar os detalhes
        # Precisa do 'div > ...', pois se não tiver ele pode pegar oustros spans
        # dentro do span quem tem a data
        details = info_p1.select_one('div > span:not(.LEwnzc.Sqrs4e)')
        if details == None:
            # Pode acontecer de o texto estar diretamente na div (caso do reddit)
            details = info_p1.get_text()
        else:
            details = details.get_text()

        # debug_print(f'{title=}\n{url=}\n{site_name=}\n{date=}\n{details=}')
        return OrganicResults(title, url, site_name, date, details)

if __name__ == "__main__":
    parameters = build_parameters()
    req1 = requests.get(URL, headers = HEADERS, params = parameters)
    debug_print(f'{req1.url=}')
    # Sai se requesição não for 200 (OK)
    req1.raise_for_status()

    soup = BeautifulSoup(req1.text, 'html.parser')

    # Explicando esse CSS selector:
    #   #search: busca pelos elementos dentro do elemento que tiver o id 'search'
    #   div.g.Ww4FFb.vt6azd.tF2Cxc.asEBEc: toda div com essa tag contém os links
    #       úteis para a query. Qualuqer coisa que não tenha essa classe é informação
    #       extra, como vídeos e tals. Achei isso usando o googler(GoogleParser.parse)
    #       e explorando o html de retorno
    organic_searches = soup.select('#search div.g.Ww4FFb.vt6azd.tF2Cxc.asEBEc')
    organic_results = [OrganicResults.parse(val) for val in organic_searches]
    for og_res in organic_results:
        print(og_res, end='\n\n')

