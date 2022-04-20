from django.contrib import admin

from data_services.models import AirtelProductList, Category, ProductList

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
class ProductAdmin(admin.ModelAdmin):    
    list_display = ('category','product_code','quantity','name','price')
    
class AirtelProductAdmin(admin.ModelAdmin):    
    list_display = ('product_code','quantity','name','price')
    
    

admin.site.register(Category,CategoryAdmin)
admin.site.register(ProductList,ProductAdmin)
admin.site.register(AirtelProductList,AirtelProductAdmin)