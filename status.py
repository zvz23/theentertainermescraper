from db import WebScraperDB


with WebScraperDB('theentertainerme.db') as conn:
    print("WITH DETAILS ", len(conn.get_all_with_info()))