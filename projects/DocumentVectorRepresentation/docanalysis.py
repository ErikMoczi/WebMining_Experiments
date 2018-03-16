import glob, os, re, math, copy


def log_dec(value):
    return math.log(value, 10)


def binary_freq_transform(value):
    if value > 0:
        return 1
    else:
        return 0


def log_freq_transform(value):
    if value > 0:
        return 1 + log_dec(value)
    else:
        return 0


def inverse_freq_transform(value, total_documents, total_apperance_per_doc):
    if value > 0:
        return (1 + log_dec(value)) * log_dec(total_documents / total_apperance_per_doc)
    else:
        return 0


class Analysis:
    def __init__(self, infilepath):
        self.__infilepath = infilepath

        self.__documents = glob.glob(infilepath + "*.txt")
        self.__documents_header = self.__get_documents_header()
        self.__data = self.__read_data()

        self.__transform()

    @property
    def binary_freq(self):
        return self.__binary_freq

    @property
    def log_freq(self):
        return self.__log_freq

    @property
    def inverse_freq(self):
        return self.__inverse_freq

    @property
    def data(self):
        return self.__data

    def __init_out_put(self):
        self.__binary_freq = copy.deepcopy(self.data)
        self.__log_freq = copy.deepcopy(self.data)
        self.__inverse_freq = copy.deepcopy(self.data)

    def __read_data(self):
        data = {}
        for document in self.__documents:
            with open(document, "r") as file:
                for line in file.readlines():
                    element = re.split(r'\t+', line)[-1].strip()
                    if not element in data:
                        data[element] = self.__documents_header.copy()
                    data[element][os.path.splitext(os.path.basename(document))[0]] += 1
        return data

    def __get_documents_header(self):
        documents_name = {}
        for tag in self.__documents:
            documents_name[os.path.splitext(os.path.basename(tag))[0]] = 0
        return documents_name

    def __transform(self):
        print("---> Creating vector representation")
        self.__init_out_put()
        for lem, documents in self.__data.items():
            for doc_name, value in documents.items():
                self.__binary_freq[lem][doc_name] = binary_freq_transform(value)
                self.__log_freq[lem][doc_name] = log_freq_transform(value)
                self.__inverse_freq[lem][doc_name] = inverse_freq_transform(value, len(documents), self.__apperance_count(documents))

    def __apperance_count(self, documents):
        return sum(x >= 1 for x in documents.values())
