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

    def validate(self, attrs):
        # Trim first_name and last_name; collapse leading/trailing whitespace
        first_name = attrs.get("first_name")
        last_name = attrs.get("last_name")
        if isinstance(first_name, str):
            attrs["first_name"] = first_name.strip()
        if isinstance(last_name, str):
            attrs["last_name"] = last_name.strip()

        # Normalize middle_name: if string -> trim; if empty after trim -> None; if None -> keep None
        middle_name = attrs.get("middle_name")
        if middle_name is None:
            attrs["middle_name"] = None
        elif isinstance(middle_name, str):
            trimmed = middle_name.strip()
            attrs["middle_name"] = trimmed if trimmed != "" else None
        return attrs


class ApplicationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["id", "status", "score", "product", "created_at"]


class ApplicationCreateSerializer(serializers.Serializer):
    applicant = ApplicantSerializer()
    product = serializers.ChoiceField(choices=Application.Product.choices)

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


