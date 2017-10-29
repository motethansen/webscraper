# webscraper
##How to extract books data from a danish book site bogbasen.dk

Some time back my dad asked me if there was a way he could extract the books he had posted on an online portal into a CSV file.
The reason was that the portal did not support exporting the books after he posted them, and he wanted to maintain a record of books he has online and offline in case someone requests a certain title.

So, I thought of writing a simple  script using BeautifulSoup to scrape the books from his pages into a CSV file.

The following example shows the step I went through. It should give you enough basic information on how to use BeautifulSoup to scrape a web page.

The web site that holds his books is called bogbased.dk - it is a danish book club.

![bogbasen](/Users/michaelhansen/Projects/Udemy/Python/webscraping/images/website-to-scrape)

Here is the link to his books (showing the first page):
```
http://www.bogbasen.dk/soeg/?kategori=&forfatter=&lookup=a5250aac23c54b0f8919e8e98e58e642&titel=&fritekst=&soeg=true&aktuelside=1
```

If you open the url in a browser (chrome) and turn on the development tools. You will see the HTML code for the page.
