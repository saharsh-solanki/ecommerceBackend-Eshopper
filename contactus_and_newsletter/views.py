from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from contactus_and_newsletter.serializer import ConatactUsSerializer, NewsLetterSerializer


class ConatactUsView(generics.CreateAPIView):
    serializer_class = ConatactUsSerializer


class NewsLetterView(generics.CreateAPIView):
    serializer_class = NewsLetterSerializer

