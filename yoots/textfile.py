"""Read+write text files of various formats."""
import ast
import configparser
import csv
import json
import os

import yaml

from yoots import eprint


class TextFile(object):
    """Object interface to a text-based file."""

    def __init__(self, fname, ftype=None):
        """Data file object.  Uses file extension to automatically figure out which
        parser we should use to work with the file.

        Args:
            fname (str): filename (may include a directory path)
            ftype (str): override file extension, treat file as csv|ini|json|txt
        """
        self.fname = fname
        if ftype is None:
            self.ftype = os.path.splitext(fname)[-1].strip('.').lower()
        assert self.ftype in ('csv', 'ini', 'json', 'txt', '', 'yaml'),\
            "Unsupported file type: {}".format(self.ftype)

    def read(self):
        """Read contents of file.

        Returns:
            fdata (*): file data, type varies by file content
        """
        assert os.path.isfile(self.fname), "File not found: {}".format(self.fname)
        if self.ftype == 'csv':
            fdata = self.read_csv(self.fname)
        elif self.ftype == 'ini':
            fdata = self.read_ini(self.fname)
        elif self.ftype == 'json':
            fdata = self.read_json(self.fname)
        elif self.ftype in ('txt', ''):
            fdata = self.read_text(self.fname)
        elif self.ftype == 'yaml':
            fdata = self.read_yaml(self.fname)
        else:
            fdata = None
        return fdata

    @staticmethod
    def read_csv(fname):
        """Read contents of CSV file, using Python built-in csv module.

        Args:
            fname (str): filename (may include a directory path)
        Returns:
            fdata (list): data content of CSV file, list of dictionaries
        """
        with open(fname) as infile:
            reader = csv.DictReader(infile)
            fdata = [row for row in reader]
        return fdata

    @staticmethod
    def read_ini(fname):
        """Read contents of INI file, using Python built-in ConfigParser module.

        Args:
            fname (str): filename (may include a directory path)
        Returns:
            fdata (dict): data content of file (nested dictionary)
        """
        ini = configparser.ConfigParser()
        ini.read(fname)
        cfg_sections = ini.sections()
        fdata = {}
        for section in cfg_sections:
            fdata[section] = dict(ini.items(section))
            # configparser reads values as strings, so try to interpret
            for key, value in fdata[section].items():
                try:
                    fdata[section][key] = ast.literal_eval(value)
                except (SyntaxError, ValueError):
                    pass
        return fdata

    @staticmethod
    def read_json(fname):
        """Read contents of JSON file, using Python built-in json module.

        Args:
            fname (str): filename (may include a directory path)
        Returns:
            fdata (*): data content of file, type varies by file contents
        """
        with open(fname) as infile:
            fdata = json.load(infile)
        return fdata

    @staticmethod
    def read_text(fname):
        """Read contents of text file.

        Args:
            fname (str): filename (may include a directory path)
        Returns:
            fdata (str): string content of text file
        """
        with open(fname) as infile:
            fdata = infile.read()
        return fdata

    @staticmethod
    def read_yaml(fname):
        """Read contents of YAML file.

        Args:
            fname (str): filename (may include a directory path)
        Returns:
            fdata (*): data content of file, type varies by file contents
        """
        with open(fname) as infile:
            fdata = yaml.load(infile)
        return fdata

    def write(self, fdata, force=None):
        """Write data to file.

        Args:
            fdata (*): data to be written, type varies
            force (bool): If True, and file exists, overwrite without prompt.
        Returns:
            (int): bytes written to file (i.e. file size).
        """
        if os.path.isfile(self.fname) and not force:
            force = self.confirm_yn_n()
            if force:
                eprint("Overwriting file: {}".format(self.fname))
            else:
                eprint("Write cancelled: {}".format(self.fname))
                return 0

        if self.ftype == 'csv':
            self.write_csv(self.fname, fdata)
        elif self.ftype == 'ini':
            self.write_ini(self.fname, fdata)
        elif self.ftype == 'json':
            self.write_json(self.fname, fdata)
        elif self.ftype in ('txt', ''):
            self.write_text(self.fname, fdata)
        elif self.ftype == 'yaml':
            self.write_yaml(self.fname, fdata)
        else:
            eprint("Unknown filetype [{}]; writing as text.".format(self.ftype))
            self.write_text(self.fname, fdata)
        return os.path.getsize(self.fname)

    @staticmethod
    def confirm_yn_n(msg="File exists! Overwrite? (y/N): "):
        """Get confirmation from user.  Default negative.

        Args:
            msg (str): A prompt for input
        Returns:
            (bool): True if confirmed, False if not.
        """
        while True:
            user_says = raw_input(msg)
            if user_says in ('y', 'Y'):
                return True
            elif user_says in ('n', 'N', ''):
                return False
            else:
                eprint("Invalid input. Try again.")

    @staticmethod
    def write_csv(fname, fdata):
        """Write data to CSV file, using Python built-in csv module.

        Args:
            fname (str): filename (may include a directory path)
            fdata (list): list of dict's (all dict's must have same keys)
        Returns:
            fname (str): filename (may include a directory path)
        """
        assert isinstance(fdata, list), "Input data must be a list."
        assert isinstance(fdata[0], dict), "Each list element must be a dictionary."
        keys = fdata[0].keys()
        with open(fname, 'w') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=keys, lineterminator='\n')
            writer.writeheader()
            writer.writerows(fdata)
        return fname

    @staticmethod
    def write_ini(fname, fdata):
        """Write data to INI file, using Python built-in configparser module.

        Args:
            fname (str): filename (may include a directory path)
            fdata (dict): dictionary of INI settings (nested dict, e.g.
                {section1: {key1:value1}, section2: {key1:value1, key2:value2}}
        Returns:
            fname (str): filename (may include a directory path)
        """
        assert isinstance(fdata, dict), "Input data must be a dictionary."
        ini = configparser.ConfigParser()
        for section, section_dict in fdata.items():
            ini.add_section(section)
            for key, value in section_dict.items():
                ini.set(section, key, value=str(value))
        with open(fname, 'w') as outfile:
            ini.write(outfile)
        return fname

    @staticmethod
    def write_json(fname, fdata):
        """Write data to JSON file, using Python built-in json module.

        Args:
            fname (str): filename (may include a directory path)
            fdata (*): data to be written, type varies
        Returns:
            fname (str): filename (may include a directory path)
        """
        with open(fname, 'w') as outfile:
            json.dump(fdata, outfile, indent=2)
        return fname

    @staticmethod
    def write_text(fname, fdata):
        """Write data to text file.

        Args:
            fname (str): filename (may include a directory path)
            fdata (str): data to be written
        Returns:
            fname (str): filename (may include a directory path)
        """
        with open(fname, 'w') as outfile:
            outfile.write(str(fdata))
        return fname

    @staticmethod
    def write_yaml(fname, fdata):
        """Write data to YAML file, using PyYAML.

        Args:
            fname (str): filename (may include a directory path)
            fdata (*): data to be written, type varies
        Returns:
            fname (str): filename (may include a directory path)
        """
        with open(fname, 'w') as outfile:
            outfile.write(yaml.dump(fdata, default_flow_style=False))
        return fname


def read(fname, ftype=None):
    """File read function for typical use cases.

    Args:
        fname (str): filename (may include a directory path)
        ftype (str): override file extension, treat file as csv|ini|json|txt|yaml
    Returns:
        (*): Data retrieved from file.
    """
    infile = TextFile(fname, ftype)
    return infile.read()


def write(fname, fdata, ftype=None, force=None):
    """File write function for typical use cases.

    Args:
        fname (str): filename (may include a directory path)
        fdata (*): data to be written, type varies
        ftype (str): override file extension, treat file as csv|ini|json|txt|yaml
        force (bool): If True, and file exists, overwrite without prompt.
    Returns:
        fsize (int): File size (bytes)
    """
    outfile = TextFile(fname, ftype)
    fsize = outfile.write(fdata, force)
    return fsize
