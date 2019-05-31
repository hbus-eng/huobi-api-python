# @Author  : Xinzhou Zhao
# @github  : https://github.com/xinzhou5

from HuobiUtil import *
from helper import update

'''
 Common API
'''

# search for all the system supported transaction pairs
def get_symbols():
    """
    :return:
    """
    url = MARKET_URL + '/v1/common/symbols'
    return publicReq(url, 'GET')

def getCurrencies():
    url = MARKET_URL + '/v1/common/currencys'
    return publicReq(url, 'GET')

def getTimestamp():
    url = MARKET_URL + '/v1/common/timestamp'
    return publicReq(url, 'GET')

'''
Market data API
'''

# Get KLine
def get_kline(symbol, period, size=None):
    """
    :param symbol
    :param period: range: {1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year}
    :param size: [1,2000]
    :return:
    """
    params = {'symbol': symbol,
              'period': period}

    update(params, {'size': size})

    url = MARKET_URL + '/market/history/kline'
    return publicReq(url, 'GET', params=params)

# Get latest ticker with some important 24h aggregated market data
def get_merged_detail(symbol):
    """
    :param symbol: range: { ethusdt }
    :return:
    """
    params = {'symbol': symbol}

    url = MARKET_URL + '/market/detail/merged'
    return publicReq(url, 'GET', params=params)

# Get marketdepth
def get_depth(symbol, type, depth=None):
    """
    :param symbol:
    :param type: range: { percent10, step0, step1, step2, step3, step4, step5 }
    :return:
    """
    params = {'symbol': symbol,
              'type': type}
    update(params, {'depth': depth})
    url = MARKET_URL + '/market/depth'
    return publicReq(url, 'GET', params=params)


# Get tradedetail
def get_trade(symbol):
    """
    :param symbol: range: { ethusdt }
    :return:
    """
    params = {'symbol': symbol}

    url = MARKET_URL + '/market/trade'
    return publicReq(url, 'GET', params=params)


# Get Market Detail 24hr Transaction Volume Data
def get_detail(symbol):
    """
    :param symbol: range: { ethcny }
    :return:
    """
    params = {'symbol': symbol}

    url = MARKET_URL + '/market/detail'
    return publicReq(url, 'GET', params=params)

def get_hist_trades(symbol, size=None):
    """
    :param symbol: range: { ethcny }
    :return:
    """
    params = {'symbol': symbol}
    update(params, {'size': size})

    url = MARKET_URL + '/market/history/trade'
    return publicReq(url, 'GET', params=params)

'''
Account API
'''

def get_accounts():
    """
    :return:
    """
    url = TRADE_URL + "/v1/account/accounts"
    return privateReq(url, 'GET')

# Get user's current asset
def get_balance(acct_id=None):
    """
    :param acct_id
    :return:
    """
    if not acct_id:
        try:
            accounts = get_accounts()
            acct_id = accounts['data'][0]['id']
        except BaseException as e:
            print 'get acct_id error.%s' % e

    url = TRADE_URL + "/v1/account/accounts/{0}/balance".format(acct_id)
    return privateReq(url, 'GET')

'''
Trade API
'''

# Create and send order
def send_order(amount, symbol, _type, price=0):
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

    params = {"account-id": acct_id,
              "amount": amount,
              "symbol": symbol,
              "type": _type,
              "source": 'api'}
    if price:
        params["price"] = price

    url = TRADE_URL + '/v1/order/orders/place'
    return privateReq(url, 'POST', data=params)


# Cancel order
def cancel_order(order_id):
    """

    :param order_id:
    :return:
    """
    url = TRADE_URL + "/v1/order/orders/{0}/submitcancel".format(order_id)
    return privateReq(url, 'POST')

def batch_cancel_order(order_ids):
    params = {'order-ids': order_ids}
    url = TRADE_URL + '/v1/order/orders/batchcancel'

    return privateReq(url, 'POST', data=params)

# Search for an order
def order_info(order_id):
    """
    :param order_id:
    :return:
    """
    url = TRADE_URL + '/v1/order/orders/{0}'.format(order_id)
    return privateReq(url, 'GET')


# Search for the order detail of an order
def order_matchresults(order_id):
    """
    :param order_id:
    :return:
    """
    url = TRADE_URL + '/v1/order/orders/{0}/matchresults'.format(order_id)
    return privateReq(url, 'GET')

# Search for the trade records of an account
def orders_matchresults(symbols=None, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
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
    params = {}
    optional = {'symbols': symbols, 'types': types, 'start_date': start_date, 'end_date': end_date, 'from': _from, 'direct': direct, 'size': size}

    update(params, optional)

    url = TRADE_URL + '/v1/order/matchresults'
    return privateReq(url, 'GET', params=params)

# Get order list
def orders_list(states, symbols=None, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
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

    params = {'states': states}
    optional = {'symbols': symbols, 'types': types, 'start-date': start_date, 'end-date': end_date, 'from': _from, 'direct': direct, 'size': size}

    update(params, optional)
    url = TRADE_URL + '/v1/order/orders'
    return privateReq(url, 'GET', params=params)

'''
Wallet API
'''
# Search deposit withdraw records
def dwTx(currency, _type, from_id, size):
    url = TRADE_URL + '/v1/query/deposit-withdraw'
    params = {
        'currency': currency,
        'type': _type,
        'from': from_id,
        'size': size
    }
    return privateReq(url, 'GET', params=params)

# Create a Withdraw Request
def withdraw(address, amount, currency, fee=None, addr_tag=None):
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
              "currency": currency}
    optional = {"fee": fee,
              "addr-tag": addr_tag}

    update(params, optional)
    url = TRADE_URL + '/v1/dw/withdraw/api/create'

    return privateReq(url, 'POST', data=params)

# Cancel a Withdraw Request
def cancel_withdraw(address_id):
    """

    :param address_id:
    :return: {
              "status": "ok",
              "data": 700
            }
    """
    url = TRADE_URL + '/v1/dw/withdraw-virtual/{0}/cancel'.format(address_id)

    return privateReq(url, 'POST')

if __name__ == '__main__':
    print get_symbols()
