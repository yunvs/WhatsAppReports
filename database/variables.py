import pandas as pd

# ------------------------------------------------------------------------------
#        the derived data will be stored in the following variables
# ------------------------------------------------------------------------------

last_txt_size = 11

chat: pd.DataFrame = pd.DataFrame()
"""
Will be filled by program automatically
[date, datetime, sender, message, sentiment] 
"""

chat_og: pd.DataFrame = pd.DataFrame()
"""
Will be filled by program automatically
[date, datetime, sender, message, sentiment] 
"""

stats: pd.DataFrame = pd.DataFrame()
"""
Will be filled by program automatically
0: msg_count, 1: chars_avg, 2: words_avg, 3: chars_max, 4: words_max, 5: polarity_avg, 6: media, 7: image, 8: video, 9: GIF, 10: sticker, 11: audio, 12: contact, 13: location, 14: file, 15: deleted, 16: calls, 17: link, 18: emoji, 19: emoji_unique 
"""

tstats: pd.DataFrame = pd.DataFrame()
"""
Will be filled by program automatically
0: first_msg, 1: last_mgs, 2: most_msg, 3: no_msg, 4: break 
"""

sender: list[str] = list()
"""
Will be filled by program automatically
list of all senders 
"""

sc: int = int()
"""
Will be filled by program automatically
count of senders 
"""
msg_ranges = list()
"""
Will be filled by program automatically
[start, end] 
"""

txt_reports: list[str] = list()
"""
Will be filled by program automatically
list contains text reports (general and per sender) 
"""

time_reports: list[str] = list()
"""
Will be filled by program automatically
list contains text reports about time (general and per sender) 
"""

ts = list()
"""
Will be filled by program automatically
list of timestamps 
"""

msg_per_s = list()
"""
Will be filled by program automatically
Messages per sender [0: messages from sender no.1, 1: messages of sender no.2, ... sc: messages of all senders] 
"""

common_words = list()
"""
Will be filled by program automatically
word frequencies per sender [0: common words of first sender, 1: common words of second sender, ...] 
"""

common_emojis = list()
"""
Will be filled by program automatically
emojis frequencies per sender [0: common emojis of first sender, 1: common emojis of second sender, ...] 
"""
