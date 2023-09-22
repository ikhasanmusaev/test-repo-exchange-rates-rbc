from django.urls import include, path

from djangoProject.settings import LOCAL_APPS

# Apps urls

# Variant 1
# urlpatterns = [path(f'{x}/', include((f'{x}.urls', f'{x}'), f'{x}'))
#                for x in LOCAL_APPS]

urlpatterns = [
    path('', include('exchange_rates.urls'), ),
    path('user/', include('users.urls', )),
]
