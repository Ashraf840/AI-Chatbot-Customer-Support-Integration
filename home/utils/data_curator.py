import datetime


# data_1 = [{'cso': 'tanjim.ashraf.doer.bp@gmail.com', 'created_at': datetime.datetime(2023, 2, 27, 5, 30, 31, 768000, tzinfo=datetime.timezone.utc)},
# {'cso': 'tanjim.ashraf@doer.com.bd', 'created_at': datetime.datetime(2023, 2, 27, 5, 7, 46, 848000, tzinfo=datetime.timezone.utc)},
# {'cso': 'tanjim.ashraf@doer.com.bd', 'created_at': datetime.datetime(2023, 2, 27, 5, 0, 19, 581000, tzinfo=datetime.timezone.utc)},
# {'cso': 'tanjim.ashraf@doer.com.bd', 'created_at': datetime.datetime(2023, 2, 27, 4, 59, 50, 814000, tzinfo=datetime.timezone.utc)},
# {'cso': 'tanjim.ashraf@doer.com.bd', 'created_at': datetime.datetime(2023, 2, 27, 4, 58, 37, 411000, tzinfo=datetime.timezone.utc)},
# {'cso': 'tanjim.ashraf@doer.com.bd', 'created_at': datetime.datetime(2023, 2, 27, 4, 57, 37, 108000, tzinfo=datetime.timezone.utc)},
# {'cso': 'tanjim.ashraf@doer.com.bd', 'created_at': datetime.datetime(2023, 2, 27, 4, 55, 3, 852000, tzinfo=datetime.timezone.utc)}]

# data_2 = [('tanjim.ashraf.doer.bp@gmail.com', 1),
# ('tanjim.ashraf@doer.com.bd', 6)]

# # from datetime import datetime, timezone

# # Extract relevant data from data_1
# # def data_curator(data_1, data_2):
# #     data_1_processed = []
# #     for entry in data_1:
# #         data_1_processed.append({
# #             'cso': entry['cso'],
# #             'created_at': entry['created_at'].strftime("%Y-%m-%d %H:%M:%S")
# #         })

# #     # Create dictionary mapping CSOs to number of chats from data_2
# #     cso_to_chats = dict(data_2)

# #     # Combine data_1 and data_2 to create final list
# #     data = []
# #     for entry in data_1_processed:
# #         cso = entry['cso']
# #         num_of_chats = cso_to_chats.get(cso, 0)
# #         data.append({
# #             'time': entry['created_at'],
# #             'id': cso,
# #             'num_of_chats': num_of_chats
# #         })

# #     print(data)


# data_1_processed = []
# for entry in data_1:
#     data_1_processed.append({
#         'cso': entry['cso'],
#         'created_at': entry['created_at'].strftime("%Y-%m-%d %H:%M:%S")
#     })
# # print('data_1_processed \n',data_1_processed)

# for data in data_1_processed:
#     print(data)

# print('\n'*3)

# # Create dictionary mapping CSOs to number of chats from data_2
# cso_to_chats = dict(data_2)

# # print('CSO to chats \n', cso_to_chats, '\n')
# # Combine data_1 and data_2 to create final list
# data = []
# for entry in data_1_processed:
#     cso = entry['cso']
#     num_of_chats = cso_to_chats.get(cso, 0)
#     data.append({
#         'time': entry['created_at'],
#         'id': cso,
#         'num_of_chats': num_of_chats
#     })

# # print(' data \n', data, '\n')
# for dt in data:
#     print(dt)

# print('\n'*3)

# # from iteration_utilities import unique_everseen
# # new_data = list(unique_everseen(data))

# # for dt in new_data:
# #     print(dt)

# seen = set()
# new_data = []
# for d in data:
#     t = tuple(d.items())
#     t = list(t)
#     print('-------',t)
#     # seen.add(list(tuple({'time': '2023-02-27 05:30:31', 'id': 'tanjim.ashraf.doer.bp@gmail.com', 'num_of_chats': 1})))
#     # if t not in seen:
#     #     print('NOT FOUND!')
#         # seen.add(t)
#         # print(seen)
#     #     new_data.append(d)

# # print('\n'*3)


class DATA_CURATOR:
    def __init__(self, cso_emai_chat_create_time, cso_email_num_of_chats) -> None:
        # data_1 = [{'cso': 'tanjim.ashraf.doer.bp@gmail.com', 'created_at': datetime.datetime(2023, 2, 27, 5, 30, 31, 768000, tzinfo=datetime.timezone.utc)},
        # {'cso': 'tanjim.ashraf@doer.com.bd', 'created_at': datetime.datetime(2023, 2, 27, 5, 7, 46, 848000, tzinfo=datetime.timezone.utc)},
        # {'cso': 'tanjim.ashraf@doer.com.bd', 'created_at': datetime.datetime(2023, 2, 27, 5, 0, 19, 581000, tzinfo=datetime.timezone.utc)},
        # {'cso': 'tanjim.ashraf@doer.com.bd', 'created_at': datetime.datetime(2023, 2, 27, 4, 59, 50, 814000, tzinfo=datetime.timezone.utc)},
        # {'cso': 'tanjim.ashraf@doer.com.bd', 'created_at': datetime.datetime(2023, 2, 27, 4, 58, 37, 411000, tzinfo=datetime.timezone.utc)},
        # {'cso': 'tanjim.ashraf@doer.com.bd', 'created_at': datetime.datetime(2023, 2, 27, 4, 57, 37, 108000, tzinfo=datetime.timezone.utc)},
        # {'cso': 'tanjim.ashraf@doer.com.bd', 'created_at': datetime.datetime(2023, 2, 27, 4, 55, 3, 852000, tzinfo=datetime.timezone.utc)}]
        self.data_1 = cso_emai_chat_create_time
        self.data_2 = cso_email_num_of_chats

        # data_2 = [('tanjim.ashraf.doer.bp@gmail.com', 1),
        # ('tanjim.ashraf@doer.com.bd', 6)]

    def main_method(self):
        data_1_processed = []
        for entry in self.data_1:
            data_1_processed.append({
                'cso': entry['cso'],
                'created_at': entry['created_at'].strftime("%Y-%m-%d %H:%M:%S")
            })
        print('data_1_processed \n',data_1_processed)
        # Create dictionary mapping CSOs to number of chats from data_2
        cso_to_chats = dict(self.data_2)

        print('CSO to chats \n', cso_to_chats, '\n')
        # Combine data_1 and data_2 to create final list
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


