from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler
from dotenv import load_dotenv
from prompts import USABILITY_DOMAIN, IO_DOMAIN, DESCRIPTION_DOMAIN, EXECUTION_DOMAIN
import tiktoken
import streamlit as st
import os

load_dotenv()
save_directory = "./data/"

token_counts = {
    "embedding": 0,
    "input": 0,
    "output": 0,
    "total": 0
}
token_counter = TokenCountingHandler(
    tokenizer = tiktoken.encoding_for_model("gpt-4-turbo-preview").encode
)
embed_model_name = "text-embedding-3-small"
embed_model = OpenAIEmbedding(model=embed_model_name)
llm_model_name = "gpt-4-turbo-preview"
Settings.llm = OpenAI(model=llm_model_name)
Settings.callback_manager = CallbackManager([token_counter])
Settings.embed_model = embed_model

st.set_page_config(
    page_title="Biocompute Object Assistant Proof of Concept",
    initial_sidebar_state="expanded",
    menu_items={"About": "Built by @seankim658 with Streamlit and LlamaIndex."}
)

if "embed_tokens" not in st.session_state:
    st.session_state["embed_tokens"] = 0

if "llm_input_tokens" not in st.session_state:
    st.session_state["llm_input_tokens"] = 0

if "llm_output_tokens" not in st.session_state:
    st.session_state["llm_output_tokens"] = 0

if "pdf_upload" not in st.session_state:
    st.session_state["pdf_upload"] = None

if "index" not in st.session_state:
    st.session_state["index"] = None

model_cost_information = {
    "llm": {
        "gpt-3.5": {
            "input_token_cost_multiplier": 0.00005,
            "output_token_cost_multiplier": 0.00015,
        },
        "gpt-4-turbo-preview": {
            "input_token_cost_multiplier": 0.01,
            "output_token_cost_multiplier": 0.03
        },
        "gpt-4": {
            "input_token_cost_multiplier": 0.03,
            "output_token_cost_multiplier": 0.06,
        }
    },
    "embedding": {
        "text-embedding-3-small": 0.00002,
        "text-embedding-3-large": 0.00013,
        "ada-v2": 0.00010
    }
}

def sidebar():
    
    for model in model_cost_information['llm'].keys():
        model_match = (llm_model_name == model)
        with st.sidebar.expander(f"💲 {model} INFERENCE COST", expanded=model_match):
            input_tokens = st.session_state["llm_input_tokens"]
            output_tokens = st.session_state["llm_output_tokens"]
            st.markdown(f"LLM Prompt: {input_tokens} tokens")
            st.markdown(f"LLM Output: {output_tokens} tokens")
            i_cost = (input_tokens / 1000) * model_cost_information["llm"][model]["input_token_cost_multiplier"]
            o_cost = (output_tokens / 1000) * model_cost_information["llm"][model]["output_token_cost_multiplier"]
            st.markdown("Rough Cost Estimation: **${0}**".format(round(i_cost + o_cost, 5)))
            "[OpenAI Pricing](https://openai.com/pricing)"
    
    for embedder in model_cost_information['embedding'].keys():
        embed_match = (embed_model_name == embedder)
        with st.sidebar.expander(f"💲 {embedder} INFERENCE COST", expanded=embed_match):
            embed_tokens = st.session_state["embed_tokens"]
            st.markdown(f"Embed Tokens: {embed_tokens}")
            cost = (embed_tokens / 1000) * model_cost_information["embedding"][embedder]
            st.markdown("Rough Cost Estimation: **${0}**".format(round(cost, 5)))
            "[OpenAI Pricing](https://openai.com/pricing)"

    st.sidebar.button("Clear Messages", type="primary", on_click=lambda : clear_messages())
    st.sidebar.divider()

def clear_messages():
    st.session_state["messages"] = []

def layout():

    st.header("Build your BioCompute Domains!")

    if st.session_state.get("pdf_upload") is None:

        st.warning(
            "Please upload your PDF file to generate the BCO domains for.\n\n",
            icon="🚨",
        )

        uploaded_pdf = st.file_uploader("Choose a PDF file", type=["pdf"])
        if uploaded_pdf is not None:
            file_path = os.path.join(save_directory, uploaded_pdf.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_pdf.getbuffer())
            st.session_state["pdf_upload"] = uploaded_pdf.name
            st.button("Index PDF", on_click=lambda : index_pdf())

    else:

        st.success("PDF uploaded, please wait while it is indexed...")
        
        if st.session_state["index"] is not None:

            st.success("Your PDF has successfully been indexed.")

            usability_domain = st.session_state.get("get_usability_domain", False)
            io_domain = st.session_state.get("get_io_domain", False)
            description_domain = st.session_state.get("get_description_domain", False)
            execution_domain = st.session_state.get("get_execution_domain", False)
            parametric_domain = st.session_state.get("get_parametric_domain", False)
            error_domain = st.session_state.get("get_error_domain", False)
            col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

            with col1:
                if st.button("Generate Usability Domain", type="primary", on_click=lambda : perform_query("usability"), disabled=usability_domain):
                    st.session_state["get_usability_domain"] = True
            with col2:
                if st.button("Generate I/O Domain", type="primary", on_click=lambda : perform_query("io"), disabled=io_domain):
                    st.session_state["get_io_domain"] = True
            with col3:
                if st.button("Generate Description Domain", type="primary", on_click=lambda : perform_query("description"), disabled=description_domain):
                    st.session_state["get_description_domain"] = True
            with col4:
                if st.button("Generate Execution Domain", type="primary", on_click=lambda : perform_query("execution"), disabled=execution_domain):
                    st.session_state["get_execution_domain"] = True
            with col5:
                if st.button("Generate Parametric Domain", type="primary", disabled=parametric_domain):
                    st.session_state["get_parametric_domain"] = True
            with col6:
                if st.button("Generate Error Domain", type="primary", disabled=error_domain):
                    st.session_state["get_error_domain"] = True

            if "messages" in st.session_state:
                for message in st.session_state["messages"]:
                    st.markdown(message)

def index_pdf():
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    token_counts["embedding"] += token_counter.total_embedding_token_count
    st.session_state["embed_tokens"] += token_counts["embedding"]
    st.session_state["index"] = index

def perform_query(domain: str):
    index = st.session_state["index"]
    query_engine = index.as_query_engine()
    response = f"This is a response for the {domain} domain.\n"

    if domain == "usability":
        query_response = query_engine.query(f"Can you give me a Biocompute Object usability domain for the provided paper. The JSON return response must be valid against the JSON schema I am providing you. {USABILITY_DOMAIN}")
        response += str(query_response)
    elif domain == "io":
        query_response = query_engine.query(f"Can you give me a Biocompute Object IO domain for the provided paper. The JSON return response must be valid against the JSON schema I am providing you. {IO_DOMAIN}")
        response += str(query_response)
    elif domain == "description":
        query_response = query_engine.query(f"Can you give me a Biocompute Object description domain for the provided paper. The JSON return response must be valid against the JSON schema I am providing you. {DESCRIPTION_DOMAIN}")
        response += str(query_response)
    elif domain == "execution":
        query_response = query_engine.query(f"Can you give me a Biocompute Object execution domain for the provided paper. The JSON return response must be valid against the JSON schema I am providing you. {EXECUTION_DOMAIN}")
        response += str(query_response)

    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    st.session_state["messages"].append(response)

    token_counts["input"] += token_counter.prompt_llm_token_count
    st.session_state["llm_input_tokens"] += token_counts["input"]
    token_counts["output"] += token_counter.completion_llm_token_count
    st.session_state["llm_output_tokens"] += token_counts["output"]
    token_counts["total"] += token_counter.total_llm_token_count

def main():
    sidebar()
    layout()

if __name__ == "__main__":
    main()

# print(response)
# print(f"embedding: {token_counts['embedding']}\ninput: {token_counts['input']}\noutput: {token_counts['output']}\ntotal: {token_counts['total']}")
# token_counter.reset_counts()
