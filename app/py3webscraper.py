import bs4
import urllib3
from bs4 import BeautifulSoup as soup
import csv
# import for write image to file
import os
import io
#import sys
#import codecs
import requests
import random
import datetime
# import for mongodb
import pymongo

encoding = 'utf8'

class Book:
    def __init__(self, imageURL="", book_title="", book_author="", book_publish="", ISBN="", category=[], price=""):
        # type: (object, object, object, object, object, object, object) -> object
        self.imageURL = imageURL
        self.book_title = book_title
        self.book_author = book_author
        self.book_publish = book_publish
        self.ISBN = ISBN
        self.category = category
        self.price = price

    def print_book(self):
        print("img :" + self.imageURL)
        print("Title :" + self.book_title)
        print("Author :" + self.book_author)
        print("Publisher :" + self.book_publish)
        print("ISBN :" + self.ISBN)
        print("category-len:" + str(len(self.category)))
        for c in self.category:
            print("Category :" + str(c))
        print("Price :" + self.price)


class book_page_scraper:
    def __init__(self, output_csvfilename = "book_csv_file.csv"):
        self.book_entries = []  # appended list of books
        self.response = ""
        self.csvfilename = output_csvfilename
        self.entries = [] # list of entries per row
        self.bookcollection = {}
        self.base_url = "http://www.bogbasen.dk"
        # Connect to server
        self.mongoclient = pymongo.MongoClient('localhost', 27017)
        # Select the database
        self.importdb = self.mongoclient.bookshelf

    def WriteImagetoDisk(self, imageURL):
       # resource = urllib.urlopen( imageURL )
        #create a random output filename
        image_str = self.base_url + imageURL
        currentFilePath = os.getcwd()
        first = random.randrange(1000)
        t = datetime.datetime.now().time()
        timestamp = (t.hour * 3600 + t.minute * 60 + t.second) - first
        outputfilename = str(timestamp) + ".jpg"
        outputFile = currentFilePath + "/images/" + outputfilename
        output = open(outputFile,"wb")
        output.write(requests.get(image_str).content)
        output.close()
        return outputfilename

    def getRemoteImageURL(self, imageURL):
    	image_str = self.base_url + imageURL
    	return image_str

    def page_url(self, url_link):
        self.my_url = url_link
        # opening the connection to read the page
        #uFile = uOpen(self.my_url) #- this is for python2
        #enabling python3 libs
        self.http = urllib3.PoolManager()
        self.response = self.http.request('GET', self.my_url)
        #self.html_page = uFile.read()
        #uFile.close()

    def set_numof_pages(self, pagestoScrape):
        self.numofpages = int(pagestoScrape)

    def drop_importDB(self): # Drop collection from the mongoDB
        print('Dropping collection bookimports')
        self.importdb.bookimports.drop()

    def scrape_page(self):
        book = Book()

        # html parsing
        page_soup = soup(self.response.data, "html.parser")
        # grab each book entry
        containers = page_soup.findAll("li", {"class": "book-info"})
        for container in containers:

            # get the book imageURL
            if container.img:
                imageURL = container.img['src']
                #write image to disk
                #book.imageURL = self.WriteImagetoDisk(imageURL)
                #store the remote image URL
                book.imageURL = self.getRemoteImageURL(imageURL)

            # get the book title
            if container.h2:
                book.book_title = container.h2.text

            # get the books author
            if container.h3:
                h3_object = container.h3
                if h3_object.a:
                    book.book_author = h3_object.a.text
            p_objects = container.findAll("p")
            if p_objects:
                for p in p_objects:
                    if p.text.find("fra") != -1:
                        book.book_publish = p.text
                    if p.text.find("ISBN") != -1:
                        if p.em:
                            book.ISBN = p.em.text
                    if p.text.find("Kategori") != -1:
                        a_objects = p.findAll("a")
                        a_counter = 0
                        for a in a_objects:
                            if a:
                                book.category.append(a.text)
                    if p.text.find("pris") != -1:
                        if p.em:
                            ems = p.find_all("em")
                            if ems[0].text.find("pris"):
                                book.price = ems[0].text

            self.entries.append(book.book_title)
            self.entries.append(book.book_author)
            self.entries.append(book.book_publish)
            self.entries.append(book.ISBN)
            self.entries.append(book.price)
            self.entries.append(book.imageURL)
            for c in book.category:
                self.entries.append(c)


            # filling our the collection
            # self.bookcollection['title'] = book.book_title
            # self.bookcollection['author'] = book.book_author
            # self.bookcollection['publish'] = book.book_publish
            # self.bookcollection['isbn'] = book.ISBN
            # self.bookcollection['price'] = book.price
            # self.bookcollection['imageurl'] = book.imageURL
            # for c in book.category:
            #     self.bookcollection['category'] = c


            self.bookdata = dict(title=book.book_title,
                               author=book.book_author,
                               publish=book.book_publish,
                               ISBN=book.ISBN,
                               price=book.price,
                               image=book.imageURL,
                               category=book.category)

            self.importdb.bookimports.insert(self.bookdata)

            book.print_book()

            self.bookcollection = {}
            self.book_entries.append(self.entries)
            self.entries = []
            book.category = []

            for item in book.category:
                del item

    csv_columns = ['Title','author','published','ISBN','price','image','category','category','category','category']

    def write_cvs(self):
        try:
            with io.open(self.csvfilename,mode='w', encoding='UTF-8') as csvfile:
                writer = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
                writer.writerow(self.csv_columns)
                for data in self.book_entries:
                    writer.writerow(data)
            csvfile.close()
        except IOError as e:
            errno, strerror = e.args
            print("I/O error({0}): {1}".format(errno,strerror))
        return


    #def push_to_db(self, dbhandle):


bookscrape = book_page_scraper("booklist.csv")
bookscrape.set_numof_pages(163) #165
for page_count in range (1,bookscrape.numofpages):
    url_sting = "http://www.bogbasen.dk/soeg/?kategori=&forfatter=&lookup=a5250aac23c54b0f8919e8e98e58e642&titel=&fritekst=&soeg=true&aktuelside=" + str(page_count)
    bookscrape.page_url(url_sting)
    bookscrape.scrape_page()

bookscrape.write_cvs()
bookscrape.mongoclient.close()
# my_url = 'https://www.zalora.sg/women/accessories/sunglasses/'
