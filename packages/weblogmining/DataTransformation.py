import re


class StatusCodeException(Exception):
    pass


class UserDataException(Exception):
    pass


class RequestDataException(Exception):
    pass


def remove_trash(input_data):
    return re.sub('\s+[q]+', '', input_data)


def get_status_code(input_data):
    status_code = [item.strip() for item in re.findall(r'"\s\d{3}\s"', input_data)]
    if not len(status_code) == 1:
        raise StatusCodeException(input_data)

    return re.sub('"', '', status_code[0]).strip()


def check_status_code(status_code):
    return int(status_code) >= 400


def clean_up(input_data):
    input_data = remove_trash(input_data)
    return input_data


def get_user_data(input_data):
    user_data = re.findall(r'"(.*?)"', input_data)
    if not len(user_data) == 3:
        raise UserDataException(input_data)

    return user_data


def check_user_data(input_data):
    return False


def get_request_data(input_data):
    data = input_data[0].split()
    if not len(data) == 3:
        raise RequestDataException(input_data)

    if input_data[0] == '-':
        raise RequestDataException(input_data)

    return data


def check_request_data(input_data):
    if not input_data[0].startswith('GET'):
        return True

    if re.search(r'(?<!robots)\.(?!(php)|(htm))[a-z]{2,4}($|\?)', input_data[1]):
        return True

    return False


def process_data(line):
    line = clean_up(line)

    status_code = get_status_code(line)
    if check_status_code(status_code):
        return None

    user_data = get_user_data(line)
    if check_user_data(user_data):
        return None

    request_data = get_request_data(user_data)
    if check_request_data(request_data):
        return None

    elements = re.split(r'\s+', line)

    return {
        'IP': elements[0],
        'Cookie': elements[1],
        'DTime': re.sub('\[|\]', '', elements[2]),
        'RequestMethod': request_data[0],
        'URL': request_data[1],
        'Version': request_data[2],
        'StatusCode': status_code,
        'Referrer': user_data[1],
        'Agent': user_data[2]
    }


class DataTransformation:
    def __init__(self, input_file):
        self.__input_file = input_file

    def process_wrapper(self, chunk_start, chunk_size):
        output_data = []
        with open(self.__input_file) as f:
            f.seek(chunk_start)
            lines = f.read(chunk_size).splitlines()
            for line in lines:
                data = process_data(line)
                output_data += [data] if data is not None else []
        return output_data
