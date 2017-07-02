from tempfile import NamedTemporaryFile as Tmp
import unittest

import yoots.textfile as tf

# list of dictionaries, for testing csv|json|txt
list_of_dicts = [
    {'a': 1, 'b': 2, 'c': 3},
    {'a': 11, 'b': 12, 'c': 13}]

# dictionary of dictionaries, for testing ini|json|txt
dict_of_dicts = {
    'section1': {'a': 1, 'b': 2, 'c': 3},
    'section2': {'a': 11, 'b': 12, 'c': 13}}


class TestTextFile(unittest.TestCase):
    """Test TextFile class"""

    def test_csv(self):
        """Test write+read CSV file."""
        tmpfile = Tmp(suffix=".csv")
        fname = tmpfile.name
        outfile = tf.TextFile(fname)
        result = outfile.write(list_of_dicts, force=True)
        self.assertTrue(result)
        infile = tf.TextFile(fname)
        result = infile.read()
        self.assertTrue(result)

    def test_ini(self):
        """Test write+read INI file."""
        tmpfile = Tmp(suffix=".ini")
        fname = tmpfile.name
        outfile = tf.TextFile(fname)
        result = outfile.write(dict_of_dicts, force=True)
        self.assertTrue(result)
        infile = tf.TextFile(fname)
        result = infile.read()
        self.assertTrue(result)

    def test_json(self):
        """Test write+read JSON file."""
        tmpfile = Tmp(suffix=".json")
        fname = tmpfile.name
        outfile = tf.TextFile(fname)
        result = outfile.write(dict_of_dicts, force=True)
        self.assertTrue(result)
        infile = tf.TextFile(fname)
        result = infile.read()
        self.assertTrue(result)

    def test_txt(self):
        """Test write+read TXT file."""
        tmpfile = Tmp(suffix=".txt")
        fname = tmpfile.name
        outfile = tf.TextFile(fname)
        result = outfile.write(dict_of_dicts, force=True)
        self.assertTrue(result)
        infile = tf.TextFile(fname)
        result = infile.read()
        self.assertTrue(result)

    def test_yaml(self):
        """Test write+read YAML file."""
        tmpfile = Tmp(suffix=".yaml")
        fname = tmpfile.name
        outfile = tf.TextFile(fname)
        result = outfile.write(dict_of_dicts, force=True)
        self.assertTrue(result)
        infile = tf.TextFile(fname)
        result = infile.read()
        self.assertTrue(result)

    def test_confirm_yn_n(self):
        """Test confirmation prompt."""
        for reply in ['Y', 'y']:
            tf.raw_input = lambda x: reply
            confirmed = tf.TextFile.confirm_yn_n()
            self.assertTrue(confirmed)
        for reply in ['N', 'n', '']:
            tf.raw_input = lambda x: reply
            confirmed = tf.TextFile.confirm_yn_n()
            self.assertFalse(confirmed)


if __name__ == "__main__":
    unittest.main()
