from tronpy import Tron, Contract
from tronpy.keys import PrivateKey
 
priv_key = '42eeb9093d499c9b16f29fc344bb18471851c514df9450e8cbb1f2d540944281'
tron = Tron.generate_address(priv_key)
print("tron is ", tron)
update = tron.update()
print("update is ", update)

balance = Tron()
balance = balance.get_account("TSx6R1UYoJ8g3o2o62wrfii8pg6WYrgqeK").get("balance")
print("balance is ", balance)
import requests

def trx_to_usdt(trx_amount):
    # Binance API endpoint for getting the current TRX to USDT exchange rate
    endpoint = 'https://api.binance.com/api/v3/ticker/price'
    
    # Query parameters for the TRX/USDT trading pair
    params = {'symbol': 'TRXUSDT'}
    
    try:
        # Sending GET request to Binance API
        response = requests.get(endpoint, params=params)
        data = response.json()
        
        # Extracting the current price of TRX in USDT
        trx_usdt_price = float(data['price'])
        
        # Calculating the equivalent amount of USDT
        usdt_amount = trx_amount * trx_usdt_price
        return usdt_amount
    
    except Exception as e:
        print("Error:", e)
        return None

# Example usage
trx_amount = float(balance) # Amount of TRX to convert
usdt_equivalent = trx_to_usdt(trx_amount)
if usdt_equivalent is not None:
    print(f"{trx_amount} TRX is equivalent to {usdt_equivalent:.4f} USDT")

