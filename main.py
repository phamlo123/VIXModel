from DataProcessing import options_chain

options_chain("AMD")



expirations = requests.get ('https://sandbox.tradier.com/v1/markets/options/expirations',
                            params={'symbol': 'SPX', 'includeAllRoots': 'true', 'strikes': 'false'},
                            headers={'Authorization': 'Bearer llAjglmAKANHiAxgxPg32bl5l7rI',
                                     'Accept': 'application/json'}
                            )
expirations_json = expirations.json ()
print (expirations.status_code)
print (expirations_json)
