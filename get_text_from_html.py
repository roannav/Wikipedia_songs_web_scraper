import bs4

# This takes any HTML, even a snippet from a web page,
# and returns just the text contained between any of the tags.
# It removes the <head>, <style>, and <script> sections first, 
# since that text doesn't show up on the webpage.
def get_text_from_html(soup):
    if soup.head:             # if there is a <head> tag in soup,
        soup.head.extract()   #     remove it
    while soup.style:         # if there are <style> tags in soup,
        soup.style.extract()  #     remove them 
    while soup.script:        # if there are <script> tags in soup,
        soup.script.extract() #     remove them 
    return soup.getText() 

def run_tests():
    html_filename = 'html/Funkytown.html'
    soup = bs4.BeautifulSoup(open(html_filename), features='html.parser')

    #print('_'*40)
    #print("HTML version:")
    #print(soup)     

    print('_'*40)
    print("text version:")
    print(get_text_from_html(soup))

run_tests()
