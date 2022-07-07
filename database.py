# This file contains the code for the database

stats_df_columns = [
    "msg_total", "msg_chars_avg", "msg_words_avg", "msg_chars_max", "msg_words_max", 
    "media_total", "images", "videos", "gifs", "stickers", "audios",
    "contacts", "locations", "files", "deleted", "missed", 
    "links", "emojis", "emoji_unique"]
"""
0: msg_total, 1: msg_chars_avg, 2: msg_words_avg, 3: msg_chars_max, 
4: msg_words_max, 5: media_total, 6: images, 7: videos, 8: gifs, 
9: stickers, 10: audios, 11: contacts, 12: locations, 13: files, 14: deleted, 
15: missed, 16: links, 17: emojis, 18: emoji_unique, 
"""

stats_matches = {
    "audios":("=","x","‎audio omitted"), 
    "images":("=","x","‎image omitted"), 
    "videos":("=","x","‎video omitted"), 
    "stickers":("=","x","‎sticker omitted"), 
    "gifs":("=","x","‎GIF omitted"),
    "media_total":("media"),
    "missed":("","x","‎Missed "), 
    "deleted":("","x","‎You deleted |‎This message was deleted."), 
    "locations":("","x","‎Location: "), 
    "files":("","x","‎document omitted"), 
    "contacts":("=","x","‎Contact card omitted"),
    "rest":("","x","‎"),
    "links":("","repl","https?:\/\/\S+", "xURL")}

senders = list()
stats_df = []
