from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest

def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    source_dir = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(source_dir, filename)
    f = open(filepath, 'r')        
    reading = f.read()  
    f.close()
    soup = BeautifulSoup(reading, 'lxml')  
    searching1 = soup.find_all('a', class_='bookTitle')
    searching2 = soup.find_all('div', class_='authorName__container')  
    book_title = []
    book_author = []
    for x in searching1:
        book_title.append(x.text.strip())
    for y in searching2:
        book_author.append(y.text.strip())   
    results = []
    results = list(zip(book_title, book_author))
    return results

def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    retrieving = requests.get(url)
    soup = BeautifulSoup(retrieving.text, 'html.parser')  
    book_title = soup.find_all('a', class_='bookTitle')
    list1 = []
    for i in book_title[:10]:
        book_names = i.get('href')
        if book_names.startswith('/book/show/'):
            list1.append("https://www.goodreads.com" + book_names)
    return list1     

def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    retrieving = requests.get(book_url)
    soup = BeautifulSoup(retrieving.text, 'html.parser')
    book_title = soup.find('h1', class_='gr-h1 gr-h1--serif').text.strip()
    book_author = soup.find('span', itemprop='name').text.strip()   
    page_number = int(soup.find('span', itemprop='numberOfPages').text.strip()[:3])   
    return (book_title, book_author, page_number)       

def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    source_dir = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(source_dir, filepath)  
    f = open(filepath, 'r')      
    reading = f.read()  
    f.close()
    soup = BeautifulSoup(reading, 'html.parser') 
    summarizing_category = soup.find_all('h4', class_='category__copy')
    summarizing_book_title = soup.find_all('div', class_='category__winnerImageContainer')
    summarizing_url = soup.find_all('div', class_='category clearFix')  
    
    #Finding Category 
    category_list = []
    for x in summarizing_category:
        category_list.append(x.text.strip())   

    #Finding Book Title 
    book_title_find_list = []
    book_title_list = []
    for y1 in summarizing_book_title:
        i = y1.find('img')['alt']
        book_title_find_list.append(i)
    for y2 in book_title_find_list:
        book_title_list.append(y2.strip())

    #Finding URL 
    url_find_list = []
    url_list = []
    for z1 in summarizing_url:
        j = z1.find('a')['href']
        url_find_list.append(j)
    for z2 in url_find_list:
        url_list.append(z2.strip())  
    best_books = list(zip(category_list, book_title_list, url_list))  
    return best_books 

def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    source_dir = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(source_dir, filename)
    f = open(filepath, 'w')       
    write_data = csv.writer(f, delimiter=",")
    write_data.writerow(['Book title', 'Author Name'])   
    for i in data:
        write_data.writerow(i)
    f.close()  

def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):
    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()  

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        title = get_titles_from_search_results("search_results.htm")

        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(title), 20)

        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(title), list) 

        # check that each item in the list is a tuple
        for i in title:
            self.assertEqual(type(i), tuple)    

        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(title[0], ('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'))   

        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(title[19][0], ('Harry Potter: The Prequel (Harry Potter, #0.5)'))     
        
    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(TestCases.search_urls), list)  

        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)  

        # check that each URL in the TestCases.search_urls is a string
        for url in TestCases.search_urls:
            self.assertEqual(type(url), str)       

        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for url in TestCases.search_urls:
            self.assertIn("https://www.goodreads.com/book/show/", url)    

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for i in TestCases.search_urls:
            summaries.append(get_book_summary(i))   

        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)
        for i in summaries:

            # check that each item in the list is a tuple
            self.assertEqual(type(i), tuple)

            # check that each tuple has 3 elements
            self.assertEqual(len(i), 3)

            # check that the first two elements in the tuple are string
            self.assertEqual(type(i[0]), str)
            self.assertEqual(type(i[1]), str)

            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(type(i[2]), int)  

            # check that the first book in the search has 337 pages
            self.assertEqual(summaries[0][2], 337)  
        
    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        best_books = summarize_best_books('best_books_2020.htm')  

        # check that we have the right number of best books (20)
        self.assertEqual(len(best_books), 20)     
        for i in best_books: 

            # assert each item in the list of best books is a tuple  
            self.assertEqual(type(i), tuple)   

            # check that each tuple has a length of 3
            self.assertEqual(len(i), 3)   

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(best_books[0], ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))  

        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(best_books[19], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))  

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        result = get_titles_from_search_results('search_results.htm')

        # call write csv on the variable you saved and 'test.csv'
        write_csv(result, 'test.csv')  

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        source_dir = os.path.abspath(os.path.dirname(__file__)) 
        filepath = os.path.join(source_dir, 'test.csv')  
        f = open(filepath, 'r')
        csv_reader = csv.reader(f)  
        csv_lines = []  
        for i in csv_reader:
            csv_lines.append(i)   

        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)  

        # check that the header row is correct
        self.assertEqual(csv_lines[0], ['Book title', 'Author Name'])     

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1], ['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])    

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'Julian Harrison (Introduction)'  
        self.assertEqual(csv_lines[20], ['Harry Potter: The Prequel (Harry Potter, #0.5)', 'Julian Harrison (Introduction)'])    
        f.close()  
        
if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)




