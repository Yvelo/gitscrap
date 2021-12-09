import psycopg2

def print_hi(name):
    print(f'Bonjour, {name}')

if __name__ == '__main__':
    print_hi('PyCharm')


try:
    conn = psycopg2.connect("dbname='gitscrap' user='scraping' host='10.28.0.3' password='JZi0DkjjCxzuBWgJne29'")
except:
    print("I am unable to connect to the database")

cur = conn.cursor()
cur.execute("""SELECT count(*) from repos""")
rows = cur.fetchall()
print("\nShow me the databases:\n")
for row in rows:
    print("   ", row[0])