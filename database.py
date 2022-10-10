import pandas as pd
from nltk.corpus import stopwords

# ----------------------------------------------------------------
# This file contains dictionaries, list and placeholders for the statistics
# which will be derived from the chat
# ----------------------------------------------------------------

test_data = ["data/input/chat_small.txt", "data/input/chat_mum.txt", "data/input/chat_mum.zip", "data/input/tash.trash", "data/input/chat_AB.txt", "data/input/_chat.txt"] #TODO remove finally
""" List of paths to test data 1: small, 2: txt, 3: zip, 4: trash, 5: AB, 6: _chat.txt """

df_cols = ["date", "datetime", "sender", "message", "sentiment"]
""" List of column names for the DataFrame """

stats_dict = {
	"msg_count": "message", 		"chars_avg": "char", 
	"words_avg": "word", 			"chars_max": "char", 
	"words_max": "word", 			"sent_avg": "sentiment", 
	"media_count": "media", 		"image": "image", 
	"video": "video", 				"GIF": "GIF", 
	"sticker": "sticker", 			"audio": "audio", 
	"contact": "contact", 			"location": "location", 
	"file": "file", 				"deleted": "message", 
	"calls": "video/audio call",	"link": "link", 
	"emoji": "emoji", 				"emoji_unique": "emoji",
	"sent_pos": "positve message",	"sent_neu": "neutral message",
	"sent_neg": "negative message",	"sent_nan": "message",}
""" .keys() = [msg_count, chars_avg, words_avg, chars_max, words_max, sent_avg, media_count, image, video, GIF, sticker, audio, contact, location, file, deleted, calls, link, emoji, emoji_unique, sent_pos, sent_neu, sent_neg, sent_nan] """ #TODO remove finally
""" Dictionary of statistics and their corresponding names """


cstats_match: dict[str, tuple[str, str]] = {
	"audio": ("exact", "‎audio omitted"),
	"image": ("exact", "‎image omitted"),
	"video": ("exact", "‎video omitted"),
	"sticker": ("exact", "‎sticker omitted"),
	"GIF": ("exact", "‎GIF omitted"),
	"location": ("", "‎Location: xURL"),
	"file": ("", "‎document omitted"),
	"contact": ("exact", "‎Contact card omitted"),
	"media_count": ("", ""),
	"calls": ("", "‎Missed "),
	"deleted": ("", "‎You deleted |‎This message was deleted."),
	"rest": ("", "‎")}
""" Dictionary of media types and their corresponding patterns """

stop_words = ["ich", "du", "und", "der", "die", "das", "ist", "nicht", "sich", "mit", "wie", "an", "auf", "aus", "bei", "bis", "bist", "da", "dann", "das", "dass", "dein", "deine", "dem", "den", "der", "des", "dessen", "dich", "dir", "doch", "dort", "durch", "ein", "eine", "einem", "einen", "einer", "eines", "einmal", "er", "es", "etwas", "für", "gegen", "habe", "haben", "hat", "hatte", "hatten", "hier", "hin", "hinter", "ich", "ihr", "ihre", "im", "in", "indem", "ins", "ist", "jede", "jedem", "jeden", "jeder", "jedes", "jene", "jenem", "jenen", "jener", "jenes", "jetzt", "kann", "kannst", "können", "könnt", "machen", "mein", "meine", "meinst", "meinst", "mich", "mir", "mit", "muss", "müssen", "musst", "nach", "nicht", "nichts", "noch", "nun", "nur", "ob", "oder", "ohne", "seid", "seien", "seinem", "sein", "seine", "seinst", "seinst", "sich", "sie", "sind", "soll", "sollen", "sollst", "sollt", "sollte", "sollten", "solltest", "sonst", "soweit", "über", "überhaupt", "übrigens", "unter", "viel", "viele", "vom", "von", "vor", "wann", "war", "waren", "warst", "wart", "warum", "was", "weg", "wegen", "weil"]
stop_words = set(stopwords.words("german") + stop_words)
stop_words = [word.upper() for word in stop_words]
""" List of stopwords for the wordclouds """

plot1_dict = {7: "Images", 8: "Videos", 9: "GIFs", 10: "Stickers", 11: "Audios", 12: "Contacts", 13: "Locations", 14: "Files"}
""" Dictionary of labels for the first plot """

time_stats_cols = ["first_msg", "last_msg", "zero_days"]
""" List of column names for the time statistics DataFrame """

# ----------------------------------------------------------------
# the actual data will be stored in the following variables
# ----------------------------------------------------------------

chat_og = pd.DataFrame()
""" #tobefilled: [date, datetime, sender, message, sentiment] """

chat = pd.DataFrame()
""" #tobefilled: [date, datetime, sender, message, sentiment] """

senders: list[str] = list()
""" #tobefilled: list of all senders """

sc: int = len(senders)
""" #tobefilled: count of senders """

chat_per_s = list()
""" #tobefilled: Chat per sender [0: chat from sender no.1, 1: chat from sender no.2, ... sc: chat from all senders] """

chat_per_s_clean = list()
""" #tobefilled: clean chat per sender [0: chat from sender no.1, 1: chat from sender no.2, ... sc: chat from all senders] """

common_words = list()
""" #tobefilled: word frequencies per sender [0: common words from first sender, 1: common words from second sender, ...] """

common_emojis = list()
""" #tobefilled: emojis frequencies per sender [0: common emojis from first sender, 1: common emojis from second sender, ...] """

stats_df = pd.DataFrame()
""" #tobefilled: 0: msg_count, 1: chars_avg, 2: words_avg, 3: chars_max, 4: words_max, 5: polarity_avg, 6: media_count, 7: image, 8: video, 9: GIF, 10: sticker, 11: audio, 12: contact, 13: location, 14: file, 15: deleted, 16: calls, 17: link, 18: emoji, 19: emoji_unique """

time_stats_df = pd.DataFrame()
""" #tobefilled: 0: first_msg, 1: last_mgs, 2: most_msg, 3: no_msg, 4: break """

msg_ranges = list()
""" #tobefilled: [start, end] """

reports: list[str] = list()
""" #tobefilled: list contains text reports (general and per sender) """

msg_bundles: list[list[str]] = list()
""" #tobefilled: list of lists containing messages bundles by each sender """

tt = pd.DataFrame()
""" #tobefilled: [task, time] """