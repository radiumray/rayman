from django.contrib import admin
from dbUsersModel.models import userInfo, Contact, Tag

# Register your models here.

admin.site.register([userInfo, Contact, Tag])


# class ContactAdmin(admin.ModelAdmin):
#     fields = ('name', 'email')

# admin.site.register(Contact, ContactAdmin)
# admin.site.register([userInfo, Tag])