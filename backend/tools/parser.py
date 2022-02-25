from configparser import ConfigParser
import os


DEFAULT_SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "settings.ini")


class Config_Parser:
    def __init__(self, path=DEFAULT_SETTINGS_PATH, allow_default=False):
        self.path = path
        self.__parser_ = ConfigParser()
        self.__parser_.read(self.path)
        self.allow_default = allow_default


    def get_sections(self):
        section_data = {}

        if self.allow_default:
            section_data["DEFAULT"] = {}
            for attribute_name in self.__parser_["DEFAULT"]:
                section_data["DEFAULT"][attribute_name] = self.__parser_["DEFAULT"][attribute_name]


        for section in self.__parser_.sections():
            section_data[section] = {}

            for attr_ in self.__parser_[section]:
                if not attr_ in self.__parser_["DEFAULT"]:
                    section_data[section][attr_] = self.__parser_[section][attr_]

        return section_data



