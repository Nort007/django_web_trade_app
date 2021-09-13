from main_app.services.BinanceAPI import Binance
from typing import List, Dict, Union, Any


def create_order(pub: str, sec: str, params: Dict[str, Union[str, int, float, bool]]) -> Binance:
    return Binance(public_key=pub, secret_key=sec).create_order(params=params).json()


def cancel_order(pub: str, sec: str, params: Dict[str, Union[str, int, float, bool]]) -> Binance:
    return Binance(public_key=pub, secret_key=sec).cancel_order(params=params).json()



def to_dict(items: Dict[str, Union[str, Any]]) -> Dict[str, Union[str, int, float, bool]]:
    keys = []
    values = []
    items = dict(items)
    del items['exchange']

    for key, value in items.items():
        tmp_key = []
        split_key = key.split('_')
        for k in range(len(split_key)):
            if k > 0:
                tmp_key.append(split_key[k][:1].upper() + split_key[k][1:])
            else:
                tmp_key.append(split_key[k])
        keys.append(''.join(tmp_key))
        values.append(value.upper() if value == str(value) else value)
    return dict(zip(keys, values))

