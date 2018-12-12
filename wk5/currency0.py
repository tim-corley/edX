import requests
import os

API_KEY = os.environ.get('CURRENCY_API_KEY')

def main():
    # get access key here: https://currencylayer.com/
    url = 'http://data.fixer.io/api/latest?access_key={key}&symbols=USD'.format(key=API_KEY)
    res = requests.get(url)
    if res.status_code != 200:
        raise Exception('ERROR: API request unsuccessful.')
    data = res.json()
    print(data)

if __name__ == "__main__":
    main()
