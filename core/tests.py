from django.test import TestCase
from rest_framework.test import APIClient


class ApplicationCreateNormalizationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_with_null_middle_name_returns_201(self):
        payload = {
            "applicant": {
                "first_name": "  Asha  ",
                "middle_name": None,
                "last_name": "  Mehta ",
                "email": "asha.norm@example.com",
                "phone": "+1-415-555-1200",
                "annual_income": "125000.00",
                "employment_status": "SALARIED",
                "city": "San Francisco",
                "state": "CA",
                "country": "US",
                "postal_code": "94107",
            },
            "product": "Platinum",
        }
        resp = self.client.post("/api/applications", data=payload, format="json")
        self.assertEqual(resp.status_code, 201, resp.content)
        self.assertIn("id", resp.data)


