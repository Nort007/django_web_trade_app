from django.forms import ModelForm, Form, ModelChoiceField, Select, NumberInput

from .models import *


class OrderTradeForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'exchange': Select(attrs={'class': 'form-select'}),  # 'readonly': 'readonly'
            'symbol': Select(attrs={'class': 'form-select'}),
            'type': Select(attrs={'class': 'form-select'}),
            'time_in_force': Select(attrs={'class': 'form-select'}),
            'side': Select(attrs={'class': 'form-select'}),
            'price': NumberInput(attrs={'class': 'form-control'}),
            'quantity': NumberInput(attrs={'class': 'form-control'}),
        }


class AccountForm(Form):
    account = ModelChoiceField(queryset=Account.objects.all(), widget=Select(attrs=
                                                                             {'class': 'form-select',
                                                                              'data-ajax-s-url': "/ajax/load-symbols"
                                                                              }))

    """class Meta:
        model = Account
        fields = '__all__'"""

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'