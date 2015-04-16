import testtools

from falcon import cors

class CORSTests(testtools.TestCase):
    def test_allow_all_origins(self):
        for p in [cors.Parameters("YOLO", "YOLO", "YOLO")]:
            self.assertTrue(cors.allow_all_origins(p))

    def test_allow_all_methods(self):
        for p in [cors.Parameters("YOLO", "YOLO", "YOLO")]:
            self.assertTrue(cors.allow_all_methods(p))
