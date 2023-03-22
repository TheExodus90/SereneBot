from dotenv import load_dotenv
import os
import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI

load_dotenv()

st.set_page_config(page_title='Serenity', layout='wide'),
st.title("Serenity Bot")

#Initialize a session state

if "generated" not in st.session_state:
    st.session_state["generated"] = [] #output
if "past" not in st.session_state:
    st.session_state["past"] = [] #past
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []


#Define a Function to get user input
def get_text():
    """
    Get the user input text.
    Returns:
        (str): The text entered by the user
    """
    input_text = st.text_input("You: ", st.session_state["input"], key="input",
                            placeholder="Your AI assistant here! Ask me anything ...", 
                            label_visibility='hidden')
    return input_text



# Retrieve the API keys from the environment variables
api = st.sidebar.text_input("Open AI API-Key", type="password")
MODEL = st.selectbox(label='Model', options= ['gpt-3.5-turbo','text-davinci-003','text-davinci-002','code-davinci-002'])
K = st.number_input(' (#)Summary of prompts to consider',min_value=3,max_value=1000)
if api:
#Create OpenAI Instance

    llm = OpenAI(
        temperature=0.75,
        openai_api_key=api,
        model_name=MODEL ,
)

  # Create a ConversationEntityMemory object if not already created
    if 'entity_memory' not in st.session_state:
            st.session_state.entity_memory = ConversationEntityMemory(llm=llm,k=K)

    #Create Conversation Chain
    Conversation = ConversationChain(
        llm = llm,
        prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        memory = st.session_state.entity_memory
    )
else:
    st.error("No API Found")

# Get User Input
user_input = get_text()

# Generate the output using the ConversationChain object
if user_input:
    output = Conversation.run (input=user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

with st.expander("Conversation"):
    for i in range(len(st.session_state['generated'])-1,-1,-1):
        st.info(st.session_state["past"][i])
        st.success(st.session_state["generated"][i],icon="🧞")
