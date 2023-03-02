import random

class NewCustomerDistribution:
    def __init__(self, amt_of_members, max_amt_of_chats_per_member, cso_id_chatamt_timestamp):
        self.amt_of_members = amt_of_members
        self.max_amt_of_chats_per_member = max_amt_of_chats_per_member
        self.cso_id_chatamt_timestamp = cso_id_chatamt_timestamp
    
    def add_new_chat(self):
        # Find the support member with the minimum number of chats
        print('NewCustomerDistribution class:', self.cso_id_chatamt_timestamp)
        minimum_chat_handler = min(self.cso_id_chatamt_timestamp, key=lambda x: x['num_of_chats'])
        next_member = None
        if len(minimum_chat_handler) != 1:
            # Find the oldest support member(s) with the minimum number of chats
            oldest_time_distributions = [x for x in self.cso_id_chatamt_timestamp if x['num_of_chats'] == minimum_chat_handler['num_of_chats']]
            oldest_time_distribution = min(oldest_time_distributions, key=lambda x: x['time'])
            if oldest_time_distribution != 1:
                next_member = oldest_time_distribution['id']
            else: 
                next_member = oldest_time_distribution['id']
        else: 
            next_member = minimum_chat_handler['id']
        
        # If the member is already at the max chats, return None
        if minimum_chat_handler['num_of_chats'] >= self.max_amt_of_chats_per_member:
            return None
        
        # Increment the number of chats for the support member
        minimum_chat_handler['num_of_chats'] += 1
        
        # Return the support member that will handle the new chat
        return next_member

# data = [
#     {"time": "2023-02-20 10:01:00", "id": "user1", "num_of_chats": 3 }, 
#     {"time": "2023-02-20 10:01:00", "id": "user2", "num_of_chats": 4 },    
#     {"time": "2023-02-20 10:02:00", "id": "user3", "num_of_chats": 2 },    
#     {"time": "2023-02-20 10:03:00", "id": "user4", "num_of_chats": 2 },    
#     {"time": "2023-02-20 10:05:00", "id": "user5", "num_of_chats": 5 }
# ]

# NCD = NewCustomerDistribution(amt_of_members=5, max_amt_of_chats_per_member=5, cso_id_chatamt_timestamp=data)
# print(NCD.add_new_chat())  # user5
# print(NCD.add_new_chat())  # user5 (user5 is at max chats)
# # NCD.cso_id_chatamt_timestamp[0]['num_of_chats'] = 0  # reset user1's chats
# print(NCD.add_new_chat())  # user1