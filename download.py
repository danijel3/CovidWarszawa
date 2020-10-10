from datetime import date, timedelta, datetime
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlretrieve


def fnames(d: datetime):
    return [f'KORONAWIRUS-komunikat-PPIS-{d.strftime("%Y-%m-%d")}.pdf',
            f'KORONAWIRUS-Komunikat-PPIS-{d.strftime("%Y-%m-%d")}.pdf',
            f'KORONAWIRUS-komunikat-PPIS-{d.strftime("%Y-%m-%d")}-.pdf',
            f'KORONAWIRUS-komunikat-PPIS-{d.strftime("%Y-%m-%d")}-k.pdf',
            f'KORONAWIRUS-komunikat-PPIS--{d.strftime("%Y-%m-%d")}.pdf']


if __name__ == '__main__':

    outdir = Path('pdf')
    today = datetime.today()
    d = datetime(2020, 3, 15)
    while d < today:
        found = False
        for fname in fnames(d):
            outfile = outdir / fname
            if outfile.exists():
                found = True
                break
            url = f'https://www.pssewawa.pl/download/{fname}'
            try:
                urlretrieve(url, str(outfile))
                print(f'Downloaded {url}...')
                found = True
                break
            except HTTPError:
                continue
        if not found:
            with open(str(outdir / fnames(d)[0]), 'w'):
                pass
        d += timedelta(days=1)
