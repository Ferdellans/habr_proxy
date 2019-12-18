from django.contrib import admin
from django.urls import path, include

from habr.views import index

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name="index"),
    path('habr/', include("habr.urls"))
]
