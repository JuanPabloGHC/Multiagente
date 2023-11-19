# necessary libraries -------->
import requests
from bs4 import BeautifulSoup as bs
import re

class Agent3():
    # constructor definition -------->
    def __init__(self, version, usedFunction):
        self.url = 'https://github.com/tensorflow/tensorflow/releases'
        self.version = version
        self.Text = ""
        self.usedFunction = usedFunction
        
    # functions definition -------->
    '''
    Clean variables
    '''
    def cleanText(self):
        self.Text = ""
    '''
    Get the html of all the page
    '''
    def getWebPage(self):
        #Request the webpage
        response = requests.get(self.url)
        
        #LOCAL-------------->
        # file  = open("pagina.txt", "r", encoding="utf-8")
        # response_html = file.read()
        
        #Convert the request into a text
        response_html = response.text
        #Parse to html the text
        soup = bs(response_html, 'html.parser')
        return soup
    '''
    Get the section according to the version
    '''
    def getSection(self, webPage):
        sections = webPage.find_all('section')

        for s in sections:
            versions = s.find_all('h2')
            for a in versions:
                if (a.string == self.version):
                    return s
    '''
    Get all the information
    '''
    def getInformation(self, section):
        # for func in self.usedFunctions:
        functionFound = False
        information = []
        # Split the information by <h1> then by <h2>, then by <h3>, then by <ul> and if you find the function:
        # Divide this last block of information by <li> to save the function title and then save the next list information about the function
        newSection = str(section).split('<h1>')[1]
        containersH2 = str(newSection).split('<h2>')
        for h2 in containersH2:
            containersH3 = str(h2).split('<h3>')
            for h3 in containersH3:
                ul = str(h3).split('<ul>')
                for list in ul:
                    ul2 = str(list).split('<ul>')
                    for item in ul2:
                        #BORRAR SI NO FUNCIONA------------
                        for func in self.usedFunction:
                            text = re.search(func, item)
                            if(text != None):
                                break
                        #PERMANECER
                        # text = re.search(self.usedFunction, item)
                        if(functionFound):
                            final = str(item).split('</ul>')
                            information.append(final[0])
                            functionFound = False
                        elif(text):
                            functionFound = True
                            li = str(list).split('<li>')
                            for i in li:
                                #BORRAR SI NO FUNCIONA------------
                                for func in self.usedFunction:
                                    text = re.search(func, i)
                                    if(text != None):
                                        break
                                #PERMANECER
                                # text = re.search(self.usedFunction, i)
                                if(text):
                                    if(str(h2).split('</h2>')[0] not in information):
                                        information.append(str(h2).split('</h2>')[0])
                                    if(str(h3).split('</h3>')[0] not in information):
                                        information.append(str(h3).split('</h3>')[0])
                                    information.append(str(i))
        return information
    '''
    Get the block text
    '''
    def getBlockText(self, container):
        block_html = bs(container, 'html.parser')
        block_text = block_html.get_text()
        return block_text
    '''
    MAIN
    '''
    def mainFunction(self):
        webPage = self.getWebPage()
        
        #Find the section
        section = self.getSection(webPage)
        
        #Get the information
        information = self.getInformation(section)

        # Convert the list of strings to an unique text else return an empty array
        if(len(information) != 0):
            for info in information:
                self.Text += info + "\n"
        else:
            return []
        
        # Delete all the tags to just keep the primary information
        block = self.getBlockText(self.Text)
        newBlock = block.split("\n")
        return newBlock