import requests
import csv
cookies = {
    'GUEST_LANGUAGE_ID': 'de_DE',
}

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'dnt': '1',
    'sec-gpc': '1',
}


# Note: original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".

def download_grants():
    session = requests.session()

    # create jsp search
    params = (
        ('actionMode', 'searchlist'),
    )
    data = {
        'suche.detailSuche': 'false',
        'suche.schnellSuche': '*Blockchain*',
        'submitAction': 'Schnellsuche starten'
    }
    response = session.post('https://foerderportal.bund.de/foekat/jsp/SucheAction.do', headers=headers, params=params,
                             cookies=cookies, data=data)
    # fetch csv list
    response = session.get(
        'https://foerderportal.bund.de/foekat/jsp/SucheAction.do?actionMode=print&presentationType=csv',
        headers=headers, cookies=cookies)
    return response.text

if __name__ == "__main__":
    data = list(csv.DictReader(download_grants().splitlines(), delimiter=';', escapechar='=', quotechar='"', doublequote=True))
    print(data[0].keys())
    print(data[0])