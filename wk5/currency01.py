import requests
import os

API_KEY = os.environ.get('CURRENCY_API_KEY')

def main():
    # get access key here: https://currencylayer.com/
    url = 'http://data.fixer.io/api/latest?access_key={key}'.format(key=API_KEY)
    res = requests.get(url)
    if res.status_code != 200:
        raise Exception('ERROR: API request unsuccessful.')
    data = res.json()
    rate = data['rates']['USD']
    print(f'1 EUR is equal to {rate} USD')

if __name__ == '__main__':
    main()
