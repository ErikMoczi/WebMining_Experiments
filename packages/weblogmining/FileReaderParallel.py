import os
import multiprocessing as mp
from .DataTransformation import DataTransformation


# http://www.blopig.com/blog/2016/08/processing-large-files-using-python/


class FileReaderParallel:
    def __init__(self, input_file, output_file):
        self.__input_file = input_file
        self.__output_file = output_file

        self.__manage_work()

    def __manage_work(self):
        self.__init_process()

        self.__process()
        self.__post_processing()

        self.__finalize_process()

    def __init_process(self):
        self.__pool = mp.Pool()
        self.__jobs = []

    def __finalize_process(self):
        self.__pool.close()

    def __process(self):
        data_transformation = DataTransformation(self.__input_file)
        for chunkStart, chunkSize in self.__chunkify():
            self.__jobs.append(self.__pool.apply_async(data_transformation.process_wrapper, (chunkStart, chunkSize)))

    def __post_processing(self):
        output_file = open(self.__output_file, 'w')
        for job in self.__jobs:
            for item in job.get() or []:
                output_file.write('\t'.join(item.values()) + '\n')
        output_file.close()

    def __chunkify(self, size=1024 * 1024):
        file_end = os.path.getsize(self.__input_file)
        with open(self.__input_file, 'rb') as file:
            chunk_end = file.tell()
            while True:
                chunk_start = chunk_end
                file.seek(size, 1)
                file.readline()
                chunk_end = file.tell()
                yield chunk_start, chunk_end - chunk_start
                if chunk_end > file_end:
                    break
