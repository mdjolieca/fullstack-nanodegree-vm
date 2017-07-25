import psycopg2

#Utitily module to run reports agains news database
DBNAME = 'news'

# constants for reports
# each report has a TITLE, UNITS, and QUERRY string.
POPULAR_ARTICLES_TITLE = 'Three most popular articles.'
POPULAR_ARTICLES_UNITS = ' views'
POPULAR_ARTICLES_QUERY = '''select articles.title,  count(*) from articles
 inner join log ON log.path like concat ('%' ,articles.slug)
 group by articles.title order by count(*) desc limit 3;
'''
POPULAR_AUTHORS_TITLE = 'Authors popularity by views.'
POPULAR_AUTHORS_UNITS = ' views'
POPULAR_AUTHORS_QUERY = '''select authors.name, count(*) from authors 
inner join articles ON authors.id = articles.author 
inner join log ON log.path like concat ('%' ,articles.slug)
group by authors.name order by count(*) desc;
'''
ERRORS_BYDAY_TITLE = 'Days with greater than one percent error.'
ERRORS_BYDAY_UNITS = '% errors'
ERRORS_BYDAY_QUERY = '''select date(time), round((sum(case when status
 <> '200 OK' then 1 else 0 end)*100.0 / count(*)),1) 
from log group by date(time)
having (sum(case when status <> '200 OK' then 1 else 0 end)
*100.0 / count(*)) > 1;
'''
# To add addtional reports add the 3 required report strings above.
# Incrementthe NUM_REPORTS then add the names for the 3 new reports
# strings to the respective lists (QUERIES, TITLES, UNITS). 
NUM_REPORTS = 3
QUERIES = [POPULAR_ARTICLES_QUERY, POPULAR_AUTHORS_QUERY, ERRORS_BYDAY_QUERY] 
TITLES = [POPULAR_ARTICLES_TITLE, POPULAR_AUTHORS_TITLE, ERRORS_BYDAY_TITLE]
UNITS = [POPULAR_ARTICLES_UNITS, POPULAR_AUTHORS_UNITS, ERRORS_BYDAY_UNITS]

# Generates reports based on the constants defined above.
def generate_reports(start=0, finish=3):
    try:
        # Connect to DB and get a cursor
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        # Generate all reports for given ranges
        for x in range(0,NUM_REPORTS):
            c.execute(QUERIES[x])
            results = c.fetchall()
            print('\n\n' + TITLES[x])
            for key,val in results:
                print('*' + '  "' + str(key) + '" -- ' + str(val)
               + UNITS[x])
        print('\n')
    finally:
        # Close DB connection.
        db.close()
    
if __name__ == "__main__":
    # execute only if run as a script
    generate_reports()
