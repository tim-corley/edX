import requests
import os

API_KEY = os.environ.get('CURRENCY_API_KEY')

def main():
    currency = input('Currency Code (not EUR): ').upper()
    # get access key here: https://currencylayer.com/
    res = requests.get('http://data.fixer.io/api/latest?access_key={key}&'.format(key=API_KEY),
                        params={'symbols': currency})
    if res.status_code != 200:
        raise Exception('ERROR: API request unsuccessful.')
    data = res.json()
    rate = data['rates'][currency]
    print(f'1 EUR is equal to {rate} {currency}')


if __name__ == '__main__':
    main()
