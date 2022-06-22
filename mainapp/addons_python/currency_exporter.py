from requests import get
from datetime import datetime

import xml.etree.ElementTree as ET


CBR_API_URL = "https://www.cbr.ru/scripts/XML_daily.asp?date_req={}"
CURRENCY_ID_DICT = {
    'USD': 'R01235'
}


def usdrub_currency_export(currency_name: str) -> float:
    """
    Экспортирует курс пары доллар/рубль с сайта ЦБРФ на текущий день
    :param currency_name: Название нужной валюты, которое должно содержаться в CURRENCY_ID_DICT
    :return: Текущее значение курса
    """
    if CURRENCY_ID_DICT.get(currency_name.upper()) is None:
        print(f'log: Данное название валюты не существует')
        return 0

    response = get(CBR_API_URL.format(datetime.now().strftime('%d/%m/%Y')))
    if response.status_code != 200:
        print(f'log: неудачный запрос к cbr, код {response.status_code}')
        return 0

    xml = ET.fromstring(response.text)
    for currency in xml.findall('Valute'):
        if currency.attrib.get('ID') == CURRENCY_ID_DICT.get(currency_name.upper()):
            return float(currency.find('Value').text.replace(',', '.'))
    print(f'log: Не удалось найти нужной валюты в ответе cbr')
    return 0


if __name__ == '__main__':
    print(usdrub_currency_export('usd'))