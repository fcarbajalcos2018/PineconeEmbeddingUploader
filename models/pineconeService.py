from openai import OpenAI
from pinecone import pinecone, Pinecone
import time

class PineconeService:

    def __init__(self, oaAPI: str, pcAPI: str):
        self.oa = OpenAI(api_key=oaAPI)
        self.pc = Pinecone(api_key=pcAPI)
        self.index = None
        self.vectors = None

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
                    'values': _generateEmbedding(content=entry['content'], embModel=embModel),
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
                
        return vectors