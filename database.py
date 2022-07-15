# ----------------------------------------------------------------
# This file contains dictionaries, list and placeholders for the statistics
# which will be derived from the chat
# ----------------------------------------------------------------

test_data = ["data/input/chat_small.txt", "data/input/chat_mum.txt", "data/input/chat_mum.zip", "data/input/tash.trash", "data/input/chat_AB.txt", "data/input/_chat.txt"]

df_cols = ["datetime", "sender", "message", "polarity", "emojis",  "emoji_count", "url_count"]

cstats_cols = [("msg_count", "message"), ("chars_avg", "character"), ("words_avg", "word"),  ("chars_max", "character"), ("words_max", "word"), ("polarity_avg", "polarity"),  ("media_count", "media"), "image", "video", "GIF", "sticker", "audio", "contact", "location", "file", ("deleted", "message"), ("missed", "(video)call"), "link", "emoji", "emoji_unique"]

cstats_match = {
	"audio": ("exact", "‎audio omitted"),
	"image": ("exact", "‎image omitted"),
	"video": ("exact", "‎video omitted"),
	"sticker": ("exact", "‎sticker omitted"),
	"GIF": ("exact", "‎GIF omitted"),
	"location": ("", "‎Location: xURL"),
	"file": ("", "‎document omitted"),
	"contact": ("exact", "‎Contact card omitted"),
	"media_count": "",
	"missed": ("", "‎Missed "),
	"deleted": ("", "‎You deleted |‎This message was deleted."),
	"rest": ("", "‎")}

stopwords = ["ich", "du", "und", "der", "die", "das", "ist", "nicht", "sich", "mit", "wie", "an", "auf", "aus", "bei", "bis", "bist", "da", "dann", "das", "dass", "dein", "deine", "dem", "den", "der", "des", "dessen", "dich", "dir", "doch", "dort", "durch", "ein", "eine", "einem", "einen", "einer", "eines", "einmal", "er", "es", "etwas", "für", "gegen", "habe", "haben", "hat", "hatte", "hatten", "hier", "hin", "hinter", "ich", "ihr", "ihre", "im", "in", "indem", "ins", "ist", "jede", "jedem", "jeden", "jeder", "jedes", "jene", "jenem", "jenen", "jener", "jenes", "jetzt", "kann", "kannst", "können", "könnt", "machen", "mein", "meine", "meinst", "meinst", "mich", "mir", "mit", "muss", "müssen", "musst", "nach", "nicht", "nichts", "noch", "nun", "nur", "ob", "oder", "ohne", "seid", "seien", "seinem", "sein", "seine", "seinst", "seinst", "sich", "sie", "sind", "soll", "sollen", "sollst", "sollt", "sollte", "sollten", "solltest", "sonst", "soweit", "über", "überhaupt", "übrigens", "unter", "viel", "viele", "vom", "von", "vor", "wann", "war", "waren", "warst", "wart", "warum", "was", "weg", "wegen", "weil", "we"]


# the actual data will be stored in the following variables

senders = list()
cwords_df = list()

cstats_df = list()
""" 0: msg_count, 1: chars_avg, 2: words_avg, 3: chars_max, 4: words_max, 5: polarity_avg, 6: media_count, 7: image, 8: video, 9: GIF, 10: sticker, 11: audio, 12: contact, 13: location, 14: file, 15: deleted, 16: missed, 17: link, 18: emoji, 19: emoji_unique"""

chat = list()
"""[datetime, sender, message, polarity, emojis, emoji_count, url_count]"""

def export() -> None:
	"""
	Export the main database dataframes to csv files
	"""
	chat.to_csv("data/testing/output/database/chat_df.csv", index=True)
	cstats_df.to_csv("data/testing/output/database/cstats_df.csv", index=True)
	# cwords_df.to_csv("data/testing/output/database/cwords_df.csv", index=True)