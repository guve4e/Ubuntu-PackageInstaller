
class CmdArgumentsParser(object):
    """
    This class parses the command line arguments
    supplied form user.
    It has 3 attributes:
        1.  project_name: String, the name of the project.
        2.  filter_keyword: String, if the user wants to filter test cases by word.
        3.  verbose: Boolean, if the user wants verbose info or not.
    """

    def __init__(self, args) -> None:
        super().__init__()

        # attributes
        self.__config_name = None
        self.__verbose = False

        # methods
        print("Arguments are : " + str(args))
        self.__validate_args(args)
        self.__retrieve_config_name(args)
        self.__retrieve_verbose(args)

    @property
    def project_name(self):
        return self.__config_name

    @project_name.setter
    def project_name(self, value):
        self.__config_name = value

    @property
    def verbose(self):
        return self.__verbose

    @verbose.setter
    def verbose(self, value):
        self.__verbose = value

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

        self.__project_name = args[1]

    def __retrieve_verbose(self, args):
        """
        It extracts the third element
        from the parameter args array
        :param args:
        :return:
        """

        self.__verbose = args[2]