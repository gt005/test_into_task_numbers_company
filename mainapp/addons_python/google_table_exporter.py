from typing import Tuple, Dict
from datetime import datetime

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


class GoogleTableExporter:
    """ Экспортирует данные из таблицы и преобразовывает их """
    __CREDENTIALS_FILE = 'credentials.json'
    __spreadsheet_id = '1UDh6xIR9k_Dt6dKpdnqY7hZ7YQe6zD0Dmv9-s9gHJyg'

    @classmethod
    def __export_data_from_sheet(cls) -> Dict:
        """
        Функция запрашивает данные файла spreadsheet_id по аккаунту из файла CREDENTIALS_FILE
        :return: Словарь с ключами: majorDimension - rows/columns, range - диапазон выбранных ячеек,
         values - значения выбранного диапазона
        """
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            cls.__CREDENTIALS_FILE,
            ('https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive')
        )
        httpAuth = credentials.authorize(httplib2.Http())
        service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

        values = service.spreadsheets().values().get(
            spreadsheetId=cls.__spreadsheet_id,
            range='A1:D',
            majorDimension='ROWS'
        ).execute()
        return values

    def get_values(cls) -> Tuple[Tuple[int, int, int, datetime], ...]:
        """
        Получает данные по __export_data_from_sheet и обрабатывает их, приводя ячейки к нужным типам данных
        :return: Кортеж из строк файла
        """
        raw_values = cls.__export_data_from_sheet()

        data_with_correct_types = tuple(
            (
                (int(table_row[0]), int(table_row[1]),
                 int(table_row[2]), datetime.strptime(table_row[3], '%d.%m.%Y'))
                for table_row in raw_values.get('values')[1:]
            )
        )
        return data_with_correct_types


if __name__ == '__main__':
    from pprint import pprint
    a = GoogleTableExporter()
    pprint(a.get_values())