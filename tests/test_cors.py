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

    def test_composed(self):
        pred = cors.pred_all([
            cors.allow_methods(['HEAD']),
            cors.allow_origins(['example.test'])
        ])

        for p in [cors.Parameters('example.test', 'HEAD', 'YOLO')]:
            self.assertTrue(pred(p))

        for p in [cors.Parameters('example.test', 'POST', 'YOLO'),
                  cors.Parameters('example.bogus', 'HEAD', 'YOLO')]:
            self.assertFalse(pred(p))


class PredicateToolsTests(testtools.TestCase):
    def test_pred_all_constantly_true(self):
        constantly_true = lambda *a, **kw: True

        p = cors.pred_all([constantly_true, constantly_true])
        for arg in [cors.Parameters('YOLO', 'POST', 'YOLO')]:
            self.assertTrue(p(arg))

    def test_pred_all_mixed(self):
        constantly_true = lambda *a, **kw: True
        constantly_false = lambda *a, **kw: False

        p = cors.pred_all([constantly_true, constantly_false])
        for arg in [cors.Parameters('YOLO', 'POST', 'YOLO')]:
            self.assertFalse(p(arg))
