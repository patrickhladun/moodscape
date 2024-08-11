from django.contrib import admin
from .models import Category, Product
from django.urls import reverse
from django_summernote.admin import SummernoteModelAdmin
from django.utils.safestring import mark_safe


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
      'name', 
      'slug',
    )
    prepopulated_fields = {'slug': ('name',)}

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ProductAdmin(SummernoteModelAdmin):

    list_display = (
      'display_featured',
      'product_name',
      'sku',
      'price',
      'category',
      'created_at',
      'updated_at',
      'is_draft',
    )

    summernote_fields = ('details',)

    def display_featured(self, obj):
        if obj.featured:
            return mark_safe('<img src="%s" width="28" />' % obj.featured.url)
        else:
            default_image_url = "/static/assets/images/avatar.png"
            return mark_safe('<img src="%s" width="28" />' % default_image_url)

    def product_name(self, obj):
        url = reverse(
            "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.model_name),
            args=[obj.id],
        )
        return mark_safe('<a href="{}">{}</a>'.format(url, obj.name))

    display_featured.allow_tags = True
    display_featured.short_description = "Image"

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('-updated_at',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)