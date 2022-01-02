import matplotlib.pyplot as plt
import calendar
from scraper.connections import *

def repository_creation_speed(tag):
    repo_creation_log = get_cursor(f"SELECT full_name, recorded_on, repository_score FROM repos WHERE tag='{tag}' AND repository_score>0 ORDER BY recorded_on  ASC")
    duplicates = {}
    x = []
    repo_found = []
    score = []
    creation_speed = []
    timeline =[]
    new_repo = 0
    for event_log in repo_creation_log:
        try:
            duplicates[event_log[0]] += 1
        except:
            duplicates[event_log[0]] = 1
            new_repo +=1
            x.append(calendar.timegm(event_log[1].timetuple()))
            repo_found.append(new_repo)
            try:
                creation_speed.append((new_repo-max(0, new_repo - 100))/(calendar.timegm(event_log[1].timetuple())-x[max(0, new_repo-100)]))
            except Exception as ex:
                creation_speed.append(0)
                print(ex)
            score.append((event_log[2]))
            timeline.append((calendar.timegm(event_log[1].timetuple()) - x[0])/3600)

    plt.figure(figsize=(10,60))
    plt.subplot(2,1,1)
    plt.title(f"Repository discovery speed (Score>5)\n{tag}\n", fontdict = {'fontsize' : 14, 'weight' : 'bold'})
    plt.plot(timeline, creation_speed, linewidth=1.0)
    plt.xlabel(f"New repositories discovered per second (average = {'{:.2f}'.format(sum(creation_speed)/len(score))}/s)")
    plt.subplot(2,1,2)
    plt.hist(score, 100, density=1, facecolor='g', alpha=0.75)
    plt.xlabel(f"Repository score distribution (average = {'{:.2f}'.format(sum(score)/len(score))})")
    plt.yticks([])
    plt.subplots_adjust(hspace = 0.3)
    plt.show()

repository_creation_speed("Classic sequence probability vector [0.1,0.1,0.1,0.2,0.2,0.2,0.1]")
#repository_creation_speed("Reference repositories")
