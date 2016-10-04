# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".

import scraperwiki
import csv
from datetime import datetime
from StringIO import StringIO
f = scraperwiki.scrape("http://www.afcd.gov.hk/english/agriculture/agr_fresh/files/Supply_Figures.csv").decode("big5").encode("utf-8")
reader = csv.reader(StringIO(f))
next(reader, None)


def remove_brackets(s):
    return s.replace("(", "").replace(")", "")

for r in reader:
    if r[0] == '':
        continue
    revision_date = datetime.strptime(r[-1], "%d/%m/%Y").date()
    provider_eng =  r[-4]
    provider_chi =  r[-3]
    source_eng =  r[-6]
    source_chi =  r[-5]
    intake_date_eng =  remove_brackets(r[-8])
    intake_date_chi =  remove_brackets(r[-7])
    unit_eng =  remove_brackets(r[-10])
    unit_chi =  remove_brackets(r[-9])
    intake = int(r[-11] if r[-11] != '-' else "0") 
    food_type_eng =  r[-14]
    food_type_chi =  r[-13]
    fresh_food_category_eng =  r[-16]
    fresh_food_category_chi =  r[-15]
    category_eng =  r[-18]
    category_chi =  r[-17]
 
    d = {'revision_date': revision_date,
         'provider_eng': provider_eng,
         'provider_chi': provider_chi,
         'source_eng': source_eng,
         'source_chi': source_chi,
         'category_eng': category_eng,
         'category_chi': category_chi,
         'fresh_food_category_eng': fresh_food_category_eng,
         'fresh_food_category_chi': fresh_food_category_chi,
         'food_type_eng': food_type_eng,
         'food_type_chi': food_type_chi,
         'intake_date_chi': intake_date_chi,
         'intake_date_eng': intake_date_eng,
         'intake': intake,
         'unit_eng': unit_eng,
         'unit_chi': unit_chi,
    }
    for k in d.keys():
        v = d[k]
        if k.endswith("chi"):
            d[k] = v.decode("utf-8")  
    scraperwiki.sqlite.save(unique_keys=['revision_date', 'category_eng', 'fresh_food_category_eng', 'food_type_eng', 'source_eng', 'provider_eng'], data=d)
