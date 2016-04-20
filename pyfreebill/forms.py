# Copyright 2013 Mathias WOLFF
# This file is part of pyfreebilling.
#
# pyfreebilling is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfreebilling is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfreebilling.  If not, see <http://www.gnu.org/licenses/>

from django import forms
from django.utils.translation import ugettext_lazy as _

from datetimewidget.widgets import DateTimeWidget

from pyfreebill.models import Company, RateCard, LCRGroup

class CDRSearchForm(forms.Form):
    """VoIP call Report Search Parameters"""
    dateTimeOptions = {
        'format': 'yyyy-dd-mm hh:ii',
        'todayBtn': 'true',
        'usetz': 'true',
        'usel10n': 'true',
        'usei18n': 'true'
    }
    from_date = forms.CharField(label=_('From'), required=False, max_length=20,
        widget=DateTimeWidget(options=dateTimeOptions))
    to_date = forms.CharField(label=_('To'), required=False, max_length=20,
        widget=DateTimeWidget(options=dateTimeOptions))
    customer_id = forms.ChoiceField(label=_('Customer'), required=False)
    provider_id = forms.ChoiceField(label=_('Provider'), required=False)
    ratecard_id = forms.ChoiceField(label=_('Customer Ratecard'), required=False)
    lcr_id = forms.ChoiceField(label=_('LCR Group'), required=False)
    dest_num = forms.IntegerField(label=_('Destination Number'), required=False,
        help_text=_('Enter the full number or the first part'))

    def __init__(self, user, *args, **kwargs):
        super(CDRSearchForm, self).__init__(*args, **kwargs)
        # Customer list
        cust_list = []
        cust_list.append((0, _('all').upper()))
        customer_list = Company.objects.values_list('id', 'name')\
                    .filter(customer_enabled='true')\
                    .order_by('name')

        for i in customer_list:
            cust_list.append((i[0], i[1]))

        self.fields['customer_id'].choices = cust_list

        # Provider list
        prov_list = []
        prov_list.append((0, _('all').upper()))
        provider_list = Company.objects.values_list('id', 'name')\
                    .filter(supplier_enabled='true')\
                    .order_by('name')

        for i in provider_list:
            prov_list.append((i[0], i[1]))

        self.fields['provider_id'].choices = prov_list

        # Customer Ratecard list
        cratec_list = []
        cratec_list.append((0, _('all').upper()))
        cratecard_list = RateCard.objects.values_list('id', 'name')\
                    .order_by('name')

        for i in cratecard_list:
            cratec_list.append((i[0], i[1]))

        self.fields['ratecard_id'].choices = cratec_list

        # LCR Group list
        lcrg_list = []
        lcrg_list.append((0, _('all').upper()))
        lcrgroup_list = LCRGroup.objects.values_list('id', 'name')\
                    .order_by('name')

        for i in lcrgroup_list:
            lcrg_list.append((i[0], i[1]))

        self.fields['lcr_id'].choices = lcrg_list








class CustomerRateCardsAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'description': forms.TextInput(attrs={"class": "input-medium"}),

        }





class CompanyAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'max_calls': forms.TextInput(attrs={"class": "input-small"}),
            'calls_per_second': forms.TextInput(attrs={"class": "input-small"}),
            'credit_limit': forms.TextInput(attrs={"class": "input-small"}),
        }
