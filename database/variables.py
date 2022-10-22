import pandas as pd

# ------------------------------------------------------------------------------
#        the derived data will be stored in the following variables
# ------------------------------------------------------------------------------

last_txt_size = 11

chat: pd.DataFrame = pd.DataFrame()
"""
Will be filled by program automatically: clean chat
[date, datetime, sender, message, sentiment]
"""

chat_og: pd.DataFrame = pd.DataFrame()
"""
Will be filled by program automatically: original chat
[date, datetime, sender, message, sentiment]
"""

stats: pd.DataFrame = pd.DataFrame()
"""
Will be filled by program automatically: statistics
0: msg_count, 1: chars_avg, 2: words_avg, 3: chars_max, 4: words_max, 5: polarity_avg, 6: media, 7: image, 8: video, 9: GIF, 10: sticker, 11: audio, 12: contact, 13: location, 14: file, 15: deleted, 16: calls, 17: link, 18: emoji, 19: emoji_unique, 20: sent_pos, 21: sent_neg
"""

tstats: pd.DataFrame = pd.DataFrame()
"""
Will be filled by program automatically: time statistics
0: first_msg, 1: last_mgs, 2: max_day, 3: max_msg, 3: msg_days, 4: zero_days, 5: msg_span_days, 6: no_msg_span
"""

sender: list[str] = list()
"""
Will be filled by program automatically: list of all senders
"""

sc: int = int()
"""
Will be filled by program automatically: sender count
"""
msg_ranges = list()
"""
Will be filled by program automatically: list of message ranges
[start, end]
"""

txt_reports: list[str] = list()
"""
Will be filled by program automatically: list of text reports
[0: sender_no0, 1: sender_no1, ..., sc: general]
"""

time_reports: list[str] = list()
"""
Will be filled by program automatically: list of time reports
[0: sender_no1, 1: sender_no2, ..., sc: general]
"""

ts = list()
"""
Will be filled by program automatically: list of timestamps
"""

msg_per_s = list()
"""
Will be filled by program automatically: list of messages per sender
[0: messages sender_no1, 1: messages sender_no2, ..., sc: all messages]
"""

common_words = list()
"""
Will be filled by program automatically: word frequencies per sender
[0: common words of first sender, 1: common words of second sender, ...]
"""

common_emojis = list()
"""
Will be filled by program automatically: emojis frequencies per sender
[0: common emojis of first sender, 1: common emojis of second sender, ...]
"""

all_msgs_clean = list()
"""
Will be filled by program automatically: list of all messages per sender as string
[0: messages of first sender, 1: messages of second sender, ...]
"""

all_msgs = str()
"""
Will be filled by program automatically: string of all messages
"""

word_counts = list()
"""
Will be filled by program automatically: list of word counts per sender
[0: word counts of first sender, 1: word counts of second sender, ...]
"""

char_count = list()
"""
Will be filled by program automatically: list of character counts per sender
[0: char counts of first sender, 1: char counts of second sender, ...]
"""
