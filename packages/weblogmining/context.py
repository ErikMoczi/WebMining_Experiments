from .FileReaderParallel import FileReaderParallel


class WebLogMining:
    def __init__(self, input_file, output_file):
        self.__input_file = input_file
        self.__output_file = output_file

        FileReaderParallel(self.__input_file, self.__output_file)
