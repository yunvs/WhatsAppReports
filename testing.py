# from timeit import default_timer as timer
from myfuncs import *
from matplotlib import cm
# import database as db
import numpy as np
# # ----------------------------------------------------------------
stats_df = pd.read_csv("data/testing/exports/database/stats_df.csv", index_col=0)
senders = list(pd.read_csv("data/testing/exports/database/senders_df.csv", index_col=0)["0"])
msg = stats_df.iloc[0:-1, 0]
# # ----------------------------------------------------------------
# Testing Area:
data = []
for i in range(len(senders)):
	data.append([stats_df.iloc[i,0], stats_df.iloc[i,6]])
data = np.array(data)
print(data)


# # ----------------------------------------------------------------
fig, ax = plt.subplots()

# cmap = plt.colormaps["tab20c"]
# outer_colors = cmap(np.arange(3)*4)
# inner_colors = cmap([1  , 2, 5, 6, 9, 10])

# ax.pie(msg, startangle=90, counterclock=False, autopct="%1.1f%%", wedgeprops={"ec": "w"}, colors=cm_colors("Greens_r", db.senders))

colors = cmap("Greens_r", db.senders)
aplha_colors = colors[:, 3] = 0.8

ax.pie(data.sum(axis=1), radius=1, colors=colors, wedgeprops=dict(width=0.3, edgecolor='w'))
ax.legend(labels=db.senders, title="Sender:", shadow=True, loc="best", markerfirst=False)

# ax.pie(data.flatten(), radius=1-0.3, colors=aplha_colors, wedgeprops=dict(width=0.3, edgecolor='w'))

ax.set(aspect="equal", title='Pie plot with `ax.pie`')
plt.show()







# fig, ax = plt.subplots()

# vals = np.array([[60., 32.], [37., 40.], [29., 10.]])


# cmap = cm.get_cmap('Greens')
# outer_colors = cmap(np.arange(3)*4)
# inner_colors = cmap([1, 2, 5, 6, 9, 10])

# ax.pie(vals.sum(axis=1), radius=1, colors=outer_colors,
# 	   wedgeprops=dict(width=0.3, edgecolor='w'))

# ax.pie(vals.flatten(), radius=1-0.3, colors=inner_colors,
# 	   wedgeprops=dict(width=0.3, edgecolor='w'))

# ax.set(aspect="equal", title='Pie plot with `ax.pie`')
# plt.show()

# stat = "messages_max"
# if "max" in stat or "unique" in stat or "calls" in stat:
# 	print("Yesss")
# else:
# 	print("Nooo")



# last_sizes = [-100]
# size = 10

# last_sizes.append(size) if size != 0 else None
# size = last_sizes[-1] if size == 0 else size


# print(f"last_sizes: {last_sizes}, size: {size}")

# def new_section(space: int=0, size: int=db.last_size[-1], style: str="") -> None:
# 	db.last_size.append(size)
# 	print(f"space: {space}, size: {size}, style: {style}")

# new_section(20)
# new_section(20, 10, "B")
# new_section(20)



# print(GREEN("testing started"))
# t = [timer()]


# def cm_colors(cm_name: str, countable):
# 	if type(countable) != int:
# 		countable = len(countable)
# 	return cm.get_cmap(cm_name)(np.linspace(.2, .8, countable+1))


# # Piechart Message per senders
# # plt.pie(stats_df.iloc[0:-1, 0], startangle=90, counterclock=False, autopct="%1.1f%%", wedgeprops={"ec": "w"}, colors=cm_colors("Greens_r", senders))
# # plt.legend(labels=senders, title="Sender:", shadow=True, loc="center left", bbox_to_anchor=(1, .5))
# # plt.show()

i=0
# Piechart with bar types of messages

# pie chart parameters

plt.pie(data, autopct="%1.1f%%", startangle=0, counterclock=False,
        	labels=["Media","Messages"], explode=[.1, 0], colors=cmap("YIGn", 2))

# bar chart parameters
age_ratios = stats_df.iloc[i, 7:14]
age_labels = ["Images", "Videos", "GIFs", "Sticker", "Audios", "Contacts", "Locations", "Files"]
print(age_ratios)


plt.show()




# # ----------------------------------------------------------------
# t.append(timer())
# print(GREEN(f"\n testing took {t[-1] - t[-2]} seconds"))
# # ----------------------------------------------------------------