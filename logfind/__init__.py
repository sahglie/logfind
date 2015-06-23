from os.path import expanduser
import os.path
import glob
import re

class Logfind:
    AND = "and"
    OR = "or"

    def __init__(self, config_file=None, search_files=[], logic_flag=AND):
        self.config_file = config_file or self.__default_config_file()
        self.search_files = search_files
        self.logic_flag = logic_flag

    def find(self, terms=[]):
        matchers = [re.compile(term) for term in terms]

        matched_files = []
        for filename in self.__find_search_files():
            if self.logic_flag == Logfind.AND:
                if self.__all_terms_match(filename, matchers):
                    matched_files.append(filename)
            else:
                if self.__any_terms_match(filename, matchers):
                    matched_files.append(filename)
        return matched_files

    def search_paths(self):
        paths = []
        with open(self.config_file) as fd:
            for line in fd.readlines():
                paths.append(line.strip())
        return paths

    def __all_terms_match(self, filename, matchers):
        with open(filename) as fd:
            data = fd.read()
            matches = [True for m in matchers if re.search(m, data)]
            return len(matches) == len(matchers)

    def __any_terms_match(self, filename, matchers):
        with open(filename) as fd:
            data = fd.read()
            for m in matchers:
                if re.search(m, data):
                    return True
            return False

    def __find_search_files(self):
        if len(self.search_files):
            return self.search_files
        else:
            for path in self.search_paths():
                for filename in glob.glob("{path}/*".format(path=path)):
                    self.search_files.append(filename)
        return self.search_files

    def __default_config_file(self):
        return os.path.join(expanduser("~"), ".logfind")
