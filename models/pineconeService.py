from openai import OpenAI
from pinecone import pinecone, Pinecone
import time
import random
import json

class PineconeService:

    def __init__(self, oaAPI: str, pcAPI: str):
        self.oa = OpenAI(api_key=oaAPI)
        self.pc = Pinecone(api_key=pcAPI)
        self.index = None
        self.vectors = None
        self.failedEmbeddings = []

    def defineIndex(self, indexName: str):
        indexes = [index['name'] for index in self.pc.list_indexes()]
        if len(indexes) == 0 or indexName not in indexes:
            self.pc.create_index(
                name=indexName,
                dimension=3072,
                metric='cosine',
                spec=pinecone.ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
        self.index = self.pc.Index(name=indexName)

    def addVectors(self, csvData: list, embModel: str):
        vectors = []
        #print(csvData)
        countErrorsInFail = 0

        for entry in csvData:
            #print('a', entry)
            if countErrorsInFail == 3:
                print('Error limit reached. Breaking operation.')
                break
            countErrorsInRetry = 0
            while countErrorsInRetry < 3:
                vector = {
                    'id': str(entry['id']),
                    'values': self._generateEmbedding(content=entry['content'], embModel=embModel),
                    'metadata': {
                        'title': entry['title']
                    }
                }
                if len(vector['values']) > 0:
                    vectors.append(vector)
                    countErrorsInFail = 0
                    print(f'Vector {vector["id"]} successfully created!')
                    break
                countErrorsInRetry += 1
                sleep = 60
                print(f'Vector {vector["id"]} creation FAILED. Reattempting creation for up to 3 times in a span of {sleep} seconds.')
                print('No. of attempts:', countErrorsInRetry)
                time.sleep(sleep)
            else:
                countErrorsInFail += 1
                print('Maximum no. of retries reached. Proceeding to the next embedding with a failure count of', countErrorsInFail, '.')
                self.failedEmbeddings.append(entry)
                print(f'Failed embedding data {vector["id"]} added to separate list for local save.')
                
        return vectors
    
    def _generateEmbedding(self, content: str, embModel: str):
        try:
            res = self.oa.embeddings.create(input=content, model=embModel)
            embedding = res.data[0].embedding
            print(f"Generated embedding of length {len(embedding)}")
            return embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
        return []
    
    def uploadVectors(self, vectors: list, batchSize: int):
        vecLen = len(vectors)
        if self.index == None or vecLen == 0:
            print('ERROR: Could not proceed with vector upload. Either the index has not been initialized or the vectors were missing.')
            return False
        batch = []
        couldUpload = True
        print('begin upload')
        print('start..')
        for i in range(vecLen):
            batch.append(vectors[i])
            print('append', i)
            print(i + 1, '%', batchSize, (i + 1) % batchSize, (i + 1) % batchSize == 0)
            if (i + 1) % batchSize != 0 and i != vecLen - 1:
                continue
            print('batch', [vector['id'] for vector in batch])
            try:
                self.index.upsert(batch)
            except TypeError as e:
                print('Unable to upload due to the following:', e)
                couldUpload = False
            batch.clear()
        return couldUpload
        
    def saveFailedEmbeddings(self):
        if len(self.failedEmbeddings) == 0:
            print('No failed embeddings. Rejecting operation.')
            return
        fullDir = f'inputFiles/{self._generateRandomFileName()}.json'
        with open(file=fullDir, mode='w') as file:
            json.dump(self.failedEmbeddings, file)
        
    def _generateRandomFileName():
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        filename = ''
        for i in range(8):
            char_i = random.randrange(len(chars))
            filename += chars[char_i]
        return filename