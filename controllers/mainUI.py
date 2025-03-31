from models.pineconeService import PineconeService
from models.inputFiles import InputFiles

class MainUI():

    def __init__(self):
        self.isLoaded: bool = None
        self.oaAPI = ''
        self.pcAPI = ''
        self.data: list | dict = None
        self.pc: PineconeService = None
        self.isIndexSelected = False
        self.vectorsQueue = []
    
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
        if len(self.oaAPI) == 0 or len(self.pcAPI) == 0 or len(self.data) == 0:
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

    def defineIndexEmbeddings(self):
        indexName = None
        self.pc = PineconeService(oaAPI=self.oaAPI, pcAPI=self.pcAPI)
        print('Contents: ', self.data)
        if not self.data or len(self.data) == 0:
            print('No data was retrieved. Terminating operation.')
            return
        if isinstance(self.data, list):
            print('Please enter a name for an existing or new Index')
            indexName = input('Index Name: ')
            self.pc.defineIndex(indexName)
            self.isIndexSelected = True
        elif isinstance(self.data, dict):
            print('Extracting name from save file')
            try:
                indexName = self.data['indexName']
                self.data = self.data['embeddings']
                self.pc.defineIndex(indexName)
                self.isIndexSelected = True
            except AttributeError as ae:
                print('INVALID JSON format:', ae)
        else:
            raise Exception('The file contents could not be read')
    
    def addVectors(self):
        if not self.isIndexSelected:
            print('Index not defined. Terminating operation.')
            return
        print('By the number, please select the embedding model as follows:')
        print('1. text-embedding-3-large')
        embModel = int(input('Embedding Model: '))
        if embModel == 1:
            print('Proceeding to add vectors...')
            self.vectors = self.pc.addVectors(csvData=self.data, embModel='text-embedding-3-large')
        else:
            print('INVALID field entry. Please reattempt.')
            self.addVectors()
            
        print('Vector generation complete.')
    
    def uploadVectors(self):
        if not self.vectors or len(self.vectors) == 0:
            print('Vectors not defined. Terminating operation.')
            return
        print('Specify a number for the batch size.')
        batchSize = int(input('Batch Size: '))
        if batchSize > 1:         
            print('Proceeding to upload...')
            self.pc.uploadVectors(vectors=self.vectors, batchSize=batchSize)
            self.pc.saveFailedEmbeddings()
        else:
            print('INVALID entry. Please reattempt.')
            self.uploadVectors()