from django.conf import settings
import requests
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from newpro.models import Course, Lesson, Subscription, Payment
from newpro.permissions import OwnerOnly
from newpro.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer


class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        if self.request.user.is_staff:
            return Course.objects.all()
        return Course.objects.filter(created_user=self.request.user)

class CourseCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(created_user=self.request.user)


class CourseUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]


class CourseRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]



class CourseDestroyAPIView(generics.DestroyAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [OwnerOnly]


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Lesson.objects.all()
        return Lesson.objects.filter(created_user=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated] #, ModeratorPermissionCreateDestroy]

    def perform_create(self, serializer):
        return serializer.save(created_user=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [OwnerOnly]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(status=Subscription.ACTIVE)


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(status=Subscription.INACTIVE)


# class PaymentAPIView(APIView):

#     # yoomoney.ru

#     def get(self, *args, **kwargs):
#
#         course_pk = self.kwargs.get('pk')
#         course_item = Course.objects.filter(pk=course_pk).first()
#         context = {
#             'receiver': settings.YOOMONEY_WALLET,
#             'label': f'{course_item.title}',
#             'sum': f'{course_item.price}'
#         }
#
#         return render(self.request, 'newpro/payment_form.html', context)

class TinkoffPayAPIView(APIView):
    def get(self, *args, **kwargs):
        course_pk = kwargs.get('pk')
        course_item = get_object_or_404(Course, pk=course_pk)

        payment = Payment.objects.create(paying_user=self.request.user, paid_course=course_item.id, summ=course_item.price,
                                         pay_type=Payment.TRANSFER)

        data_for_request = {
            "TerminalKey": f'{settings.TERMINAL_KEY}',
            "Amount": course_item.price,
            "OrderId": course_item.pk,
            "Description": "Оплата курса",
            "DATA": {
                "Phone": "+77051234567",
                "Email": "admin@sky.pro"
            },
            "Receipt": {
                "Email": "a@test.ru",
                "Phone": "+79031234567",
                "EmailCompany": "b@test.ru",
                "Taxation": "osn",
                "Items": [
                    {
                        "Name": course_item.title,
                        "Price": course_item.price,
                        "Quantity": 1.00,
                        "Amount": course_item.price,
                        "PaymentMethod": "full_prepayment",
                        "PaymentObject": "commodity",
                        "Tax": "vat10",
                        "Ean13": "0123456789"
                    }
                ]
            }
        }

        response = requests.post('https://securepay.tinkoff.ru/v2/Init', json=data_for_request)

        return Response(response.json()['PaymentURL'])
