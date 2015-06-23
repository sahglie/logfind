import unittest
import os.path
from logfind import Logfind


class LogfindTest(unittest.TestCase):
    def setUp(self):
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.config_file = os.path.join(self.root_dir, "tests", ".logfind")
        self.large_file = os.path.join(self.root_dir, "fixtures", "large_file.txt")
        self.small_file = os.path.join(self.root_dir, "fixtures", "small_file.txt")

    def test_load_search_paths(self):
        logfind = Logfind(self.config_file)
        paths = ["/Users/sahglie/lib", "/Users/sahglie/bin"]
        self.assertEquals(paths, logfind.search_paths())

    def test_error_for_missing_config_file(self):
        config_file = self.config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".badfile")
        logfind = Logfind(config_file)
        self.assertRaises(IOError, logfind.search_paths)

    def test_find_with_and_matching(self):
        search_files = [self.large_file]
        logfind = Logfind(search_files=search_files)
        self.assertEqual(0, len(logfind.find(["hat", "pat"])))
        self.assertEqual(1, len(logfind.find(["hat", "fat", "bat", "mat"])))

    def test_find_with_or_matching(self):
        search_files = [self.large_file]
        logfind = Logfind(search_files=search_files, logic_flag=Logfind.OR)
        self.assertEqual(0, len(logfind.find(["that", "pat"])))
        self.assertEqual(1, len(logfind.find(["hat", "pat"])))
        self.assertEqual(1, len(logfind.find(["hat", "fat", "bat", "mat", "pat"])))

    def test_find_with_regex_matching(self):
        search_files = [self.large_file]
        logfind = Logfind(search_files=search_files)
        self.assertEqual(1, len(logfind.find(["h.{2}"])))
        self.assertEqual(1, len(logfind.find([".at"])))
        self.assertEqual(1, len(logfind.find(["f.+", "b.t"])))


if __name__ == '__main__':
    unittest.main()
