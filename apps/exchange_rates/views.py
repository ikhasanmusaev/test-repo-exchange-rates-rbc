from django.db.models import Max, Min
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics, mixins
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from exchange_rates.models import DailyRate, UserCurrency, Currency
from exchange_rates.serializers import RateSerializers, UserCurrencySerializers, CurrencySerializer, \
    CurrencyAnalyseSerializer


class RatesListAPIView(generics.ListAPIView):
    queryset = DailyRate.objects.all()
    serializer_class = RateSerializers
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['value', 'currency__num_code']
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination

    @swagger_auto_schema(
        operation_description="Description: List of only latest rates.",
        manual_parameters=[
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="The ordering param, [value, -value]",
                type=openapi.TYPE_STRING,
            ), ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.filter_queryset(super().get_queryset())
        last_date = queryset.first().date
        return queryset.filter(date=last_date)


class CurrencyListAPIView(mixins.ListModelMixin, GenericViewSet):  # Для разнообразия
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Всем вернутся только свои Отслеживаемые КВ",
        manual_parameters=[
            openapi.Parameter(
                'date_from',
                openapi.IN_QUERY,
                description="Filter date_from",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'date_to',
                openapi.IN_QUERY,
                description="Filter date_to",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
    )
    @action(["GET", ], detail=True, permission_classes=[IsAuthenticated])
    def analytics(self, request, pk):
        currency = self.get_object()
        date_from = request.GET.get('date_from', None)
        date_to = request.GET.get('date_to', None)
        rates = DailyRate.objects.filter(currency=currency, date__range=[date_from, date_to])
        min_max_rates = rates.aggregate(max_rate=Max('value'), min_rate=Min('value'))
        serializer = CurrencyAnalyseSerializer(rates, many=True,
                                               context={'request': self.request, 'min_max_rates': min_max_rates})
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Description: Все КВ",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserCurrencyAPIView(generics.CreateAPIView, generics.ListAPIView):
    queryset = UserCurrency.objects.all()
    serializer_class = UserCurrencySerializers
