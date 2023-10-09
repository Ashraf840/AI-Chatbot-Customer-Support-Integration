import datetime


class DATA_CURATOR:
    def __init__(self, cso_emai_chat_create_time, cso_email_num_of_chats) -> None:
        self.data_1 = cso_emai_chat_create_time
        self.data_2 = cso_email_num_of_chats

    def main_method(self):
        data_1_processed = []
        for entry in self.data_1:
            data_1_processed.append({
                'cso': entry['cso'],
                'created_at': entry['created_at'].strftime("%Y-%m-%d %H:%M:%S")
            })
        print('data_1_processed \n',data_1_processed)
        cso_to_chats = dict(self.data_2)

        print('CSO to chats \n', cso_to_chats, '\n')
        data = []
        ids_processed = set()
        print('ids_processed',ids_processed,'\n')

        for entry in data_1_processed:
            cso = entry['cso']
            num_of_chats = cso_to_chats.get(cso, 0)
            if cso not in ids_processed:
                ids_processed.add(cso)
                data.append({
                    'time': entry['created_at'],
                    'id': cso,
                    'num_of_chats': num_of_chats
                })
        return data
        print(' data \n', data, '\n')


