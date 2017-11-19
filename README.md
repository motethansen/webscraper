
# Web Scraping

Web scraping is done to extract data from a web page.
This example will be presented using python and [beautifulsoup.](https://www.crummy.com/software/BeautifulSoup/)

To get started, it will be good to setup a virtual environment:

In order to have a simple environment to work on, we will install [virtualenv](https://virtualenv.pypa.io/en/stable/installation/).
use:

```bash
$ pip install virtualenv
```

Now you can create your directory

```bash
$ mkdir mypythonproject
```

Let's go ahead and create a virtual environment for this python project


```bash
$ cd mypythonproject
$ virtualenv ENV
```


This command **virtualenv ENV** will create the python environment.
You will need to activate the environment by executing:

```bash
$ source ENV/bin/activate
```

you should now see your prompt change to something like this:

```bash
 (ENV)$
```

Now you can run your pip install commands to install depend packages for this project.

```bash
 (ENV)$ pip install [package name]
```

Do create a list of required packages for this project by using:

```bash
 (ENV)$ pip freeze > requirements.txt
```

This will create a file **requirements.txt** listing all the packages used in this project.

If you want to install the packages from the requirement file you must execute:

```bash
 (ENV)$ pip install -r requirements.txt
```

When you want to close the virtual environment use the command *deactivate*

Sometime you might have an older version of pip. then you will upgrade:

```bash
$ pip install --upgrade pip
```
---

## Web scraping with [Portia](https://github.com/scrapinghub/portia#running-portia)
[Portia](https://github.com/scrapinghub/portia#running-portia) is a tool that allows you to visually scrape websites without any programming knowledge required. With Portia you can annotate a web page to identify the data you wish to extract, and Portia will understand based on these annotations how to scrape data from similar pages.


I like to show you how to develop your own web scraping code using Python and BeautifulSoup.

## Installing Beautiful Soup
We will be using BeautifulSoup4 in this example.

Installing Beautiful Soup is done by using pip:
```bash
(ENV)$ pip install beautifulsoup4
```

You can create a python file and install beautifulsoup and URL request. This is what is needed to open a HTML file and parse it.

mywebscraper.py
``` python
import bs4 #import beautifulsoup
import urllib2

```

Some time back my dad asked me if there was a way he could extract the books he had posted on an online portal into a CSV file.
The reason was that the portal did not support exporting the books after he posted them, and he wanted to maintain a record of books he has online and offline in case someone requests a certain title.

This is how we got started writing a simple  script using BeautifulSoup to scrape the books from his pages into a CSV file.

The following example shows the step I went through. It should give you enough basic information on how to use BeautifulSoup to scrape a web page.

The web site that holds his books is called bogbased.dk - it is a danish book club.

![bogbasen](https://i.imgur.com/PZYYTuC.png)

Here is the link to his books (showing the first page):
```
http://www.bogbasen.dk/soeg/?kategori=&forfatter=&lookup=a5250aac23c54b0f8919e8e98e58e642&titel=&fritekst=&soeg=true&aktuelside=1
```

If you open the url in a browser (chrome) and turn on the development tools. You will see the HTML code for the page.

![developmenttools](https://i.imgur.com/Mkkkw3C.png)

The code can be testing by running the python shell.

```python
Python 2.7.14 (default, Oct 14 2017, 21:14:02)
[GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.37)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import bs4
>>> import urllib2
>>> from bs4 import BeautifulSoup as soup
>>> from urllib2 import urlopen as uOpen
>>>
```

Now lets try to open the URL and read the page.
```python
>>> my_url = 'http://www.bogbasen.dk/soeg/?kategori=&forfatter=&lookup=a5250aac23c54b0f8919e8e98e58e642&titel=&fritekst=&soeg=true&aktuelside=1'
>>> uFile = uOpen(my_url)
>>> html_page = uFile.read()
>>> uFile.close()
```

we read the page and store it in the html_page variable.
Then we can start to parse it:
```bash
>>> page_soup = soup(html_page, "html.parser")
>>> containers = page_soup.findAll("li",{"class":"book-info"})
>>> containers[4]
```
```html
<li class="book-info">\n<p class="date">Senest opdateret 7.
   november</p><h2>Det Allerhelligste</h2><h3><span>Af</span>
     <a href="/soeg/?forfatter=J.+Bech+Nygaard&amp;soeg=true"
      title="Find flere b\xf8ger af J. Bech Nygaard">J. Bech
       Nygaard</a></h3><p> p\xe5 forlaget <em>Samleren.
          Indb.394sider</em></p><p>Kategori:
      <a href="/kategorier/Sk%C3%B8nlitteratur">
        Sk\xf8nlitteratur</a></p><p>pris: <em>20 kr
        </em> \u2013 stand:<em class="condition condition-5"
         title="5/6">\u2605\u2605\u2605\u2605\u2605</em></p>
        <ul class="actions">\n<li>\n
          <a href="/boeger/3698768:det-allerhelligste/">
            K\xf8b bog</a> </li>\n<li
             id="add-to-list-d577ad4b358e9ee82574c6c60189e490">
             \n<a href="javascript:hideBook(
             'd577ad4b358e9ee82574c6c60189e490')">
             Gem i "udvalgte b\xf8ger"</a> </li>\n</ul>\n</li>
```
Take a look at the output for the container. The printed segment is for item 4 in the list.
Below is the output reformatted using [jsbeautifier.org](http://jsbeautifier.org/) this makes it easier to read:
```html
<li class="book-info">\n
    <p class="date">Senest opdateret 7. november
    </p>
    <h2>Det Allerhelligste</h2>
    <h3><span>Af</span>
        <a href="/soeg/?forfatter=J.+Bech+Nygaard&amp;soeg=true" title="Find flere b\xf8ger af J. Bech Nygaard">J. Bech
       Nygaard</a></h3>
    <p> p\xe5 forlaget <em>Samleren.
          Indb.394sider</em></p>
    <p>Kategori:
        <a href="/kategorier/Sk%C3%B8nlitteratur">
        Sk\xf8nlitteratur</a></p>
    <p>pris: <em>20 kr
        </em> \u2013 stand:<em class="condition condition-5" title="5/6">\u2605\u2605\u2605\u2605\u2605</em></p>
    <ul class="actions">\n
        <li>\n
            <a href="/boeger/3698768:det-allerhelligste/">
            K\xf8b bog</a> </li>\n
        <li id="add-to-list-d577ad4b358e9ee82574c6c60189e490">
            \n<a href="javascript:hideBook(
             'd577ad4b358e9ee82574c6c60189e490')">
             Gem i "udvalgte b\xf8ger"</a> </li>\n</ul>\n
       </li>
```
Try to print the p object:
```bash
>>> containers[4].p
<p class="date">Senest opdateret 7. november</p>
>>>
```
It will give you the first p object in the container index 4.

then try get the H2 out:
```bash
>>> containers[4].h2
<h2>Det Allerhelligste</h2>
>>>
>>> containers[4].h2.text
u'Det Allerhelligste'
>>>
```
Notice, I printed the H2 object and adding the .text  in order to extract the text from the H2 object.
The text is utf-8 format, so to convert we need to encode:
```bash
>>> containers[4].h2.text.encode('utf-8')
'Det Allerhelligste'
>>>
```
You can now built up the code to extract the individual objects.
below is an extract of the different objects we like to collect:
```python
# get the book imageURL
  if container.img:
    imageURL = container.img['src'].encode('utf-8')
    #write image to disk
    #book.imageURL = self.WriteImagetoDisk(imageURL)
    #store the remote image URL
    book.imageURL = self.getRemoteImageURL(imageURL)

# get the book title
  if container.h2:
    book.book_title = container.h2.text.encode('utf-8')

# get the books author
  if container.h3:
    h3_object = container.h3
  if h3_object.a:
    book.book_author = h3_object.a.text.encode('utf-8')
```
You will find the code repository here:

[webscraper](https://github.com/motethansen/webscraper)
