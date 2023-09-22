from rest_framework import serializers

from exchange_rates.models import DailyRate, Currency, UserCurrency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = [
            'id',
            'id_cbr',
            'num_code',
            'char_code',
            'name',
        ]


class CurrencyAnalyseSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(read_only=True)
    is_threshold_exceeded = serializers.SerializerMethodField(read_only=True)
    threshold_match_type = serializers.SerializerMethodField(read_only=True)
    percentage_ratio = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DailyRate
        fields = [
            'id',
            'currency',
            'nominal',
            'value',
            'date',
            'is_threshold_exceeded',  # логическое значение, отвечающим на вопрос, превысила ли котировка ПЗ
            'threshold_match_type',
            'percentage_ratio',
        ]

    def get_is_threshold_exceeded(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            user_currency = UserCurrency.objects.get(user=user, currency=obj.currency)
            return user_currency.threshold < obj.value / obj.nominal  # я тут не уверень.
            # До коцна не понял логику порога. Может наоборот  last_rate.nominal / last_rate.value
        else:
            return None

    def get_threshold_match_type(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            user_currency = UserCurrency.objects.get(user=user, currency=obj.currency)
            if user_currency.threshold < obj.value / obj.nominal:
                return 'less'
            if user_currency.threshold > obj.value / obj.nominal:
                return 'equal'
            return 'exceeded'
        else:
            return None

    def get_percentage_ratio(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            user_currency = UserCurrency.objects.get(user=user, currency=obj.currency)
            return (obj.value / obj.nominal) / user_currency.threshold * 100
        else:
            return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        min_value = self.context['min_max_rates']['min_rate']
        max_value = self.context['min_max_rates']['max_rate']
        representation['is_min_value'] = True if min_value == instance.value else False
        representation['is_max_value'] = True if max_value == instance.value else False
        return representation


class RateSerializers(serializers.ModelSerializer):
    currency = CurrencySerializer(read_only=True)

    class Meta:
        model = DailyRate
        fields = [
            'id',
            'currency',
            'nominal',
            'value',
            'date',
        ]

        read_only_fields = ['id']


class UserCurrencySerializers(serializers.ModelSerializer):
    last_rate_value = serializers.FloatField(read_only=True, source='currency.last_rate_of_currency.value')

    class Meta:
        model = UserCurrency
        fields = [
            'id',
            'user',
            'currency',
            'threshold',
            'last_rate_value',
        ]

        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        instance = super().create(validated_data)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['currency'] = CurrencySerializer(instance.currency, context=self.context).data
        return representation
