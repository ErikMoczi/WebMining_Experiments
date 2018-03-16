import os, shutil, glob
import treetaggerwrapper as ttpw


class Lematization:
    def __init__(self, infilepath, outfilepath):
        self.__outfilepath = outfilepath
        self.__infilepath = infilepath

        self.__create_out_file_dir()
        self.__run()

    def __create_out_file_dir(self):
        if os.path.exists(self.__outfilepath):
            shutil.rmtree(self.__outfilepath)
        os.mkdir(self.__outfilepath)

    def __run(self):
        print("---> Creating lemas for documents")
        poll = ttpw.TaggerPoll(TAGLANG='sk', TAGDIR='TreeTagger')
        res = []
        for item in glob.glob(self.__infilepath + "*.txt"):
            res.append(poll.tag_file_to_async(item, self.__outfilepath + os.path.basename(item)))
        for i, r in enumerate(res):
            r.wait_finished()
