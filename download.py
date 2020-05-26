from datetime import date, timedelta, datetime
from pathlib import Path
from urllib.request import urlretrieve

if __name__ == '__main__':

    outdir = Path('pdf')
    today = datetime.today()
    d = datetime(2020, 5, 11)
    while d < today:
        fname = f'KORONAWIRUS-komunikat-PPIS-{d.strftime("%Y-%m-%d")}.pdf'
        outfile = outdir / fname
        if outfile.exists():
            d += timedelta(days=1)
            continue
        url = f'https://www.pssewawa.pl/download/{fname}'
        print(f'Downloading {url}...')
        urlretrieve(url, str(outfile))
        d += timedelta(days=1)
