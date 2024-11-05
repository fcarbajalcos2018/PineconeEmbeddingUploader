from openai import OpenAI
from pinecone import Pinecone

class PineconeService:

    def __init__(self, oaAPI: str, pcAPI: str):
        self.oa = OpenAI(api_key=oaAPI)
        self.pc = Pinecone(api_key=pcAPI)
        self.index = None
        self.vectors = None
