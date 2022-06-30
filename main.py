from myfunctions import *


paths = ["data/chat_small.txt", "data/chat_mum.txt", "data/chat_mum.zip", "tash.trash"]
path_to_file = paths[0] # 0: small, 1: mum.zip, 2: mum.txt, 3: trash

contents = get_content(path_to_file)
chat_history = chats_to_list(contents)

print(len(chat_history))


chats_senders = chats_per_sender(chat_history)
# print(chats_senders[0])
for a in chats_senders[0]:
    if not a.startswith('m'):
        print("fuck")
for a in chats_senders[1]:
    if not a.startswith('y'):
        print("fuck")

print(len(chats_senders[0])+len(chats_senders[1]))