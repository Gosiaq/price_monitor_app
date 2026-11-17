from django.test import SimpleTestCase
from monitor_ofert.pipelines import DjangoDatabasePipeline

class PipelineLogicTest(SimpleTestCase):
    def setUp(self):
        self.pipeline = DjangoDatabasePipeline()

    def test_parse_price(self):
        self.assertEqual(self.pipeline.parse_price("19,99 zł"), 19.99)
        self.assertEqual(self.pipeline.parse_price("Od: 1 200,50 PLN"), 1200.50)
        self.assertEqual(self.pipeline.parse_price("bad_price"), 0.0)

    def test_calculate_unit_price(self):
        price, unit = self.pipeline.calculate_unit_price(20.0, 500, 'g', 1)
        self.assertEqual(price, 40.0)
        self.assertEqual(unit, 'kg')