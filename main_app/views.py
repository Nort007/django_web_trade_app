from django.shortcuts import render, redirect, HttpResponseRedirect
# from .models import OpenOrders
# from .filters import OrderFilter
from .forms import *
from .services.service import *


def dashboard_page(request):
    return render(request, 'main_app/dashboard.html', {'general_form': 'general_form'})


def trade_view(request):  # create order
    account = AccountForm(request.POST or None)
    order_trade_form = OrderTradeForm(request.POST or None)
    open_order_obj = OpenOrders.objects.all()
    context = {'account': account, 'orderTradeForm': order_trade_form, 'OpenOrderObj': open_order_obj}
    if request.method == 'POST':
        account = AccountForm(request.POST or None)
        if order_trade_form.is_valid() and account.is_valid():
            key = account.cleaned_data['account']
            params_dict = to_dict(order_trade_form.cleaned_data.items())
            order = create_order(pub=key.key_public, sec=key.key_secret, params=params_dict)
            insert = OpenOrders(date=order['transactTime'], pair=order['symbol'], type=order['type'],
                                side=order['side'], price=order['price'], quantity=order['origQty'],
                                order_id=order['orderId'], status=order['status'], account_id=account.cleaned_data['account'].id)
            insert.save()
            open_order_obj = OpenOrders.objects.all()
            context.update({'respondOrder': 'respond_order', 'OpenOrderObj': open_order_obj})

            return HttpResponseRedirect('/trade')
    return render(request, 'main_app/trade.html', context=context)


def cancel_trade(request, event_id):
    account = Account.objects.all()
    if request.method == 'GET':
        open_order = OpenOrders.objects.get(pk=event_id)

        print(open_order.order_id)
        key = {
            "key_public": Account.objects.get(pk=open_order.account_id).key_public,
            "key_secret": Account.objects.get(pk=open_order.account_id).key_secret,
        }
        client = Binance(public_key=key['key_public'], secret_key=key['key_secret'])
        cancel = client.cancel_order({'orderId': open_order.order_id, 'symbol': open_order.pair})
        open_order.delete()
        return redirect('trade')


def load_symbols(request):
    account_id = request.GET.get('symbol')
    exchange_id = Account.objects.get(pk=account_id).exchange.id
    keys = [Account.objects.get(pk=account_id).key_public, Account.objects.get(pk=account_id).key_secret]
    symbols = Pairs.objects.filter(exchange_id=exchange_id)
    return render(request, 'main_app/dropdown_list_symbols.html', {'symbols': symbols})
