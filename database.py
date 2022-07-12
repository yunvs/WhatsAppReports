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


test_data = ["data/chat_small.txt", "data/chat_mum.txt", "data/chat_mum.zip",
             "tash.trash", "data/chat_AB.txt", "data/_chat.txt"]


stats_matches = {
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


senders = list()
stats_df = []
"""
0: msg_total, 1: msg_chars_avg, 2: msg_words_avg, 3: msg_chars_max, 
4: msg_words_max, 5: media_total, 6: image, 7: video, 8: GIF, 
9: sticker, 10: audio, 11: contact, 12: location, 13: file, 14: deleted, 
15: missed, 16: link, 17: emoji, 18: emoji_unique
"""


chat = []
"""[datetime, sender, message, emojis, emoji_count, url_count]"""


ouput_check = [
    """
	Test""",
    """
	WA-Report for Meral Renz:
	Meral Renz sent 829 messages, 261 emojis and 323 media in this chat.
	A average message is 33.4 characters long and contains 6.4 words.
	The longest message they sent contained 2154 characters and 329 words.
	Meral Renz sent 2 audios, 273 images, 35 videos, 10 stickers and 3 GIFs.
	They shared 21 contacts, 7 locations, 6 files and 121 links.
	Meral Renz changed their mind one time and deleted a message.
	You missed 125 (video)calls by Meral Renz.

	WA-Report for Yunus:
	Yunus sent 731 messages, 85 emojis and 259 media in this chat.
	A average message is 24.5 characters long and contains 5.2 words.
	The longest message they sent contained 975 characters and 191 words.
	Yunus sent 19 audios, 198 images, 30 videos, 12 stickers and not a single GIF.
	They shared 2 contacts, 7 locations, 4 files and 26 links.
	Yunus changed their mind 6 times and deleted a message.""",
    """
	Test"""]
