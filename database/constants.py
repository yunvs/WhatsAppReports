from nltk.corpus import stopwords

# ----------------------------------------------------------------
# This file contains dictionaries, list for the statistics
# which will be derived from the chat
# ----------------------------------------------------------------

STATS_DICT = {"msg_count": "text", "chars_avg": "char", "words_avg": "word", "chars_max": "char", "words_max": "word", "sent_avg": "sentiment", "media": "media", "image": "image", "video": "video", "GIF": "GIF", "sticker": "sticker", "audio": "audio", "contact": "contact", "location": "location", "file": "file", "deleted": "message", "calls": "video/audio call", "link": "link", "emoji": "emoji", "emoji_unique": "distinct emoji", "sent_pos": "positve message", "sent_neg": "negative message"}
""" Dictionary of statistics and their corresponding names """

STATS_PATTERN = {"audio": ("exact", "‎audio omitted"), "image": ("exact", "‎image omitted"), "video": ("exact", "‎video omitted"), "sticker": ("exact", "‎sticker omitted"), "GIF": ("exact", "‎GIF omitted"), "location": ("", "‎Location: xURL"), "file": ("", "‎document omitted"), "contact": ("exact", "‎Contact card omitted"), "media": ("", ""), "calls": ("", "‎Missed "), "deleted": ("", "‎You deleted |‎This message was deleted."), "rest": ("", "‎")}
""" Dictionary of media types and their corresponding patterns """

STOP_WORDS = [word.upper() for word in set(stopwords.words("german") + ["ich", "du", "und", "der", "die", "das", "ist", "nicht", "sich", "mit", "wie", "an", "auf", "aus", "bei", "bis", "bist", "da", "dann", "das", "dass", "dein", "deine", "dem", "den", "der", "des", "dessen", "dich", "dir", "doch", "dort", "durch", "ein", "eine", "einem", "einen", "einer", "eines", "einmal", "er", "es", "etwas", "für", "gegen", "habe", "haben", "hat", "hatte", "hatten", "hier", "hin", "hinter", "ich", "ihr", "ihre", "im", "in", "indem", "ins", "ist", "jede", "jedem", "jeden", "jeder", "jedes", "jene", "jenem", "jenen", "jener", "jenes", "jetzt", "kann", "kannst", "können", "könnt", "machen", "mein", "meine", "meinst", "meinst", "mich", "mir", "mit", "muss", "müssen", "musst", "nach", "nicht", "nichts", "noch", "nun", "nur", "ob", "oder", "ohne", "seid", "seien", "seinem", "sein", "seine", "seinst", "seinst", "sich", "sie", "sind", "soll", "sollen", "sollst", "sollt", "sollte", "sollten", "solltest", "sonst", "soweit", "über", "überhaupt", "übrigens", "unter", "viel", "viele", "vom", "von", "vor", "wann", "war", "waren", "warst", "wart", "warum", "was", "weg", "wegen", "weil"])]
""" List of stopwords for the wordclouds """
