from django.contrib import admin

from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "user",
        "rating",
        "created_at",
        "updated_at",
    )
    search_fields = ("product__name", "user__username", "comment")
    list_filter = ("product", "rating", "created_at")

    list_filter = []


admin.site.register(Review, ReviewAdmin)
