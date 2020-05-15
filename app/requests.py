import requests





def get_quote():
    quotes_url='http://quotes.stormconsultancy.co.uk/random.json'
    fetch = requests.get(quotes_url)
    get_quotes = fetch.json()

    return get_quotes






