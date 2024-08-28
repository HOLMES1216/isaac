from django.test import TestCase
from project.models import *
class eclipseCalculationTest(TestCase):
    fixtures=["all_models_project_fixture.json"]

    def test_pad_model(self):
        obj = Brake.objects.get(id=1)
        self.assertEqual(obj.item,'II110674/57324(*PB*)')
