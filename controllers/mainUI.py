from ..models.pineconeService import PineconeService

class MainUI():

    def __init__(self):
        self.isLoaded: bool = None
        self.oaAPI = ''
        self.pcAPI = ''
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
