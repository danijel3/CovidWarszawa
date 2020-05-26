import re
from datetime import datetime
from pathlib import Path
from time import strptime, mktime

from tika import parser
import pandas as pd

re_date = re.compile(r'^Stan danych.*w dniu ([0-9.]+)( )?r.')
re_field = re.compile(r'.*(liczba [^/:]*).*:')
re_num = re.compile(r'([0-9]+).*')

if __name__ == '__main__':
    pdfdir = Path('pdf')
    data = {'data': []}
    lres = []
    for file in pdfdir.glob('*.pdf'):
        res = {}
        lines = parser.from_file(str(file))['content'].splitlines()
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
                    if k not in data:
                        data[k] = []

                    v = line[line.find(':') + 1:].strip()
                    if v:
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
