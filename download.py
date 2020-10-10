from datetime import date, timedelta, datetime
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlretrieve

if __name__ == '__main__':

    outdir = Path('pdf')
    today = datetime.today()
    d = datetime(2020, 3, 15)
    while d < today:
        fname = f'KORONAWIRUS-komunikat-PPIS-{d.strftime("%Y-%m-%d")}.pdf'
        fname2 = f'KORONAWIRUS-Komunikat-PPIS-{d.strftime("%Y-%m-%d")}.pdf'
        outfile = outdir / fname
        outfile2 = outdir / fname2
        if outfile.exists() or outfile2.exists():
            d += timedelta(days=1)
            continue
        url = f'https://www.pssewawa.pl/download/{fname}'
        print(f'Downloading {url}...')
        try:
            urlretrieve(url, str(outfile))
        except HTTPError:
            url = f'https://www.pssewawa.pl/download/{fname2}'
            try:
                urlretrieve(url, str(outfile2))
            except HTTPError:
                with open(str(outfile), 'w'):
                    pass
        d += timedelta(days=1)
