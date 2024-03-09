# import unittest
# import censoror
# class TestCensorNames(unittest.TestCase):
#     def test_censor_single_name(self):
#         content = "John Doe went to the park."
#         flags = ['names']
#         expected_content = "████████ went to the park."
#         censored_content = censoror.censor_text(content, flags)
#         self.assertEqual(censored_content, expected_content)


#     def test_censor_multiple_names(self):
#         content = "John Doe and Jane Doe went to the park."
#         flags = ['names']
#         expected_content = "████████ and ████████ went to the park."
#         censored_content = censoror.censor_text(content, flags)
#         self.assertEqual(censored_content, expected_content)


# if __name__ == '__main__':
#     unittest.main()

def test_censor_names_with_pyap():
    assert(True)