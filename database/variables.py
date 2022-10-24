from html import entities
import pandas as pd

# ------------------------------------------------------------------------------
#        the derived data will be stored in the following variables
# ------------------------------------------------------------------------------

last_txt_size = 11

chat: pd.DataFrame = pd.DataFrame()
"""
Filled automatically by program: clean chat
[date, datetime, sender, message, sentiment]
"""

chat_og: pd.DataFrame = pd.DataFrame()
"""
Filled automatically by program: original chat
[date, datetime, sender, message, sentiment]
"""

stats: pd.DataFrame = pd.DataFrame()
"""
Filled automatically by program: statistics
0: msg_count, 1: chars_avg, 2: words_avg, 3: chars_max, 4: words_max, 5: polarity_avg, 6: media, 7: image, 8: video, 9: GIF, 10: sticker, 11: audio, 12: contact, 13: location, 14: file, 15: deleted, 16: calls, 17: link, 18: emoji, 19: emoji_unique, 20: sent_pos, 21: sent_neg
"""

time_stats: pd.DataFrame = pd.DataFrame()
"""
Filled automatically by program: time statistics
0: first_msg, 1: last_mgs, 2: max_day, 3: max_msg, 4: msg_days, 5: zero_days, 6: msg_span_days, 7: max_no_msg_span, 8: avg_no_msg_span, 9: avg_msg_per_day
"""

nlp_stats: pd.DataFrame = pd.DataFrame()
"""
Filled automatically by program: nlp statistics
0: words, 1: lemmas, 2: stopwords, 3: words_clean, 4: unique_words, 5: unique_lemmas, 6: unique_stopwords, 7: unique_clean_words, 8: avg_word_len, *POS_TAGS
"""

sender: list[str] = list()
"""
Filled automatically by program: sender names
[first sender, second sender, ...]
"""

sc: int = int()
"""
Filled automatically by program: sender count
"""

msg_ranges = list()
"""
Filled automatically by program: message ranges per
[[first sender: start, end], [second sender: start, end], ...]
"""

txt_reports: list[str] = list()
"""
Filled automatically by program: text reports
[stats for first sender, stats for second sender, ..., general stats]
"""

time_reports: list[str] = list()
"""
Filled automatically by program: text time reports
[stats for first sender, stats for second sender, ..., general stats]
"""

nlp_reports: list[str] = list()
"""
Filled automatically by program: text nlp reports
[stats for first sender, stats for second sender, ..., general stats]
"""

ts = list()
"""
Filled automatically by program: timestamps
"""

msg_per_s = list()
"""
Filled automatically by program: messages per sender
[messages first sender, messages second sender, ..., sc: all messages]
"""

common_emojis = list()
"""
Filled automatically by program: emojis frequencies per sender
[common emojis of first sender, common emojis of second sender, ...]
"""

frequencies = list()
"""
Filled automatically by program: different frequencies per sender
[[words, lemmas, stop_words words_clean frequency DataFrames of first sender], ...]
"""

named_entities = list()
"""
Filled automatically by program: list of entities dicts with named entities
[{label1: [all entities of first sender, label2: [all entities of first sender, ...}, ...]
"""

named_entities_counts = list()
"""
Filled automatically by program: list of counts of named entities per sender
[0: count for first sender, 1: count for second sender, ...]
"""

pos_tags = list()
"""
Filled automatically by program: list of pos tag dicts per sender
[0: pos tags for first sender, 1: pos tags for second sender, ...]
"""

all_msgs_clean = list()
"""
Filled automatically by program: list of all messages per sender as string
[0: messages of first sender, 1: messages of second sender, ...]
"""

all_msgs = str()
"""
Filled automatically by program: string of all messages
"""

word_counts = list()
"""
Filled automatically by program: list of word counts per sender
[0: word counts of first sender, 1: word counts of second sender, ...]
"""

char_counts = list()
"""
Filled automatically by program: list of character counts per sender
[0: char counts of first sender, 1: char counts of second sender, ...]
"""
