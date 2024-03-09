import unittest
from  censoror import censor_text

class TestCensorPhones(unittest.TestCase):
    def test_censor_phone_number(self):
        content = "Call me at (352)535-1889."
        flags = ['phones']
        expected_content = "Call me at █████████████."
        censored_content = censor_text(content, flags)
        self.assertEqual(censored_content, expected_content)

if __name__ == '__main__':
    unittest.main()
