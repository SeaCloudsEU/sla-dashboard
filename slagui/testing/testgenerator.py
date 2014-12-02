
import unittest

from slagui.generator import AgreementGenerator
from slagui.generator import AgreementParams


class TestGenerator(unittest.TestCase):

    def test_agreement_generator(self):
        #template = path("slagui/testing/template-generator.xml").text()
        with open("slagui/testing/template-generator.xml") as f:
            template = f.read()
        params = AgreementParams(
            "templateid", "consumerid", "appid", "moduleid")
        generator = AgreementGenerator(template, params)
        agreement, agreement_id = generator.do()
        print(agreement)
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
