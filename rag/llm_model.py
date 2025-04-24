from typing import Optional
from langchain_groq import ChatGroq
from dataclasses import dataclass
import logging
import os
from dotenv import load_dotenv
load_dotenv()
# print("pass word is ",os.getenv("GROQ_API_KEY"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LlmConfig:
    """Configuration for LLM model."""
    model_name: str = "llama3-70b-8192"
    temperature: float = 0
    max_retries: int = 2
    
class LlmModel:
    """LLM model wrapper for Groq."""
    
    _instance = None
    
    @classmethod
    def initialize(cls, config: Optional[LlmConfig] = None) -> None:
        """Initialize LLM model with configuration."""
        try:
            if not config:
                config = LlmConfig()
            
            cls._instance = ChatGroq(
                api_key=os.getenv("GROQ_API_KEY"),
                model_name=config.model_name,
                temperature=config.temperature,
                max_retries=config.max_retries,
            )
            logger.info(f"LLM Model initialized: {config.model_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLM model: {str(e)}")
            raise
            
    @classmethod
    def get_model(cls) -> ChatGroq:
        """Get LLM model instance."""
        if not cls._instance:
            cls.initialize()
        return cls._instance

try:
    LlmModel.initialize()
except Exception as e:
    logger.error(f"Failed to initialize LLM model on import: {str(e)}")


def main():
    """Simple test function to get a direct response from the LLM model."""
    try:
        
        print("\nTesting direct LLM response...\n")
        
        model = LlmModel.get_model()
      
        test_query = "Tell me about the benefits of AI in healthcare."
        print(f"Query: {test_query}\n")
        
        from langchain_core.messages import HumanMessage
        response = model.invoke([HumanMessage(content=test_query)])
        
        print("Response from Llama:")
        print("-" * 50)
        print(response.content)
        print("-" * 50)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    
    main()