from typing import Dict, List, Tuple, Any
import logging
from langgraph.graph.graph import CompiledGraph
from langchain.agents import Tool
from langgraph.prebuilt import create_react_agent
from langsmith import traceable
from langgraph.checkpoint.memory import MemorySaver
from llm_model import LlmModel
from system_message import system_message_function
from tool_knowledge_base import ToolKnowledgeBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGAgent:
    def __init__(self, config = None):
        try:
            self.config = config
            self.model = LlmModel.get_model()
            self.system_message = None
            self.memory = MemorySaver()  
            self.knowledge_base = ToolKnowledgeBase()
            self.tools = self._setup_tools()
            logger.info("RAG Agent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize RAG Agent: {str(e)}")
            raise Exception(f"Agent initialization failed: {str(e)}")
    
    def _setup_tools(self) -> List[Tool]:
        """Setup knowledge base tool"""
        return [
            self.knowledge_base
        ]

    def create_agent(self) -> CompiledGraph:
        """
        Create agent with system message, memory, tools and model.
        Returns:
            CompiledGraph: Configured agent graph
        """
        try:
          
            if not all([self.model, self.tools, self.memory, self.system_message]):
                raise ValueError("Missing required components")

            agent = create_react_agent(
                model=self.model,
                state_modifier=self.system_message,
                checkpointer=self.memory,
                tools=self.tools
            )
            return agent
        except Exception as e:
            logger.error(f"Agent creation failed: {str(e)}")
            raise Exception(f"Failed to create agent: {str(e)}")
    
    @traceable(metadata={"rag": "call_agent"})
    def call_agent(self, input_params: Dict[str, List[Tuple[str, Any]]], config: Dict[str, Dict[str, str]]) -> str:
        """Run agent with input and return response"""
        try:
           
            if not input_params or not config:
                raise ValueError("Missing input parameters")
            
            agent = self.create_agent()

          
            response = agent.invoke(input_params, config)
            
            logger.info("Agent execution completed successfully")
            return response["messages"][-1].content

        except Exception as e:
            logger.error(f"Agent execution failed: {str(e)}")
            raise Exception(f"Failed to execute agent: {str(e)}")


agent = RAGAgent()

def call_agent(input_params_1: Dict[str, List[Tuple[str, Any]]], input_params_2: Dict[str, Dict[str, str]]) -> str:
    """
    Call agent (convenience function).
    
    Returns:
        LLM response as text
    """
    agent.system_message = system_message_function()
    return agent.call_agent(input_params_1, input_params_2)

def __str__(self) -> str:
    """
    String representation of RAG Agent for debugging and logging.
    Returns informative string about agent's components and state.
    """
    components = {
        "model": type(self.model).__name__,
        "memory": type(self.memory).__name__,
        "system_message": type(self.system_message).__name__,
        "tools": [tool.__class__.__name__ for tool in self.tools]
    }
    return f"RAGAgent(model={components['model']}, tools={components['tools']}, memory={components['memory']})"

def __repr__(self) -> str:
    """Detailed string representation for development."""
    return self.__str__()


def main():
    """Test the RAG Agent functionality."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Testing the RAG Agent")
    
    try:
       
        logger.info("Initializing RAG Agent...")
        rag_agent = RAGAgent()
        rag_agent.system_message = system_message_function()
        logger.info("RAG Agent successfully initialized")
   
        test_queries = [
            "I am Karthik",
   "where can i get biryani?",
   "compare the food in twohannbar and chezpanize ",
   "what is my name?"
]
      
        for i, query in enumerate(test_queries):
            logger.info(f"Testing query {i+1}/{len(test_queries)}: '{query}'")
            
         
            input_params = {
                "messages": [
                    ("human", query)
                ]
            }
            
            config_params = {
                "configurable": {
                    "thread_id": f"test_thread_{0}"
                }
            }
            
            try:
                
                result = rag_agent.call_agent(input_params, config_params)
                
                print("\n" + "="*50)
                print(f"Query: {query}")
                print("-"*50)
                print(f"Response: {result}")
                print("="*50)
            except Exception as e:
                logger.error(f"Error processing query '{query}': {str(e)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in main test function: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\nRAG Agent test completed successfully")
    else:
        print("\nRAG Agent test failed")