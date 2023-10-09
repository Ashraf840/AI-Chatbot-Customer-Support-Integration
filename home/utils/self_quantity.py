import random
import time

class NewCustomerDistribution:
    def __init__(self, amt_of_members, max_amt_of_chats_per_member, cso_id_chatamt_timestamp):
        self.amt_of_members = amt_of_members
        self.max_amt_of_chats_per_member = max_amt_of_chats_per_member
        self.cso_id_chatamt_timestamp = cso_id_chatamt_timestamp
        self.last_assigned_time = time.time()
    
    def add_new_chat(self):
        current_time = time.time()
        if current_time - self.last_assigned_time >= 60:
            return None
        
        minimum_chat_handler = min(self.cso_id_chatamt_timestamp, key=lambda x: x['num_of_chats'])
        next_member = None
        if len(minimum_chat_handler) != 1:
            oldest_time_distributions = [x for x in self.cso_id_chatamt_timestamp if x['num_of_chats'] == minimum_chat_handler['num_of_chats']]
            oldest_time_distribution = min(oldest_time_distributions, key=lambda x: x['time'])
            if oldest_time_distribution != 1:
                next_member = oldest_time_distribution['id']
            else: 
                next_member = oldest_time_distribution['id']
        else: 
            next_member = minimum_chat_handler['id']
        
        if minimum_chat_handler['num_of_chats'] >= self.max_amt_of_chats_per_member:
            return None
        
        minimum_chat_handler['num_of_chats'] += 1
        
        self.last_assigned_time = time.time()
        
        return next_member
