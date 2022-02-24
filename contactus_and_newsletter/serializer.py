from rest_framework import serializers

from contactus_and_newsletter.models import ConatactUs, NewsLetter


class ConatactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConatactUs
        # fields = "__all__"
        exclude = ["status"]


class NewsLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLetter
        # fields = "__all__"
        exclude = ["id"]
