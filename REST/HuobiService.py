# @Author  : Xinzhou Zhao
# @github  : https://github.com/xinzhou5

from HuobiUtil import *

'''
Market data API
'''

# Get KLine


def get_kline(symbol, period, size):
    """
    :param symbol
    :param period: range: {1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year}
    :param size: [1,2000]
    :return:
    """
    params = {'symbol': symbol,
              'period': period,
              'size': size}

    url = MARKET_URL + '/market/history/kline'
    return http_get_request(url, params)


# Get marketdepth
def get_depth(symbol, type):
    """
    :param symbol: 
    :param type: range: { percent10, step0, step1, step2, step3, step4, step5 }
    :return:
    """
    params = {'symbol': symbol,
              'type': type}

    url = MARKET_URL + '/market/depth'
    return http_get_request(url, params)


# Get tradedetail
def get_trade(symbol):
    """
    :param symbol: range: { ethcny }
    :return:
    """
    params = {'symbol': symbol}

    url = MARKET_URL + '/market/trade'
    return http_get_request(url, params)


# Get Market Detail 24hr Transaction Volume Data
def get_detail(symbol):
    """
    :param symbol: range: { ethcny }
    :return:
    """
    params = {'symbol': symbol}

    url = MARKET_URL + '/market/detail'
    return http_get_request(url, params)

# search for all the system supported transaction pairs

def get_symbols():
    """
    :return:
    """
    url = MARKET_URL + '/v1/common/symbols'
    params = {}
    return http_get_request(url, params)

'''
Trade/Account API
'''


def get_accounts():
    """
    :return: 
    """
    path = "/v1/account/accounts"
    params = {}
    return api_key_get(params, path)

ACCOUNT_ID = 0
# Get user's current asset 
def get_balance(acct_id=None):
    """
    :param acct_id
    :return:
    """
    global ACCOUNT_ID
    
    if not acct_id:
        try:
            accounts = get_accounts()
            acct_id = ACCOUNT_ID = accounts['data'][0]['id']
        except BaseException as e:
            print 'get acct_id error.%s' % e
            acct_id = ACCOUNT_ID

    url = "/v1/account/accounts/{0}/balance".format(acct_id)
    params = {"account-id": acct_id}
    return api_key_get(params, url)


# Create and send order
def send_order(amount, source, symbol, _type, price=0):
    """
    :param amount: 
    :param source: 
    :param symbol: 
    :param _type: range: {buy-market, sell-market, buy-limit, sell-limit}
    :param price: 
    :return: 
    """
    try:
        accounts = get_accounts()
        acct_id = accounts['data'][0]['id']
    except BaseException as e:
        print 'get acct_id error.%s' % e
        acct_id = ACCOUNT_ID

    params = {"account-id": acct_id,
              "amount": amount,
              "symbol": symbol,
              "type": _type,
              "source": source}
    if price:
        params["price"] = price

    url = '/v1/order/orders/place'
    return api_key_post(params, url)


# Cancel order 
def cancel_order(order_id):
    """

    :param order_id: 
    :return: 
    """
    params = {}
    url = "/v1/order/orders/{0}/submitcancel".format(order_id)
    return api_key_post(params, url)


# Search for an order
def order_info(order_id):
    """

    :param order_id: 
    :return: 
    """
    params = {}
    url = "/v1/order/orders/{0}".format(order_id)
    return api_key_get(params, url)


# Search for the order detail of an order
def order_matchresults(order_id):
    """

    :param order_id: 
    :return: 
    """
    params = {}
    url = "/v1/order/orders/{0}/matchresults".format(order_id)
    return api_key_get(params, url)


# Get order list
def orders_list(symbol, states, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
    """
    :param symbol: 
    :param states: range {pre-submitted, submitted, partial-filled, partial-canceled, filled, canceled}
    :param types: range {buy-market, sell-market, buy-limit, sell-limit}
    :param start_date: 
    :param end_date: 
    :param _from: 
    :param direct: range{prev, next}
    :param size: 
    :return: 
    """
    params = {'symbol': symbol,
              'states': states}

    if types:
        params[types] = types
    if start_date:
        params['start-date'] = start_date
    if end_date:
        params['end-date'] = end_date
    if _from:
        params['from'] = _from
    if direct:
        params['direct'] = direct
    if size:
        params['size'] = size
    url = '/v1/order/orders'
    return api_key_get(params, url)


# Search for the trade records of an account
def orders_matchresults(symbol, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
    """
    :param symbol: 
    :param types: range {buy-market, sell-market, buy-limit, sell-limit}
    :param start_date: 
    :param end_date: 
    :param _from: 
    :param direct: range {prev, next}
    :param size: 
    :return: 
    """
    params = {'symbol': symbol}
    # direct = "prev"
    if types:
        params[types] = types
    if start_date:
        params['start-date'] = start_date
    if end_date:
        params['end-date'] = end_date
    if _from:
        params['from'] = _from
    if direct:
        params['direct'] = direct
    if size:
        params['size'] = size
    url = '/v1/order/matchresults'
    return api_key_get(params, url)


# Create a Withdraw Request
def withdraw(address, amount, currency, fee=0, addr_tag=""):
    """

    :param address_id: 
    :param amount: 
    :param currency:btc, ltc, bcc, eth, etc ...
    :param fee: 
    :param addr_tag:
    :return: {
              "status": "ok",
              "data": 700
            }
    """
    params = {'address': address,
              'amount': amount,
              "currency": currency,
              "fee": fee,
              "addr-tag": addr_tag}
    url = '/v1/dw/withdraw/api/create'

    return api_key_post(params, url)

# Cancel a Withdraw Request
def cancel_withdraw(address_id):
    """

    :param address_id: 
    :return: {
              "status": "ok",
              "data": 700
            }
    """
    params = {}
    url = '/v1/dw/withdraw-virtual/{0}/cancel'.format(address_id)

    return api_key_post(params, url)


# Place a New Order
def send_margin_order(amount, source, symbol, _type, price=0):
    """
    :param amount: 
    :param source: 'margin-api'
    :param symbol: 
    :param _type: range {buy-market, sell-market, buy-limit, sell-limit}
    :param price: 
    :return: 
    """
    try:
        accounts = get_accounts()
        acct_id = accounts['data'][0]['id']
    except BaseException as e:
        print 'get acct_id error.%s' % e
        acct_id = ACCOUNT_ID

    params = {"account-id": acct_id,
              "amount": amount,
              "symbol": symbol,
              "type": _type,
              "source": 'margin-api'}
    if price:
        params["price"] = price

    url = '/v1/order/orders/place'
    return api_key_post(params, url)

# Transfer Asset from Spot Trading Account to Margin Account
def exchange_to_margin(symbol,currency,amount):
    """
    :param amount: 
    :param currency: 
    :param symbol: 
    :return: 
    """
    params = {"symbol":symbol,
              "currency":currency,
              "amount":amount}

    url = "/v1/dw/transfer-in/margin"
    return api_key_post(params,url)

# Transfer Asset from Margin Account to Spot Trading Account
def margin_to_exchange(symbol,currency,amount):
    """
    :param amount: 
    :param currency: 
    :param symbol: 
    :return: 
    """
    params = {"symbol":symbol,
              "currency":currency,
              "amount":amount}

    url = "/v1/dw/transfer-out/margin"
    return api_key_post(params,url)

# Request a Margin Loan
def get_margin(symbol, currency, amount):
    """
    :param amount: 
    :param currency: 
    :param symbol: 
    :return: 
    """
    params = {"symbol": symbol,
              "currency": currency,
              "amount": amount}
    url = "/v1/margin/orders"
    return api_key_post(params, url)

# Repay Margin Loan
def repay_margin(order_id, amount):
    """
    :param order_id: 
    :param amount: 
    :return: 
    """
    params = {"order-id": order_id,
              "amount": amount}
    url = "/v1/margin/orders/{0}/repay".format(order_id)
    return api_key_post(params, url)

# Search Past Margin Orders
def loan_orders(symbol, currency, start_date="", end_date="", start="", direct="", size=""):
    """
    :param symbol: 
    :param currency: 
    :param direct: prev , next
    :return: 
    """
    params = {"symbol":symbol,
              "currency":currency}
    if start_date:
        params["start-date"] = start_date
    if end_date:
        params["end-date"] = end_date
    if start:
        params["from"] = start
    if direct and direct in ["prev","next"]:
        params["direct"] = direct
    if size:
        params["size"] = size
    url = "/v1/margin/loan-orders"
    return api_key_get(params,url)


#Get the Balance of the Margin Loan Account
def margin_balance(symbol):
    """
    :param symbol: 
    :return: 
    """
    params = {}
    url = "/v1/margin/accounts/balance"
    if symbol:
        params['symbol'] = symbol
    
    return api_key_get(params, url)


if __name__ == '__main__':
    print get_symbols()
