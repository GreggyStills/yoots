import unittest
from yoots import prompt


class TestPrompt(unittest.TestCase):

    def test_confirmyn_yes(self):
        prompt.raw_input = lambda x: "y"
        result = prompt.confirm_yn()
        self.assertTrue(result)

    def test_confirmyn_no(self):
        prompt.raw_input = lambda x: "n"
        result = prompt.confirm_yn()
        self.assertFalse(result)

    def test_confirmcountdown(self):
        prompt.time.sleep = lambda x: None
        result = prompt.confirm_countdown()
        self.assertTrue(result)

    def test_confirm_rnd(self):
        prompt.raw_input = lambda x: "1"
        result = prompt.confirm_rnd(1, 2)
        self.assertTrue(result)

    def test_ask_string(self):
        prompt.raw_input = lambda x: "blah"
        result = prompt.ask_string()
        self.assertTrue(result == "blah")

    def test_ask_string_confirm(self):
        prompt.raw_input = lambda x: "y"
        result = prompt.ask_string_confirm()
        self.assertTrue(result)

    def test_ask_string_secret(self):
        prompt.getpass = lambda x: "blah"
        result = prompt.ask_string_secret()
        self.assertTrue(result == "blah")

    def test_pick_one(self):
        prompt.raw_input = lambda x: "1"
        result = prompt.pick_one(['a', 'b', 'c'])
        self.assertTrue(result == "a")

    def test_pick_many_all(self):
        prompt.raw_input = lambda x: "all"
        result = prompt.pick_many(['a', 'b', 'c'])
        self.assertTrue(result == ['a', 'b', 'c'])

    def test_pick_many_none(self):
        prompt.raw_input = lambda x: "none"
        result = prompt.pick_many(['a', 'b', 'c'])
        self.assertTrue(result == [])

    def test_pick_many_multiple(self):
        prompt.raw_input = lambda x: "1 2"
        result = prompt.pick_many(['a', 'b', 'c'])
        self.assertTrue(result == ['a', 'b'])

    def test_pick_many_one(self):
        prompt.raw_input = lambda x: "1"
        result = prompt.pick_many(['a', 'b', 'c'])
        self.assertTrue(result == ['a'])


if __name__ == '__main__':
    unittest.main(exit=False)
