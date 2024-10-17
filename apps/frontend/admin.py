from django.contrib import admin
from .models import ContactMessage, FAQ, FAQSection


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "message", "created_at")


class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "section", "created_at")


class FAQSectionAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")


admin.site.register(FAQ, FAQAdmin)
admin.site.register(FAQSection, FAQSectionAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
