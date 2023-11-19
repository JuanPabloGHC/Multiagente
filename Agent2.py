# necessary libraries -------->
import re

class Agent2():
    # constructor definition -------->
    def __init__(self):
        self.modulesList = []
        self.tf_re = r"(.*tf\..*)|(.*tensorflow\..*)"
        self.re_tokenizer = r"(tf\.[a-zA-Z_\.]+)|(tensorflow\.[a-zA-Z_\.]+)"
    
    # functions definition -------->
    def getModulesList(self):
        return self.modulesList

    def cleanModulesList(self):
        self.modulesList.clear

    def getIdentifiersFromFile(self, filename):
        # open file
        with open(filename, 'r') as source_code:
            # get all the lines contained by the file
            lines_array = source_code.readlines()
            # iterate through each line looking for used tensorflow modules
            for line in lines_array:
                # tf module(s) found
                if re.search(self.tf_re, line):
                    functionMatch = re.findall(self.re_tokenizer,line)
                    for func in functionMatch:
                        tfFunction = func[0].split(".")
                        newFunction = tfFunction[0] + '.' + tfFunction[1]
                        if not newFunction in self.modulesList:
                            self.modulesList.append(newFunction)
        return self.modulesList

# include all the modules/classes/functions/members that go after tf