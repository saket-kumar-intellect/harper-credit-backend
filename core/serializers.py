from rest_framework import serializers

from django.db import IntegrityError
from rest_framework import serializers

from core.models import Applicant, Application
from core.utils import compute_application_score


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "phone",
            "annual_income",
            "employment_status",
            "city",
            "state",
            "country",
            "postal_code",
        ]


class ApplicationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["id", "status", "score", "product", "created_at"]


class ApplicationCreateSerializer(serializers.Serializer):
    applicant = ApplicantSerializer()
    product = serializers.ChoiceField(choices=Application.Product.choices)

    # Unified name normalization for first_name, middle_name, last_name
    def validate(self, attrs):
        applicant = attrs.get("applicant") or {}
        for field_name in ("first_name", "middle_name", "last_name"):
            value = applicant.get(field_name)
            if isinstance(value, str):
                applicant[field_name] = value.strip()
        if applicant.get("middle_name") == "":
            applicant["middle_name"] = None
        attrs["applicant"] = applicant
        return attrs

    def create(self, validated_data):
        applicant_data = validated_data.pop("applicant")
        try:
            applicant = Applicant.objects.create(**applicant_data)
        except IntegrityError:
            raise serializers.ValidationError({
                "applicant": {"email": ["An applicant with this email already exists."]}
            })

        application = Application.objects.create(
            applicant=applicant, product=validated_data["product"]
        )
        score = compute_application_score(applicant)
        application.score = score
        application.save()
        return application

    def to_representation(self, instance):
        return ApplicationDetailSerializer(instance).data


