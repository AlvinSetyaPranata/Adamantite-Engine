from configparser import ConfigParser


class Config_Parser:
    def __init__(self, path, allow_default=False):
        self.path = path
        self.__parser_ = ConfigParser()
        self.__parser_.read(path)
        self.allow_default = allow_default

    def get_sections(self):
        section_data = {}

        if self.allow_default:
            section_data["DEFAULT"] = self.__parser_["DEFAULT"]
        
        for section in self.__parser_.sections():
            section_data[section] = self.__parser_[section]

        
        return section_data


