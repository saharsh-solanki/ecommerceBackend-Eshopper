from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from products.models import *



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    fields = ["image","image_preview"]
    readonly_fields = ('image_preview',)

    def image_preview(self,obj):
        if obj.image:
            return mark_safe(
                '<img src="{0}" width="100" height="100" style="object-fit:contain" />'.format(obj.image.url))
        else:
            return  "(No Image Found)"


class ProductSizeInline(admin.TabularInline):
    fields = ["sizes", "stock","color"]
    model = ProductSize
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductSizeInline]


admin.site.register(Product, ProductAdmin)

admin.site.register(Sizes)
admin.site.register(ProductColors)
admin.site.register(ProductSize)
admin.site.register(ProductImage)
admin.site.register(ProductCategory)