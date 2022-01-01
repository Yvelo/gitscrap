import matplotlib.pyplot as plt
import calendar

from scraper.connections import *

repo_creation_log = get_cursor("SELECT full_name, recorded_on, repository_score FROM repos ORDER BY recorded_on  ASC")
duplicates = {}
x = []
repo_found = []
score = []
new_repo = 0
for event_log in repo_creation_log:
    try:
        duplicates[event_log[0]] += 1
    except:
        duplicates[event_log[0]] = 1
        new_repo +=1
        x.append(calendar.timegm(event_log[1].timetuple()))
        repo_found.append(new_repo)
        score.append(event_log[2]*100)

plt.style.use('_mpl-gallery')

# plot
fig, ax = plt.subplots()

ax.plot(x, repo_found, linewidth=1.0)
ax.plot(x, score, linewidth=1.0)

ax.set(xlim=(x[0], x[-1]),
       ylim=(0, new_repo))

plt.show()