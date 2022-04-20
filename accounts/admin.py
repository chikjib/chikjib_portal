from django.contrib import admin
from django.contrib.auth.models import User
from accounts.models import Profile
from django.contrib.auth.admin import UserAdmin


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'get_wallet_balance', 'is_staff')
    list_select_related = ('profile', )
    search_fields = ['username','email']
    
    def get_wallet_balance(self,instance):
        return "N" + str(instance.profile.wallet_balance)
    get_wallet_balance.short_description = "Wallet Balance"

    # def get_profile_picture(self, instance):
    #     return mark_saf('<img src="%s" width="100px" height="100px" />' % (instance.profile.profile_picture.url))
    # get_profile_picture.short_description = 'Profile Picture'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
    

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
