from django.db import models


class Exchange(models.Model):
    """Добавление биржи."""
    exchange_name = models.CharField(max_length=35)

    def __str__(self):
        return "{}".format(self.exchange_name)


class ExchangeType(models.Model):
    """Добавление типа биржи и соответсвенно типа ключа АПИ."""
    exchange_type = models.CharField(max_length=35, null=True)

    def __str__(self):
        return "{}".format(self.exchange_type)


class Account(models.Model):
    """Добавление инфрмации об аккаунте."""
    exchange = models.ForeignKey(Exchange, max_length=35, null=True, on_delete=models.SET_NULL, verbose_name='(Exchange) Биржа')
    account_type = models.ForeignKey(ExchangeType, max_length=35, null=True, on_delete=models.SET_NULL, verbose_name='(Account type) Тип аккаунта')
    email = models.EmailField(max_length=250, null=True, verbose_name='(Email) Почта')
    user = models.CharField(max_length=250, null=True, verbose_name='(User) Пользователь')
    key_public = models.CharField(max_length=250, null=True, verbose_name='(Key Public) Публичный ключ')
    key_secret = models.CharField(max_length=250, null=True, verbose_name='(Key Private) Приватный ключ')

    def __str__(self):
        return '{}: {} ({}) {}'.format(self.pk, self.user, self.account_type, self.exchange)


class Pairs(models.Model):
    """Добавление к биржам пары криптовалют."""
    exchange = models.ForeignKey(Exchange, max_length=20, null=True, on_delete=models.SET_NULL)
    #ymbol_type = models.ForeignKey(ExchangeType, max_length=20, null=True, on_delete=models.SET_NULL)
    pair = models.CharField(max_length=20, null=True, verbose_name='(Symbol) Символ')

    def __str__(self):

        return '{}'.format(self.pair)


class OrderType(models.TextChoices):
    """Все типы ордера. Param: type."""
    LIMIT = "limit"
    MARKET = "market"
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"
    LIMIT_MAKER = "limit_maker"
    STOP_LOSS_LIMIT = "stop_loss_limit"
    TAKE_PROFIT_LIMIT = "take_profit_limit"
    STOP = "STOP"
    STOP_MARKET = "stop_market"
    TAKE_PROFIT_MARKET = "take_profit_market"
    TRAILING_STOP_MARKET = "trailing_stop_market"


class TIF(models.TextChoices):
    """Param: timeInForce."""
    GTC = "gtc"
    FOK = "fok"
    IOC = "ioc"


class Side(models.TextChoices):
    """Param: side."""
    SIDE_BUY = "buy"
    SIDE_SELL = "sell"


class Order(models.Model):
    """Основные(все) параметры  биржи для ордера"""
    exchange = models.ForeignKey(Exchange, null=True, on_delete=models.SET_NULL)
    symbol = models.ForeignKey(Pairs, null=True, on_delete=models.SET_NULL)
    type = models.CharField(choices=OrderType.choices, null=True, max_length=25)
    time_in_force = models.CharField(choices=TIF.choices, null=True, max_length=25)
    side = models.CharField(choices=Side.choices, null=True, max_length=25)
    price = models.DecimalField(max_digits=30, decimal_places=8, null=True, blank=True)
    quantity = models.DecimalField(max_digits=30, decimal_places=8, null=True, blank=True)

    '''def __str__(self):
        return '{}: {}'''


class Wallet(models.Model):
    account = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    btc = models.FloatField(null=True)
    eth = models.FloatField(null=True)
    usdt = models.FloatField(null=True)

    def __str__(self):
        return "{}".format(self.account)


class OpenOrders(models.Model):
    date = models.FloatField()
    order_id = models.IntegerField(null=True)
    pair = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    side = models.CharField(max_length=64)
    fills = models.CharField(max_length=64, null=True)
    price = models.FloatField()
    quantity = models.FloatField()
    total = models.FloatField(null=True)
    status = models.CharField(max_length=64, null=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)