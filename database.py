# This file contains the code for the database

stats_df_columns = [
    "msg_total", "msg_chars_avg", "msg_words_avg", "msg_chars_max", "msg_words_max", 
    "media_total", "images", "videos", "gifs", "stickers", "audios",
    "contacts", "locations", "files", "deleted", "missed", 
    "links", "emojis", "emoji_unique"]

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
    "links":("","repl","https?:\/\/\S+", "xURLx")}

senders = list()
stats_df = []
