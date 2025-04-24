import streamlit as st
import logging

from agent import RAGAgent, system_message_function

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="RAG Agent Chat",
    page_icon="🤖",
    layout="centered"
)

st.title("RAG Agent Chat")
st.markdown("Ask questions to the RAG Agent and get answers powered by LLM and knowledge base.")

@st.cache_resource
def initialize_agent():
    """Initialize and return the RAG Agent."""
    try:
        logger.info("Initializing RAG Agent...")
        rag_agent = RAGAgent()
        rag_agent.system_message = system_message_function()
        logger.info("RAG Agent successfully initialized")
        return rag_agent
    except Exception as e:
        logger.error(f"Failed to initialize RAG Agent: {str(e)}")
        st.error(f"Error initializing the agent: {str(e)}")
        return None

rag_agent = initialize_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("What would you like to know?"):
   
    st.session_state.messages.append({"role": "user", "content": prompt})
   
    with st.chat_message("user"):
        st.write(prompt)
    
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            
            input_params = {
                "messages": [
                    ("human", prompt)
                ]
            }
            
            config_params = {
                "configurable": {
                    "thread_id": "1289078667"
                }
            }
            
           
            response = rag_agent.call_agent(input_params, config_params)
            
          
            message_placeholder.markdown(response)
            
           
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            error_message = f"Error: {str(e)}"
            message_placeholder.error(error_message)
            logger.error(f"Error processing query '{prompt}': {str(e)}")
            st.session_state.messages.append({"role": "assistant", "content": error_message})

with st.sidebar:
    st.title("About")
    st.markdown("""
    This is a RAG (Retrieval-Augmented Generation) Agent chatbot.
    
    It uses:
    
    - LangChain for tools integration
    - Knowledge base for answering questions
    
    Feel free to ask questions about restaurants, food, or anything the knowledge base contains!
    """)
    
  
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()