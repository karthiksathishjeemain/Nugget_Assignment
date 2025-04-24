from href_collection import href_collection
from data_collection import data_collection
from data_cleaning import data_cleaning
from store import store

if __name__ =="__main__":
    print("AAAAAAAA collecting hrefs")
    href_collection()
    print("BBBBBBBB data collecting")
    data_collection()
    print("CCCCCCCC data cleaning")
    data_cleaning()
    print("DDDDDDDD storing")
    store()