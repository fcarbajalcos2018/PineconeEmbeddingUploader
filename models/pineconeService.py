from openai import OpenAI
from pinecone import pinecone, Pinecone

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