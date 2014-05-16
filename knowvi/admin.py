from django.contrib import admin
from knowvi.models import Category, Page, PageAdmin, UserProfile

admin.site.register(Category)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
