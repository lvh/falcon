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

    def test_multi_composed(self):
        pred = cors.pred_any([
            cors.pred_all([
                cors.allow_methods(['HEAD']),
                cors.allow_origins(['example-one.test'])
            ]),
            cors.pred_all([
                cors.allow_methods(['GET', 'POST']),
                cors.allow_origins(['example-two.test'])
            ]),
        ])

        for p in [cors.Parameters('example-one.test', 'HEAD', 'YOLO'),
                  cors.Parameters('example-two.test', 'GET', 'YOLO'),
                  cors.Parameters('example-two.test', 'POST', 'YOLO')]:
            self.assertTrue(pred(p))

        for p in [cors.Parameters('example-one.test', 'GET', 'YOLO'),
                  cors.Parameters('example-two.test', 'DELETE', 'YOLO'),
                  cors.Parameters('example.bogus', 'HEAD', 'YOLO')]:
            self.assertFalse(pred(p))


def constantly_true(*a, **kw):
    return True


def constantly_false(*a, **kw):
    return False


class PredicateToolsTests(testtools.TestCase):
    def test_pred_all_constantly_true(self):

        p = cors.pred_all([constantly_true, constantly_true])
        for arg in [cors.Parameters('YOLO', 'POST', 'YOLO')]:
            self.assertTrue(p(arg))

    def test_pred_all_constantly_false(self):
        p = cors.pred_any([constantly_false, constantly_false])
        for arg in [cors.Parameters('YOLO', 'POST', 'YOLO')]:
            self.assertFalse(p(arg))

    def test_pred_all_mixed(self):
        p = cors.pred_all([constantly_true, constantly_false])
        for arg in [cors.Parameters('YOLO', 'POST', 'YOLO')]:
            self.assertFalse(p(arg))

    def test_pred_any_constantly_true(self):
        p = cors.pred_any([constantly_true, constantly_true])
        for arg in [cors.Parameters('YOLO', 'POST', 'YOLO')]:
            self.assertTrue(p(arg))

    def test_pred_any_constantly_false(self):
        p = cors.pred_any([constantly_false, constantly_false])
        for arg in [cors.Parameters('YOLO', 'POST', 'YOLO')]:
            self.assertFalse(p(arg))

    def test_pred_any_mixed(self):
        p = cors.pred_any([constantly_true, constantly_false])
        for arg in [cors.Parameters('YOLO', 'POST', 'YOLO')]:
            self.assertTrue(p(arg))
