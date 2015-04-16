import testtools

from falcon import cors


class CORSTests(testtools.TestCase):
    def test_allow_all_origins(self):
        for p in [cors.Parameters('YOLO', 'YOLO', 'YOLO')]:
            self.assertTrue(cors.allow_all_origins(p))

    def test_allow_origins(self):
        pred = cors.allow_origins(['good'])

        for p in [cors.Parameters('good', 'YOLO', 'YOLO')]:
            self.assertTrue(pred(p))

        for p in [cors.Parameters('bogus', 'YOLO', 'YOLO')]:
            self.assertFalse(pred(p))

    def test_allow_all_methods(self):
        for p in [cors.Parameters('YOLO', 'YOLO', 'YOLO')]:
            self.assertTrue(cors.allow_all_methods(p))

    def test_allow_methods(self):
        pred = cors.allow_methods(['HEAD'])

        for p in [cors.Parameters('YOLO', 'HEAD', 'YOLO')]:
            self.assertTrue(pred(p))

        for p in [cors.Parameters('YOLO', 'POST', 'YOLO')]:
            self.assertFalse(pred(p))
