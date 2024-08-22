from django.contrib import admin
from .models import Order, OrderLineItem

class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('order_number', 'created_at', 'order_total', 'grand_total', 'shipping_cost')

    fields = (
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'address_line_1',
        'address_line_2',
        'town_city',
        'postcode',
        'country',
        'county',
        'order_total',
        'shipping_cost',
        'grand_total')

    list_display = ('order_number', 'created_at', 'first_name', 'order_total', 'shipping_cost', 'grand_total')

    ordering = ('-created_at',)

admin.site.register(Order, OrderAdmin)
