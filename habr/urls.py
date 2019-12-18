from django.urls import path
from habr.views import Habr, HabrPost

urlpatterns = [
    path('', Habr.as_view(), name="habr_index"),
    path('post/', HabrPost.as_view(), name='habr_post')
]
