import requests

chains = requests.get ('https://sandbox.tradier.com/v1/markets/history?symbol=SPX',
                       headers={'Authorization': 'Bearer llAjglmAKANHiAxgxPg32bl5l7rI', 'Accept': 'application/json'}
                       )

json_chains = chains.json ()
print (chains.status_code)
print(json_chains)

