from ..models.pineconeService import PineconeService
from ..models.inputFiles import InputFiles

class MainUI():

    def __init__(self):
        self.isLoaded: bool = None
        self.oaAPI = ''
        self.pcAPI = ''
        self.data: list | dict = None
        self.pc: PineconeService = None
    
    def welcome(self):
        print('Welcome to the Pinecone Embedding and Vector Uploader!')
        print('Press 1 to start a new upload')
        print('Press 2 to continue an upload from saved file')
        res = int(input('Your response: '))
        if res == 1:
            print('You selected (1) to start a new upload job')
            self.isLoaded = False
        elif res == 2:
            print('You selected (2) to load an existing save file and continue upload job')
            self.isLoaded = True
        else:
            print('Your selection was INVALID. Please reattempt.')
            self.welcome()

    def loadOrNew(self):
        if self.isLoaded == True:
            self._resumeFromFile()
        else:
            self._startNewJob()
    
    def _startNewJob(self):
        inFile = InputFiles()
        self.oaAPI, self.pcAPI = self.__insertOaPc(inFile=inFile)
        print('OpenAI Key:', self.oaAPI)
        print('Pinecone Key:', self.pcAPI)
        print('Please enter the name of the CSV file containing the Embeddings')
        csvFileName = input('CSV File:')
        inFile.set_csvFilename(csvFileName)
        print('Proceeding to access contents of files...')
        self.data = inFile.get_csv()
        if len(self.oaAPI) == 0 or len(self.pcAPI) == 0 or len(self.csv) == 0:
            print('Unable to access file contents.')
            print('The names you entered do not match with existing files in this directory. Please reattempt.')
            self._startNewJob()

    def __insertOaPc(self, inFile: InputFiles):
        print('Please enter the name of the file containing the Open AI API Key')
        oaFileName = input('OpenAI API Key File: ')
        inFile.set_oaAPIfilename(oaFileName)
        print('Please enter the name of the file containing the Pinecone API Key')
        pcFileName = input('Pinecone API Key File: ')
        inFile.set_pcAPIfilename(pcFileName)
        return inFile.get_oaAPI(), inFile.get_pcAPI()
    
    def _resumeFromFile(self):
        inFile = InputFiles()
        self.oaAPI, self.pcAPI = self.__insertOaPc(inFile=inFile)
        print('Please enter the name of the JSON file containing the SAVED embeddings')
        embFileName = input('JSON File: ')
        inFile.set_embFilename(embFileName)
        print('Loading file...')
        self.data = inFile.get_emb()
        if len(self.oaAPI) == 0 or len(self.pcAPI) == 0 or len(self.data.keys()) == 0:
            print('Unable to access file contents.')
            print('The names you entered do not match with existing files in this directory. Please reattempt.')
            self._resumeFromFile()
