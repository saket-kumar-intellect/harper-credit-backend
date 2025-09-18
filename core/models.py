from django.db import models


class Applicant(models.Model):
    class EmploymentStatus(models.TextChoices):
        SALARIED = "SALARIED", "SALARIED"
        SELF_EMPLOYED = "SELF_EMPLOYED", "SELF_EMPLOYED"
        STUDENT = "STUDENT", "STUDENT"
        UNEMPLOYED = "UNEMPLOYED", "UNEMPLOYED"

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2)
    employment_status = models.CharField(
        max_length=20, choices=EmploymentStatus.choices
    )
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} <{self.email}>"


class Application(models.Model):
    class Product(models.TextChoices):
        PLATINUM = "Platinum", "Platinum"
        GOLD = "Gold", "Gold"

    class Status(models.TextChoices):
        SUBMITTED = "Submitted", "Submitted"
        UNDER_REVIEW = "UnderReview", "UnderReview"
        APPROVED = "Approved", "Approved"
        REJECTED = "Rejected", "Rejected"

    applicant = models.ForeignKey(
        Applicant, on_delete=models.CASCADE, related_name="applications"
    )
    product = models.CharField(max_length=20, choices=Product.choices)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.SUBMITTED
    )
    score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Application#{self.pk} - {self.product} - {self.status}"


