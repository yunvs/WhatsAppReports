# ------------------------------------------------------------------------------
# 		This file contains constants that will be used in the program
# ------------------------------------------------------------------------------


STATS_PATTERN = {
	"audio": ("exact", "‎audio omitted"),
	"image": ("exact", "‎image omitted"),
	"video": ("exact", "‎video omitted"),
	"sticker": ("exact", "‎sticker omitted"),
	"GIF": ("exact", "‎GIF omitted"),
	"location": ("", "‎Location: xURL"),
	"file": ("", "‎document omitted"),
	"contact": ("exact", "‎Contact card omitted"),
	"media": ("", ""),
	"calls": ("", "‎Missed "),
	"deleted": ("", "‎You deleted |‎This message was deleted."),
	"rest": ("", "‎"),
}
""" Dictionary of media types and their corresponding patterns """

STATS_DICT = {
	"msg_count": "text",
	"chars_avg": "char",
	"words_avg": "word",
	"chars_max": "char",
	"words_max": "word",
	"sent_avg": "sentiment",
	"media": "media",
	"image": "image",
	"video": "video",
	"GIF": "GIF",
	"sticker": "sticker",
	"audio": "audio",
	"contact": "contact",
	"location": "location",
	"file": "file",
	"deleted": "message",
	"calls": "video/audio call",
	"link": "link",
	"emoji": "emoji",
	"emoji_unique": "distinct emoji",
	"sent_pos": "positive message",
	"sent_neg": "negative message",
}
""" Dictionary of statistics and their corresponding names """


HOURS = [
	"0",
	"1",
	"2",
	"3",
	"4",
	"5",
	"6",
	"7",
	"8",
	"9",
	"10",
	"11",
	"12",
	"13",
	"14",
	"15",
	"16",
	"17",
	"18",
	"19",
	"20",
	"21",
	"22",
	"23",
]
""" List of hours of the day """

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
""" List of days of the week """

MONTHS = [
	"January",
	"February",
	"March",
	"April",
	"May",
	"June",
	"July",
	"August",
	"September",
	"October",
	"November",
	"December",
]
""" List of months of the year """

TIME_STATS_COLS = [
	"first_msg",
	"last_msg",
	"max_day",
	"max_msg",
	"msg_days",
	"zero_days",
	"msg_span_days",
	"max_no_msg_span",
	"avg_no_msg_span",
	"msg_per_day",
	"avg_msg_per_day",
]
""" List of time statistics column names """


POS_TAGS = {
	"ADJ": "Adjective",
	"ADP": "Adposition",
	"ADV": "Adverb",
	"AUX": "Auxiliary",
	"CCONJ": "Coordinating conjunction",
	"DET": "Determiner",
	"INTJ": "Interjection",
	"NOUN": "Noun",
	"NUM": "Numeral",
	"PART": "Particle",
	"PRON": "Pronoun",
	"PROPN": "Proper noun",
	"PUNCT": "Punctuation",
	"SCONJ": "Subordinating conjunction",
	"SYM": "Symbol",
	"VERB": "Verb",
	"X": "Other",
}
""" Dictionary of POS tags and their corresponding names (pos_tag: name) """

NER_TAGS = {
	"LOC": "Locations",
	"MISC": "Miscellaneous entities",
	"ORG": "Companies/organizations",
	"PER": "Named person/family",
}
""" Dictionary of NER tags and their corresponding names (ner_tag: name) """

NLP_STATS_COLS = [
	"words",
	"lemmas",
	"stopwords",
	"words_clean",
	"unique_words",
	"unique_lemmas",
	"unique_stopwords",
	"unique_clean_words",
	"avg_word_len",
]
""" List of NLP statistics column names """
