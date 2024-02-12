import requests
from bs4 import BeautifulSoup
import genanki
import html

# URL of the webpage containing the questions and answers

#Module 1-3
#url = "https://itexamanswers.net/ccna-1-v7-modules-1-3-basic-network-connectivity-and-communications-exam-answers.html"

#Module 4-7
#url = "https://itexamanswers.net/ccna-1-v7-modules-4-7-ethernet-concepts-exam-answers.html"

#Module 8-10
#url = "https://itexamanswers.net/ccna-1-v7-modules-8-10-communicating-between-networks-exam-answers.html"

#Module 11-13
# name = "CNAA 11-13" 
# url = "https://itexamanswers.net/ccna-1-v7-modules-11-13-ip-addressing-exam-answers-full.html"

#Module 14-15
# name = "CNAA 14-15" 
# url = "https://itexamanswers.net/ccna-1-v7-modules-14-15-network-application-communications-exam-answers.html"

#Module 16-17
name = "CNAA 16-17" 
url = "https://itexamanswers.net/ccna-1-v7-modules-16-17-building-and-securing-a-small-network-exam-answers.html"

# Make a request to the webpage and parse
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the content from the specified <div>

#Module 1-3
# content_div = soup.select_one('#post-36900 > div > div > div.thecontent.clearfix')

#Module 4-7
#content_div = soup.select_one('#post-36903 > div > div > div.thecontent.clearfix')

#Module 8-10
#content_div = soup.select_one('#post-36912 > div > div > div.thecontent.clearfix')

#Module 11-13
# content_div = soup.select_one('#post-36918 > div > div > div.thecontent.clearfix')

#Module 14-15
# content_div = soup.select_one('#post-36920 > div > div > div.thecontent.clearfix')

#Module 16-17
content_div = soup.select_one('#post-36929 > div > div > div.thecontent.clearfix')

if content_div:
    # The content_div exists, proceed with scraping questions and answers
    elements = content_div.find_all(['p', 'ul'])
    insideElement = None

    # Initialize variables to store questions, answers, and explanations
    flashcards = []
    current_question = None
    current_answer_options = []
    answer_options_forQuestion = []
    current_explanation = "No explanation"
    image_url = None

    for element in elements:
        if element.name == 'p':
            print(element)
            strong_tag = element.find('strong')
            insideElement = element.find(['b'])
            # print(insideElement)
            if insideElement != None:
                # print("ELEMENT FOUND", element )
                current_explanation = element.get_text()
            
            # explanation_text = element.find('Explanation:')

            # print(element)
            # print(explanation_text)

            if strong_tag:
                text = strong_tag.get_text()
                
                # if current_question:
                #     # Create a flashcard for the previous question
                #     flashcards.append((current_question, answer_options_forQuestion, current_answer_options, current_explanation))

                current_question = text
                current_answer_options = []
                current_answer_options_question = []



                # if insideElement:
                #     current_explanation = insideElement

                # print (current_explanation)

                
                

        elif element.name == 'ul':
            # Extract the list items from the <ul> element
            li_elements = element.find_all('li')
            #print (li_elements)

            answer_options = [" - " + li_element.get_text() for li_element in li_elements]
            answer_options_forQuestion = [" - " + li_element.get_text() for li_element in li_elements]
            #print (answer_options)
            
            for i in range(len(answer_options)):
                #print (li_elements[i])
                if li_elements[i].find('strong'):
                    answer_options[i] = " ☆ ANSWER" + (answer_options[i])
            #print (answer_options_forQuestion)
            
            
            current_answer_options_question = answer_options_forQuestion
            current_answer_options = answer_options

            if current_question:
                flashcards.append((current_question, answer_options_forQuestion, current_answer_options, current_explanation))
                current_question = None 

    # Create a Anki deck
    model_id = 1234567890  #ID Anki deck
    deck_id = 987654321  #ID Anki deck
    model = genanki.Model(
        model_id,
        'Custom Model Name',
        fields=[
            {'name': 'Question'},
            {'name': 'AnswerOptionsQuestion'},
            {'name': 'AnswerOptions'},
            {'name': 'Explanation'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}<br>{{AnswerOptions}}',
                'afmt': '{{Question}}<br>{{AnswerOptionsQuestion}}<br>{{Explanation}}',
            },
        ]
    )

    deck = genanki.Deck(deck_id, name)

    # Create flashcards for each question, answers, and explanations
    for question, answer_options, answer_options_forQuestion, explanation in flashcards:
        
        
        
        answer_options_str = "<br> ".join(answer_options)

        #Explanation not added at this time.
        #answer_options_str = "<br> ".join(explanation)
        answer_options_quest_str = "<br> ".join(answer_options_forQuestion)


        
        note = genanki.Note(
            model=model,
            fields=[str(question), str(answer_options_quest_str), str(answer_options_str), str(explanation)]
        )
        deck.add_note(note)

    # Package and save the deck
    package = genanki.Package(deck)
    package.write_to_file('C:/Users/atmcd/OneDrive/School Folder UWT/WebsitesCode/Webscraper/output3.apkg')
else:
    print("Content div not found on the webpage.")
