import streamlit as st
from llama_cpp import Llama

st.set_page_config(page_title="💬 Local Bot")

with st.sidebar:
    st.title('💬 Local Bot')
    hf_email = st.text_input('E-mail:', type='password')
    hf_pass = st.text_input('Passwort:', type='password')
    if not (hf_email and hf_pass):
        st.warning('Bitte einloggen!', icon='⚠️')
    elif (hf_email != st.secrets['EMAIL']) | (hf_pass != st.secrets['PASSWORD']):
        st.warning('E-mail oder Passwort sind falsch!', icon='⚠️')
    else:
        st.success('Jetzt chatten!', icon='👉')

# Load LLM
if "llm" not in st.session_state.keys():
    modelpath = "assets/em_german_mistral_v01.Q8_0.gguf"
    st.session_state.llm = Llama(
	      model_path=modelpath,
	      n_ctx=2048,
	      n_batch=1024,
	      n_gpu_layers=-1,
	      verbose=False
      )

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hallo! Wie kann ich helfen?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLM response
def generate_response(prompt):
    output = llm(
	    f"Du bist ein hilfreicher Assistent. USER: {prompt} ASSISTANT:",
	    max_tokens=500,
	    temperature=0.6)
    response = output['choices'][0]['text']
    return response

# User-provided prompt
if prompt := st.chat_input("Hier Frage eingeben", disabled=not (hf_email and hf_pass)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
