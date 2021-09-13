import hashlib
import hmac
import time
from urllib.parse import urlencode

import requests

# Simple support binance rest api


class Binance:
    """
    General class with mandatory params API or FAPI pub. and secret key.
    public_key=pub_val, secret_key=secret_val
    """

    def __init__(self, public_key, secret_key):
        self.PUBLIC_KEY = public_key
        self.SECRET_KEY = secret_key
        self.BASE_URL = "https://api.binance.com"  # BASE URL
        self.BASE_URL_FAPI = "https://fapi.binance.com"
        self.recv = True

    def return_api_keys(self):
        return "{} - {}".format(self.PUBLIC_KEY, self.SECRET_KEY)

    def sha256(self, data):
        return hmac.new(self.SECRET_KEY.encode('utf-8'), data.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

    def server_time(self):
        url_path = "/api/v3/time"
        return self.public_api_query("GET", url_path)

    def get_timestamp(self):
        return int(time.time() * 1000)

    def _request(self, method, url, headers):
        response = requests.request(method, url, headers=headers)

        return response

    def private_api_query(self, method, url_path, payload: dict = None, fapi=False):
        headers = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-MBX-APIKEY': self.PUBLIC_KEY
        }
        if self.recv is True:
            payload.update(recvWindow=10000)
        payload = urlencode(sorted(payload.items()))

        if payload:

            payload = f"{payload}&timestamp={self.get_timestamp()}"

        else:
            payload = f"timestamp={self.get_timestamp()}"
        if fapi is True:
            full_url = self.BASE_URL_FAPI + url_path + '?' + payload + '&signature=' + self.sha256(payload)
        else:

            full_url = self.BASE_URL + url_path + '?' + payload + '&signature=' + self.sha256(payload)

        print(full_url)
        return self._request(method, full_url, headers)

    def public_api_query(self, method, url_path, payload={}, fapi=False):
        headers = {
            'Content-Type': 'application/json;charset=utf-8'
        }
        payload = urlencode(sorted(payload.items()))
        if fapi is True:
            full_url = self.BASE_URL_FAPI + url_path + '?' + payload
        else:
            full_url = self.BASE_URL + url_path + '?' + payload
        # return full_url
        return self._request(method, full_url, headers)

    def create_order(self, params):
        """
        symbol 	            STRING 	YES\n
        side 	            ENUM 	YES\n
        type 	            ENUM 	YES\n
        timeInForce         ENUM 	NO\n
        quantity 	        DECIMAL NO (If limit - YES)\n
        quoteOrderQty 	    DECIMAL NO\n
        price 	            DECIMAL NO (If limit - YES)\n
        newClientOrderId 	STRING 	NO\n
        stopPrice 	        DECIMAL NO\n
        icebergQty 	        DECIMAL NO\n
        newOrderRespType 	ENUM 	NO\n
        recvWindow 	        LONG 	NO\n
        timestamp 	        LONG 	YES
        """
        url_path = '/api/v3/order'
        return self.private_api_query('POST', url_path, params)

    def cancel_order(self, params):
        """
        MANDATORY:\n
        symbol 	            STRING 	YES\n
        orderId 	        LONG 	YES\n
        origClientOrderId   STRING 	NO\n
        newClientOrderId    STRING 	NO\n
        recvWindow 	        LONG 	NO\n
        timestamp 	        LONG 	YES\n
        """
        url_path = '/api/v3/order'
        return self.private_api_query('DELETE', url_path, params)

    def cancel_all_orders(self, **kwargs):
        url_path = '/api/v3/openOrders'
        return self.private_api_query('DELETE', url_path, kwargs)

    def query_order(self, **params):
        """
        MANDATORY:\n
        * symbol 	            STRING 	YES\n
        * orderId 	            LONG 	NO\n
        * origClientOrderId 	STRING 	NO\n
        * recvWindow 	        LONG 	NO\n
        * timestamp 	        LONG 	YES\n
        """
        url_path = "/api/v3/order"
        return self.private_api_query('GET', url_path, params)

    def open_orders(self, **kwargs):
        # active, canceled, filled orders
        url_path = '/api/v3/openOrders'
        return self.private_api_query('GET', url_path, kwargs)

    def get_account_info(self, url_path='/api/v3/account'):
        return self.private_api_query('GET', url_path)

    def current_open_orders(self, **kwargs):
        """
        MANDATORY:\n
        * symbol 	    STRING 	NO\n
        * recvWindow 	LONG 	NO\n
        * timestamp 	LONG 	YES\n
        """
        url_path = '/api/v3/openOrders'
        return self.private_api_query('GET', url_path)

    def query_margin_acc_open_orders(self, **kwargs):
        url_path = '/sapi/v1/margin/openOrders'
        return self.private_api_query('GET', url_path, kwargs)

    def order_book(self, **params):
        """
        symbol 	STRING 	YES\n
        limit 	INT 	NO 	(Default 100)\n
        params = {'symbol': 'YFIBTC', 'limit': 5-100}
        """
        url_path = "/api/v3/depth"
        p = params
        return self.public_api_query('GET', url_path, p)

    def account_trade_list(self, **params):
        """
        MANDATORY:\n
        * symbol - YES\n
        * stratTime - NO\n
        * endTime - NO\n
        * fromId - NO\n
        * limit - NO (default 500, max 1000)\n
        * recWindow - NO\n
        * timestamp - YES
        """
        url_path = "/api/v3/myTrades"
        return self.private_api_query('GET', url_path, params)

    def all_orders(self, **params):
        """
        symbol 	    STRING 	YES\n
        orderId 	LONG 	NO\n
        startTime 	LONG 	NO\n
        endTime 	LONG 	NO\n
        limit 	    INT 	NO 	Default 500; max 1000.\n
        recvWindow 	LONG 	NO\n
        timestamp 	LONG 	YES\n
        """
        url_path = "/api/v3/allOrders"
        return self.private_api_query('GET', url_path, params)

    def candlestick_data(self, **params):
        """
        **symbol** 	    STRING 	YES\n
        **interval** 	ENUM 	YES\n
        **startTime** 	LONG 	NO\n
        **endTime** 	LONG 	NO\n
        **limit** 	INT 	NO 	Default 500; max 1000.\n
        -------------------\n
        Example:
            [\n
            1613656800000, // Open time [0]\n
            "0.13813000", // Open[1]\n
            "0.14000000", // High[2]\n
            "0.12882000", // Low[3]\n
            "0.13318000", // Close[4]\n
            "12167135.1", // Volume[5]\n
            1613660399999, // Close time[6]\n
            "1626878.46196500", // Quote asset[7]\n
            4835, // Numb of trade[8]\n
            "3637996.5", // Taker buy base asset vol[9]\n
            "491470.141585", // Taker buy quote asset vol[10]\n
            "0" // Ignore[11]\n
            ]
        """
        url_path = "/api/v3/klines"
        return self.public_api_query('GET', url_path, params)

    def test_connctivity(self):

        url_path = "/api/v3/ping"
        return self.public_api_query("GET", url_path)

    def ticker_price_change_statisrics24h(self, **params):
        """
        symbol: YES/NO
        """
        url_path = "/api/v3/ticker/24hr"
        return self.public_api_query("GET", url_path, params)

    def fapi_balance(self):
        url_path = "/fapi/v2/balance"
        return self.private_api_query("GET", url_path, fapi=True)

    def fapi_order_book(self, **params):
        url_path = "/fapi/v1/depth"
        return self.public_api_query("GET", url_path, params, fapi=True)

    def fapi_new_order(self, **params):
        url_path = "/fapi/v1/order"
        return self.private_api_query("POST", url_path, params, fapi=True)

    def fapi_query_order(self, **params):
        url_path = "/fapi/v1/order"
        return self.private_api_query("GET", url_path, params, fapi=True)

    def fapi_all_orders(self, **params):
        url_path = "/fapi/v1/allOrders"
        return self.private_api_query("GET", url_path, params, fapi=True)

    def fapi_current_all_open_orders(self, **params):
        '''
        "/fapi/v1/openOrders"
        https://binance-docs.github.io/apidocs/futures/en/#current-all-open-orders-user_data
        '''
        url_path = "/fapi/v1/openOrders"
        return self.private_api_query("GET", url_path, params, fapi=True)

    def fapi_query_current_order(self, **params):
        '''
        "/fapi/v1/openOrder"
        https://binance-docs.github.io/apidocs/futures/en/#query-current-open-order-user_data
        '''
        url_path = "/fapi/v1/openOrder"
        return self.private_api_query("GET", url_path, params, fapi=True)

    def fapi_position_info_v2(self, **params):
        url_path = "/fapi/v1/positionRisk"
        return self.private_api_query("GET", url_path, params, fapi=True)

    def fapi_klines(self, **params):
        url_path = "/fapi/v1/klines"
        return self.public_api_query("GET", url_path, params, fapi=True)

    def fapi_exchange_info(self, **params):
        url_path = "/fapi/v1/exchangeInfo"
        return self.public_api_query("GET", url_path, params, fapi=True)

    def fapi_cancel_all_orders(self, **params):
        url_path = "/fapi/v1/allOpenOrders"
        return self.private_api_query("DELETE", url_path, params, fapi=True)

    def fapi_account_balance(self, **params):
        url_path = "/fapi/v2/balance"
        return self.private_api_query("GET", url_path, params, fapi=True)

    def fapi_listen_key(self, **params):
        url_path = "/fapi/v1/listenKey"
        return self.private_api_query("POST", url_path, params, fapi=True)

    def fapi_keepalive_key(self, **params):
        url_path = "/fapi/v1/listenKey"
        return self.private_api_query("PUT", url_path, params, fapi=True)

    def fapi_close_key(self, **params):
        url_path = "/fapi/v1/listenKey"
        return self.private_api_query("DELETE", url_path, params, fapi=True)

    def fapi_aggregate_trade_list(self, **params):
        url_path = "/fapi/v1/aggTrades"
        return self.public_api_query("GET", url_path, params, fapi=True)

    def fapi_server_time(self):
        url_path = "/fapi/v1/time"
        return self.public_api_query("GET", url_path, fapi=True)
