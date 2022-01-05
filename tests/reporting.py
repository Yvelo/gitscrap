from scraper.rl_agent import *
import calendar

def overal_activity():
    rows=get_cursor(f"SELECT COUNT(full_name) as repository_count, "
                    f"COUNT(DISTINCT full_name) as distinc_repository_count FROM repos")
    print(f"#### Statistics for all test runs combined")
    for row in rows:
        repository_count=row[0]
        print(f"* Repositories found: {repository_count}.")
        print(f"* Distinct repositories found: {row[1]} ({'{:.1f}'.format(100*row[1]/(repository_count))} %).")
    rows = get_cursor(f"SELECT COUNT(full_name) AS repository_count, "
                      f"COUNT(DISTINCT full_name) AS distinc_repository_count FROM repos WHERE repository_score>3")
    for row in rows:
        print(f"* Distinct repositories with a score greater than 3: {row[1]} "
              f"({'{:.1f}'.format(100 * row[1] / (repository_count))} %).")
    rows = get_cursor(f"SELECT COUNT(full_name) as repository_count, "
                      f"COUNT(DISTINCT full_name) AS distinc_repository_count FROM repos WHERE repository_score>4")
    for row in rows:
        print(f"* Distinct repositories with a score greater than 4: {row[1]} "
              f"({'{:.1f}'.format(100 * row[1] / (repository_count))} %).")
    rows = get_cursor(f"SELECT COUNT(full_name) AS repository_count, "
                      f"COUNT(DISTINCT full_name) AS distinc_repository_count FROM repos WHERE repository_score>5")
    for row in rows:
        print(f"* Distinct repositories with a score greater than 5: {row[1]} "
              f"({'{:.1f}'.format(100 * row[1] / (repository_count))} %).")
    rows = get_cursor(f"SELECT COUNT(full_name) AS repository_count, COUNT(DISTINCT full_name) "
                      f"AS distinc_repository_count FROM repos WHERE repository_score>6")
    for row in rows:
        print(f"* Distinct repositories with a score greater than 6: {row[1]} "
              f"({'{:.1f}'.format(100 * row[1] / (repository_count))} %).")
    print(f"")
    print(f"#### Statistics per test runs")
    rows=get_cursor("SELECT tag, min(recorded_on) AS started_on, max(recorded_on) AS finished_on, "
                   f"COUNT(full_name) AS repository_count, COUNT(DISTINCT full_name) AS distinc_repository_count "
                   f"FROM repos GROUP BY tag ORDER BY started_on")
    for row in rows:
        print(f"* Session: {row[0]}")
        print(f"    * Processing time: "
             f"{calendar.timegm(row[2].timetuple())-calendar.timegm(row[1].timetuple())} seconds.")
        print(f"    * Repositories found: {row[3]} at a speed of "
              f"{'{:.3f}'.format(row[3]/(calendar.timegm(row[2].timetuple()) -calendar.timegm(row[1].timetuple())))} "
              f"repository/second.")
        print(f"    * Distinct repositories found: {row[4]} ({'{:.1f}'.format(100*row[4]/(row[3]))} %) at a speed of "
              f"{'{:.3f}'.format(row[4]/(calendar.timegm(row[2].timetuple())-calendar.timegm(row[1].timetuple())))} "
              f"repository/second.")
    print(f"")
    print(f"#### Reference repositories")
    rows=get_cursor(f"SELECT full_name, repository_score, commits_count, forks FROM repos "
                   f"WHERE tag='Reference repositories' ORDER BY repository_score DESC")
    for row in rows:
        print(f"* Repository https://github.com/{row[0]} (score: {'{:.1f}'.format(row[1])}, "
              f"commits: {row[2]}, forks: {row[3]}, found: 1).")
    print(f"")
    print(f"#### Top 100 repositories found")
    rows=get_cursor(f"SELECT full_name, max(repository_score) AS score, max(commits_count) AS commits, "
                    f"max(forks) AS forks, count(full_name) AS duplicate_level "
                    f"FROM repos GROUP BY full_name ORDER BY score DESC LIMIT 100")
    duplicate_count=0
    for row in rows:
        print(f"* Repository https://github.com/{row[0]} (score: {'{:.1f}'.format(row[1])}, commits: {row[2]}, "
              f"forks: {row[3]}, found: {row[4]}).")
        duplicate_count += row[4]-1
    print(f"")
    print(f"Among the top 100 repositories {duplicate_count} duplicates "
          f"({'{:.1f}'.format(100*duplicate_count/(100+duplicate_count))} %) have been found.")
    print(f"")

overal_activity()