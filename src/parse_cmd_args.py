
class CmdArgumentsParser(object):
    """
    This class parses the command line arguments
    supplied form user.
    It has 3 attributes:
        1.  config_name: String, the name of the configuration (will correspond to json file).
    """

    def __init__(self, args)-> None:
        super().__init__()

        # attributes
        self.__config_name = None
        self.__file_name = None
        self.__raw_packages = False

        # methods
        self.__validate_args(args)
        self.__retrieve_config_name(args)
        self.__retrieve_file_name(args)

    @property
    def config_name(self):
        return self.__config_name

    @property
    def file_name(self):
        return self.__file_name

    @classmethod
    def __validate_args(cls, args):
        """
        Validates args array
        :raise Exception if the array length is less than 2
        """
        len_args = len(args)

        if len_args < 2:
            raise Exception("Config Name Must Be Specified")

        if len_args > 3:
            raise Exception("Too many arguments")

    def __retrieve_config_name(self, args):
        """
        It extracts the second element
        from the parameter args array
        :param args: args array
        """
        param1 = args[1]

        if param1 == "--packages":
            self.__config_name = None
            self.__raw_packages = True
        else:
            self.__config_name = args[1]

    def __retrieve_file_name(self, args):
        """
        It extracts the third element
        from the parameter args array
        :param args:
        :return:
        """
        if len(args) == 3:
            self.__file_name = args[2]

    def is_raw_packages(self):
        return self.__raw_packages
