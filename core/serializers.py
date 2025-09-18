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

    def create(self, validated_data):
        applicant_data = validated_data.pop("applicant")
        applicant, _ = Applicant.objects.get_or_create(
            email=applicant_data["email"], defaults=applicant_data
        )
        # If applicant existed, update latest profile fields
        for field_name, field_value in applicant_data.items():
            setattr(applicant, field_name, field_value)
        applicant.save()

        application = Application.objects.create(
            applicant=applicant, product=validated_data["product"]
        )
        score = compute_application_score(applicant)
        application.score = score
        application.save()
        return application

    def to_representation(self, instance):
        return ApplicationDetailSerializer(instance).data


