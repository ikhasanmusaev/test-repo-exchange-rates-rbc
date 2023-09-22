from django.urls import include, path
from rest_framework.routers import DefaultRouter

from exchange_rates.views import RatesListAPIView, UserCurrencyAPIView, CurrencyListAPIView

router = DefaultRouter()
router.register('currency', CurrencyListAPIView, 'currency')

urlpatterns = [
    path('currency/user_currency/', UserCurrencyAPIView.as_view()),
    # path('currency/', .as_view()),
    path('rates/', RatesListAPIView.as_view()),
    path('', include(router.urls)),
]
