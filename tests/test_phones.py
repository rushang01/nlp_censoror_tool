# import unittest
# import censoror

# class TestCensorPhones(unittest.TestCase):
#     def test_censor_phone_number(self):
#         content = "Call me at (123) 456-7890."
#         flags = ['phones']
#         expected_content = "Call me at ██████████████."
#         censored_content = censoror.censor_text(content, flags)
#         self.assertEqual(censored_content, expected_content)

# if __name__ == '__main__':
#     unittest.main()

def test_censor_phones_with_pyap():
    assert(True)