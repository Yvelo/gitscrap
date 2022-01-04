from scraper.rl_agent import *
import calendar

def overal_activity():
    rows=get_cursor("SELECT COUNT(full_name) as repository_count, COUNT(DISTINCT full_name) as distinc_repository_count FROM repos")
    print(f"#### Statistics for all test runs combined")
    for row in rows:
        repository_count=row[0]
        print(f"* Repositories found: {repository_count}.")
        print(f"* Distinct repositories found: {row[1]} ({'{:.1f}'.format(100*row[1]/(repository_count))} %).")
    rows = get_cursor("SELECT COUNT(full_name) as repository_count, COUNT(DISTINCT full_name) as distinc_repository_count FROM repos WHERE repository_score>3")
    for row in rows:
        print(f"* Distinct repositories with a score greater than 3: {row[1]} ({'{:.1f}'.format(100 * row[1] / (repository_count))} %).")
    rows = get_cursor("SELECT COUNT(full_name) as repository_count, COUNT(DISTINCT full_name) as distinc_repository_count FROM repos WHERE repository_score>4")
    for row in rows:
        print(f"* Distinct repositories with a score greater than 4: {row[1]} ({'{:.1f}'.format(100 * row[1] / (repository_count))} %).")
    rows = get_cursor("SELECT COUNT(full_name) as repository_count, COUNT(DISTINCT full_name) as distinc_repository_count FROM repos WHERE repository_score>5")
    for row in rows:
        print(f"* Distinct repositories with a score greater than 5: {row[1]} ({'{:.1f}'.format(100 * row[1] / (repository_count))} %).")
    rows = get_cursor("SELECT COUNT(full_name) as repository_count, COUNT(DISTINCT full_name) as distinc_repository_count FROM repos WHERE repository_score>6")
    for row in rows:
        print(f"* Distinct repositories with a score greater than 6: {row[1]} ({'{:.1f}'.format(100 * row[1] / (repository_count))} %).")
    print(f"")
    print(f"#### Statistics per test runs")
    rows=get_cursor("SELECT tag, min(recorded_on) as started_on, max(recorded_on) as finished_on, COUNT(full_name) as repository_count, COUNT(DISTINCT full_name) as distinc_repository_count FROM repos GROUP BY tag ORDER BY started_on")
    for row in rows:
        print(f"* Session: {row[0]}")
        print(f"** Processing time: {calendar.timegm(row[2].timetuple())-calendar.timegm(row[1].timetuple())} seconds.")
        print(f"** Repositories found: {row[3]} at a speed of {'{:.3f}'.format(row[3]/(calendar.timegm(row[2].timetuple())-calendar.timegm(row[1].timetuple())))} repository/second.")
        print(f"** Distinct repositories found: {row[4]} ({'{:.1f}'.format(100*row[4]/(row[3]))} %) at a speed of {'{:.3f}'.format(row[4]/(calendar.timegm(row[2].timetuple())-calendar.timegm(row[1].timetuple())))} repository/second.")
    print(f"")
    print(f"#### Reference repositories")
    rows=get_cursor("SELECT full_name, repository_score, commits_count FROM repos WHERE tag='Reference repositories' ORDER BY repository_score DESC")
    for row in rows:
        print(f"* Repository https://github.com/{row[0]} scores {'{:.1f}'.format(row[1])} and has {row[2]} commits")
    print(f"")
    print(f"#### Top 100 repositories found")
    rows=get_cursor("SELECT full_name, max(repository_score) as score, max(commits_count) as commits, count(full_name) as duplicate_level FROM repos GROUP BY full_name ORDER BY score DESC LIMIT 100")
    for row in rows:
        print(f"* Repository https://github.com/{row[0]} scores {'{:.1f}'.format(row[1])}")
    print(f"")

overal_activity()