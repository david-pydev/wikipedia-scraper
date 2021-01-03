import requests                          # library to do http requests.
from bs4 import BeautifulSoup            # library to treat html.
import pyfiglet                          # library to make custom titles.
from colorama import Fore, Back, init    # library to color text.
from sys import exit                     # function to exit quit the program.

init(convert=True, autoreset=True)

# welcome titles.
welcome_text = (pyfiglet.figlet_format("\n \t Wkipedia Scraper", font="digital"))
welcome_text += "\t   by @david-pydev"
welcome_text += "\n" *4
welcome_text += " * This program will print a short introduction of the topics \n   of the list that you select."
welcome_text += "\n \n * Don't forget to send a txt file with the topics \n"
welcome_text += "   comma separated, like this: 'topic 1, topic 2, topic 3, ...'.\n"
welcome_text += "\n * Type 'q' to quit." 


# format string to write the param to url.
def format_param(strings):

    formated_param = ""

    for string in strings:

       formated_param += string + "+"
    
    return formated_param.rstrip("+")  


# load the list of topics.
def loader(topics_list):
    
    # manipulates strings to correct possible spacing errors.
    with open(topics_list, 'r') as f_obj:
        topics_list = f_obj.read()   
        topics_list = topics_list.split(",")
        topics_list = list(map(lambda x: format_param(x), list(map(lambda x:x.split(), (list(map(lambda x: x.strip(), topics_list)))))))

    return topics_list


# do the request and get the html with BeautifulSoup.
def get_html(topic, leng):

    # set lenguage and url
    if leng == "1":
        leng = "en"
    else:
        leng = "pt"

    url = "https://" + leng + ".wikipedia.org"
    url += "/w/index.php?search={}&title=Especial%3APesquisar&go=Ir&wprov=acrw1_-1".format(topic)

    # do the request
    response = requests.get(url)  

    soup = BeautifulSoup(response.text, 'html.parser')

    return (soup, response.url)


# filter the html and get only the title and the introduction of the article.
def get_text(soup):


    # extract the title and introduction of the article
    title_text = soup.find('h1').text
    indice = soup.find(id= "toc")
    introduction = list(map(lambda x:x.text, indice.find_all_previous('p')))

    return (title_text, introduction)


# return a cleaned and formated text.
def format_text(title_text, introduction):

    output_text = ""

    custom_title = pyfiglet.figlet_format("\n \t" + title_text)

    output_text += custom_title

    # remove references like "[1], [2]", etc. and mount the introduction"
    for p_tag in reversed(introduction):

        for i in range(100):
            p_tag = p_tag.replace("[{}]".format(i), "")

        output_text += p_tag + "\n"

    return output_text


# main function to execute the program.
def main():

    topics_not_found = []

    # choose the list of topics.
    while True:
        try:
            topics_list_path = input("\n >> Enter the topics list path: ")
            if topics_list_path == 'q':
                print("\n\n    Come back anytime :)\n")
                exit()
            if ".txt" not in topics_list_path:
                topics_list_path += ".txt"
            
            topics_list = loader(topics_list_path)
            
            break

        except FileNotFoundError:
            print(Fore.RED + "\n Error: file or directory not found. Try another path.")

    # choose the lenguage of article.
    while True:
        leng = input("\n >> Choose lenguage: \n\n => english (enter '1') \n => portuguese (enter '2') \n\n >> ")
        if leng == 'q':
            print("\n\n    Come back anytime :)\n")
            exit()
        if leng == "1" or leng == "2":
            break
        else:
            print(Fore.RED + "\n Error: invalid input! Please enter '1' (english) or '2' (portuguese).")

    print("\n >> Please Wait. Searching for results...")

    # Make the requests and print the results
    for topic in topics_list:

        soup_url = get_html(topic, leng)

        try:
            contents = get_text(soup_url[0])
        except AttributeError:
            topics_not_found.append(topic)
            continue

        formated_text = format_text(contents[0], contents[1])

        print(formated_text + Fore.BLUE + " => Read more on: {}".format(soup_url[1]))

    # print the topics that program cannot found
    if topics_not_found:
        not_found_output = ""

        for topic in topics_not_found: 
            not_found_output += " => " + topic.replace("+", " ") + "\n"
      
        print(Fore.RED + "\n\n * Some topics cannot be found: \n\n" + not_found_output)

    print("\n\n    Thanks for use :)\n")


# execution
print(welcome_text)
main()
