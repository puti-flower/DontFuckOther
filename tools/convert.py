from typing import Dict


def text_to_dict(headers: str) -> Dict:
    '''
    转换网页复制的字典值, 参考: 李玺

    headers: """
    xxx1: xxx
    xxx2: xxx
    """

    return {"xxx1": xxx, "xxx2": xxx}
    '''

    if not headers:
        raise TypeError("headers is not empty str!")

    lines = headers.splitlines()
    headers_list = [header.split(":", 1) for header in lines]

    result = dict()
    for header_item in headers_list:
        if not len(header_item) == 2:
            continue
        item_key = header_item[0].strip()
        item_value = header_item[1].strip()
        result[item_key] = item_value
    return result
