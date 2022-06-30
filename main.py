from myfunctions import *


paths = ["data/chat_small.txt", "data/chat_mum.txt", "data/chat_mum.zip", "tash.trash", "data/chat_AB.txt"]
path_to_file = paths[2] # 0: small, 1: mum.zip, 2: mum.txt, 3: trash, 4: AB

contents = get_content(path_to_file) # get the content of the filepath
chat_history = chats_to_list(contents) # convert the chat history to a list of all messages 
# Format: [ [[date, time], sender, message], [[date, time], sender, message], … ]
sender_texts = chats_per_sender(chat_history) # divide the chat history into a list of lists, where each list contains all messages from a sender # [ [all messages from first sender], [all messages from next sender], … ]

chats_per_senders = chats_per_sender(chat_history)
amount_senders = len(chats_per_senders)

for i in range(amount_senders):
    globals()['chats_sender'+str(i)] = chats_per_senders[i]


print(chats_per_senders[0][0])
print(chats_per_senders[1][0])









print(f"")