# This file contains the code for the database

stats_df_columns = [
    "msg_total", "msg_chars_avg", "msg_words_avg", "msg_chars_max", "msg_words_max", 
    "media_total", "image", "video", "GIF", "sticker", "audio",
    "contact", "location", "file", "deleted", "missed", 
    "link", "emoji", "emoji_unique"]

"""
0: msg_total, 1: msg_chars_avg, 2: msg_words_avg, 3: msg_chars_max, 
4: msg_words_max, 5: media_total, 6: image, 7: video, 8: GIF, 
9: sticker, 10: audio, 11: contact, 12: location, 13: file, 14: deleted, 
15: missed, 16: link, 17: emoji, 18: emoji_unique
"""

stats_matches = {
    "audio":("=","x","‎audio omitted"), 
    "image":("=","x","‎image omitted"), 
    "video":("=","x","‎video omitted"), 
    "sticker":("=","x","‎sticker omitted"), 
    "GIF":("=","x","‎GIF omitted"),
    "media_total":"",
    "missed":("","x","‎Missed "), 
    "deleted":("","x","‎You deleted |‎This message was deleted."), 
    "location":("","x","‎Location: xURL"), 
    "file":("","x","‎document omitted"), 
    "contact":("=","x","‎Contact card omitted"),
    "rest":("","x","‎")}


senders = list()
stats_df = []
