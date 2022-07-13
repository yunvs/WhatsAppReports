
# ----------------------------------------------------------------
# This file contains dictionaries, list and placeholders for the statistics
# which will be derived from the chat
# ----------------------------------------------------------------

test_data = ["data/imports/chat_small.txt", "data/imports/chat_mum.txt", 
                "data/imports/chat_mum.zip", "data/imports/tash.trash", 
                "data/imports/chat_AB.txt", "data/imports/_chat.txt"]

cstats_cols = [
    "msg_total", "msg_chars_avg", "msg_words_avg", "msg_chars_max", "msg_words_max",
    "media_total", "image", "video", "GIF", "sticker", "audio",
    "contact", "location", "file", "deleted", "missed",
    "link", "emoji", "emoji_unique"]

cstats_match = {
    "audio": ("=", "x", "‎audio omitted"),
    "image": ("=", "x", "‎image omitted"),
    "video": ("=", "x", "‎video omitted"),
    "sticker": ("=", "x", "‎sticker omitted"),
    "GIF": ("=", "x", "‎GIF omitted"),
    "media_total": "",
    "missed": ("", "x", "‎Missed "),
    "deleted": ("", "x", "‎You deleted |‎This message was deleted."),
    "location": ("", "x", "‎Location: xURL"),
    "file": ("", "x", "‎document omitted"),
    "contact": ("=", "x", "‎Contact card omitted"),
    "rest": ("", "x", "‎")}



# the actual data will be stored in the following variables

senders = list()
cwords_df = list()

cstats_df = list()
""" 0: msg_total, 1: msg_chars_avg, 2: msg_words_avg, 3: msg_chars_max,
4: msg_words_max, 5: media_total, 6: image, 7: video, 8: GIF, 9: sticker, 
10: audio, 11: contact, 12: location, 13: file, 14: deleted, 15: missed, 
16: link, 17: emoji, 18: emoji_unique """

chat = list()
"""[datetime, sender, message, emojis, emoji_count, url_count] """


def export() -> None:
    """
    Export the main database dataframes to csv files
    """
    chat.to_csv("data/output/database/chat_df.csv", index=True)
    cstats_df.to_csv("data/output/database/cstats_df.csv", index=True)
    cwords_df.to_csv("data/output/database/cwords_df.csv", index=True)