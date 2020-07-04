import re
from datetime import datetime
from pathlib import Path
from time import strptime, mktime

from tika import parser
import pandas as pd
re_date = re.compile(r'^[ ]*Stan danych.*w dniu ([0-9.]+)( )?r.')
re_field = re.compile(r'^[•].*(liczba [^/:]*).*')
re_num = re.compile(r'[^0-9]*([0-9]+).*')

fix = {
    'liczba osób aktualnie hospitalizowanych z powodu podejrzenia zakażenia COVID-19': 'liczba osób hospitalizowanych z powodu podejrzenia zakażenia COVID-19',
    'liczba osób objętych aktualnie nadzorem epidemiologicznym': 'liczba osób aktualnie objętych nadzorem epidemiologicznym',
    'liczba zgonów w związku z zakażeniem COVID-19': 'liczba zgonów związanych z COVID-19',
    'liczba zgonów powiązanych z COVID-19': 'liczba zgonów związanych z COVID-19',
    'liczba osób objętych aktualnie kwarantanną domową na podstawie decyzji inspektora': 'liczba osób aktualnie objętych kwarantanną domową'}

if __name__ == '__main__':
    pdfdir = Path('pdf')
    data = {'data': []}
    lres = []
    for file in pdfdir.glob('*.pdf'):
        res = {}
        content = parser.from_file(str(file))['content']
        if not content:
            continue
        lines = content.splitlines()
        for ln, line in enumerate(lines):
            if not res:
                m = re_date.match(line)
                if m:
                    res['data'] = datetime.fromtimestamp(mktime(strptime(m.group(1), '%d.%m.%Y')))
            else:
                m = re_field.match(line)
                if m:
                    k = m.group(1).strip()
                    k = ' '.join(k.split())
                    if k in fix:
                        k = fix[k]
                    if k not in data:
                        data[k] = []

                    pos = line.find(':')
                    if pos > 0:
                        v = line[pos + 1:].strip()
                    if pos > 0 and v:
                        res[k] = int(re_num.match(v).group(1))
                    else:
                        v = ' '.join(lines[ln + 1:ln + 3]).strip()
                        res[k] = int(re_num.match(v).group(1))
        lres.append(res)

    for res in lres:
        for k, t in data.items():
            if k in res:
                t.append(res[k])
            else:
                t.append(None)
    df = pd.DataFrame.from_dict(data)
    df.to_pickle('out.pkl')
