import random
import string
from django.db import transaction
from rest_framework import serializers
from .models import UserAccount, Transaction, TransactionStatuses, TransactionTypes


class ThunesUserAccountSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.CharField()
    account = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    last_modified_timestamp = serializers.SerializerMethodField()

    def get_name(self, name):
        return name

    def get_balance(self, instance: UserAccount):
        return instance.balance

    def get_account(self, instance: UserAccount):
        return instance.account

    def get_id(self, instance: UserAccount):
        return str(instance.id)

    def get_last_modified_timestamp(self, instance: UserAccount):
        return instance.last_modified_timestamp

    class Meta:
        model = UserAccount
        fields = '__all__'

class ThunesUserAccountTopupSerializer(serializers.Serializer):
    balance =  serializers.DecimalField(max_digits=15, decimal_places=4)
    last_modified_timestamp = serializers.SerializerMethodField()

    def validate_balance(self, balance):
        request = self.context.get('request')
        print(request.user)
        if not request.user.id:
            raise serializers.ValidationError(detail='Permission denied', code=401)

        if not UserAccount.objects.filter(user_id=request.user.id).exists():
            raise serializers.ValidationError('You do not have account please create one.')
        
        if balance <= 0:
            raise serializers.ValidationError('Please provide valid topup amount.')

        return balance

    def get_last_modified_timestamp(self, instance: UserAccount):
        return instance.last_modified_timestamp

    @transaction.atomic()
    def create(self, validated_data):
        print('validated_data {}'.format(validated_data))
        request = self.context.get('request')
        instance = UserAccount.objects.filter(user_id=request.user.id).first()
        instance.balance = instance.balance + validated_data.get('balance')
        instance.save()
        return instance


class ThunesUserTransactionSerializer(serializers.Serializer):
    amount =  serializers.DecimalField(max_digits=15, decimal_places=4)
    receiver_id = serializers.IntegerField()
    last_modified_timestamp = serializers.SerializerMethodField()
    sender_id = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    transaction_id = serializers.SerializerMethodField()

    def validate_amount(self, amount):

        request = self.context.get('request')
        if not request.user.id:
            raise serializers.ValidationError(detail='Permission denied', code=401)

        if amount <= 0:
            raise serializers.ValidationError(details='Amount can be negative', code=401)
        user_accounts = UserAccount.objects.filter(user_id=request.user.id)
        if not user_accounts:
            raise serializers.ValidationError('User account not found, please try again')

        if user_accounts.first() and user_accounts.first().balance < amount:
            raise serializers.ValidationError('Insufficient balance')

        return amount

    def validate_receiver_id(self, receiver_id):
        if not UserAccount.objects.filter(user_id=receiver_id):
            raise serializers.ValidationError('Receiver account not found, please try again.')
        return receiver_id

    def get_last_modified_timestamp(self, instance: Transaction):
        return instance.last_modified_timestamp

    def get_sender_id(self, instance: Transaction):
        return instance.sender_id

    def get_is_owner(self, instance: Transaction):
        return True if instance.sender_id == self.context.get('request').user.id else False

    def get_transaction_id(self, instance: Transaction):
        return str(instance.id)

    @transaction.atomic()
    def create(self, validated_data):
        request = self.context.get('request')
        data = validated_data
        kwargs = {
            'owner_id': request.user.id,
            'sender_id':request.user.id,
            'receiver_id': validated_data.get('receiver_id'),
            'amount': validated_data.get('amount'),
            'type': TransactionTypes.ACCOUNT,
            'status': TransactionStatuses.COMPLETED
        }
        new_transaction = Transaction.objects.create(**kwargs)
        return new_transaction