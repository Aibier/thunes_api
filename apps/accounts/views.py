import os
from django.db.models import Q
from django.conf import settings
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from .serializer import ThunesUserAccountSerializer, ThunesUserTransactionSerializer, ThunesUserAccountTopupSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, NotFound
from apps.accounts.utils.pagination import PaginationWithDefaults
from apps.accounts.utils.generate_report import generate_report
from apps.accounts.models import UserAccount, Transaction


class ThunesUserAccountAPI(APIView):
    permission_required = (IsAuthenticated,)
    serializer_class = ThunesUserAccountSerializer

    def get(self, request):
        user_id = request.user.id
        user_account = UserAccount.objects.filter(user_id=user_id).first()
        serializer = ThunesUserAccountSerializer(user_account)
        return Response(serializer.data)


class ThunesUserAccountTopupAPI(CreateAPIView):
    permission_required = (IsAuthenticated,)
    serializer_class = ThunesUserAccountTopupSerializer


class ThunesTransactionViewSet(viewsets.ViewSet, ListAPIView, CreateAPIView):
    permission_required = [IsAuthenticated]
    serializer_class = ThunesUserTransactionSerializer
    pagination_class = PaginationWithDefaults

    def get_queryset(self):
        # get all transaction
        transactions = Transaction.objects.filter(Q(sender_id=self.request.user.id) | Q(
            receiver_id=self.request.user.id))
        return transactions

    def retrieve(self, request, pk):
        transaction = Transaction.objects.filter(id=pk).first()
        if not transaction:
            raise NotFound(detail='Not found', code=404)

        if not self.request.user.id or self.request.user.id != transaction.owner_id:
            raise PermissionDenied(detail='Permission denied', code=403)
        serializer = ThunesUserTransactionSerializer(transaction, context={'request': request})
        return Response(serializer.data)


class ThunesTransactionReportAPI(APIView):
    permission_required = [IsAuthenticated]

    def get(self, request):
        print(self.request.user)
        user_id = self.request.user.id
        if user_id:
            generate_report(user_id, 'Feb', 'May')
            with open('{}/report.pdf'.format(settings.BASE_DIR), 'rb') as pdf:
                response = HttpResponse(pdf.read(),content_type='application/pdf')
                os.remove('{}/report.pdf'.format(settings.BASE_DIR))
                return response
        raise PermissionDenied(detail='Permission denied', code=403)

