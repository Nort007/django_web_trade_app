from django.contrib import admin

from .models import (Exchange,
                     ExchangeType,
                     Account,
                     Pairs,
                     Order,
                     Wallet,
                     OpenOrders)


class PairsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Pair Information",
         {
             "fields": [
                 "pair",
                 "exchange",
             ]
         }
         ),
    ]
    list_display = ('pair', 'exchange',)
    list_filter = ('pair', 'exchange',)


class AccountAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Account Information (Информация об аккаунте).",
         {
             "fields": [
                 "exchange",
                 "account_type",
                 "email",
                 "user",
                 "key_public",
                 "key_secret",
             ]
         }
         ),
    ]
    list_display = ('exchange', 'account_type', 'email', 'user', 'key_public', 'key_secret',)
    list_filter = ('user', 'exchange',)


class WalletAdmin(admin.ModelAdmin):
    list_display = ('account', 'btc', 'eth', 'usdt')


admin.site.site_header = 'Bizz'
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Order)
admin.site.register(Exchange)
admin.site.register(ExchangeType)
admin.site.register(Pairs, PairsAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(OpenOrders)