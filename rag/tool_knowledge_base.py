import logging
from typing import Optional, Any
from pydantic import BaseModel, Field, ConfigDict
from langchain.tools import StructuredTool
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_huggingface import HuggingFaceEmbeddings
from langsmith import traceable

logger = logging.getLogger(__name__)
logging.basicConfig()
logging.getLogger("langchain.retrievers").setLevel(logging.INFO)
url = "https://f555dca1-ee7b-4467-96cc-3ff43eae0610.us-east-1-0.aws.cloud.qdrant.io:6333"
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.-MFkhf_hItKpDmSFBLVFDgEbc6swVPYaXAdccHL0o4I"

class KBaseQuery(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    query: str = Field(description="User query to search in restaurant knowledge base", 
                      example="Does Pizza Palace have vegetarian options?")

class ToolKnowledgeBase(StructuredTool):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    vector_db: Optional[QdrantVectorStore] = None
    vs_retriever: Optional[Any] = None
    
    def __init__(self):
        super().__init__(
            name="RestaurantKnowledgeBase",
            description="Tool to query restaurant information from vector database.",
            func=self.retrieve_from_kbase,
            args_schema=KBaseQuery,
            return_direct=False
        )
        
        client = QdrantClient(
            url=url,
            api_key=api_key,
        )
        
        self.vector_db = QdrantVectorStore(
            client=client,
            embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"),
            collection_name="website_content_2"
        )
        self.vs_retriever = self.vector_db.as_retriever(search_type="mmr")
    
    @traceable(run_type="retriever", name="retrieve_restaurant_info")
    def retrieve_from_kbase(self, query: str, k: int = 3) -> str:
        logger.info(f"Searching restaurant knowledge base for query: {query}")
        try:
            docs = self.vs_retriever.invoke(query)[:k]
            results = [f"Restaurant: {doc.metadata.get('restaurant_name', 'Unknown')}\nInfo: {doc.page_content}\nSource: {doc.metadata.get('source', 'Unknown')}" 
                    for doc in docs]
            return "\n\n".join(results) if results else "No relevant restaurant information found."
        except Exception as e:
            logger.error(f"Knowledge base search failed: {str(e)}")
            return f"Error searching knowledge base: {str(e)}"

def main():
    """Test the ToolKnowledgeBase functionality."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Testing the ToolKnowledgeBase")
    
    try:
      
        logger.info("Initializing ToolKnowledgeBase...")
        kb_tool = ToolKnowledgeBase()
        logger.info("ToolKnowledgeBase successfully initialized")
        
        test_queries = [
    "where can I buy the best burger?"
]
        
        for query in test_queries:
            logger.info(f"Testing query: '{query}'")
            result = kb_tool.retrieve_from_kbase(query)
            print(f"\nQuery: {query}")
            print("-" * 50)
            print(f"{result}")
            print("-" * 50)
        
      
        agent_query = "Is there a Japanese restaurant with good sushi?"
        logger.info(f"Testing tool invocation with query: '{agent_query}'")
        tool_result = kb_tool.invoke({"query": agent_query})
        print(f"\nAgent Query: {agent_query}")
        print("-" * 50)
        print(f"{tool_result}")
        print("-" * 50)
        
        return True
        
    except Exception as e:
        logger.error(f"Error in main test function: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\nToolKnowledgeBase test completed successfully")
    else:
        print("\nToolKnowledgeBase test failed")