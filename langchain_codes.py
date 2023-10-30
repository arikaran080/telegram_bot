from dotenv import load_dotenv
from langchain.llms import HuggingFacePipeline
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM
import transformers
import os
import torch
device = torch.device('cpu')
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

model_id = 'meta-llama/Llama-2-7b-chat-hf'
hf_auth = os.getenv("HF_TOKEN")

model_config = AutoConfig.from_pretrained(
    model_id,
    use_auth_token=hf_auth
)

tokenizer = AutoTokenizer.from_pretrained(
    model_id,
    use_auth_token=hf_auth
)

# Initialize the model to run on CPU
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    config=model_config,
)

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=device,  # Use CPU
    max_length=1000,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id
)

llm = HuggingFacePipeline(pipeline=pipeline, model_kwargs={'temperature': 0.7})

prompt_template = """<s>[INST] <<SYS>>
{{ You are a helpful AI Assistant}}<<SYS>>
###

Previous Conversation:
'''
{history}
'''

{{{input}}}[/INST]

"""
prompt = PromptTemplate(template=prompt_template, input_variables=['input', 'history'])

memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=5,
    return_messages=True,
    output_key="output"
)

chain = ConversationChain(llm=llm, prompt=prompt)

print(chain.run("What is the capital of India?"))




# responses

def handle_responses(text: str) -> str:
    processed = text.lower()
    if "hello" in processed:
        return "Hey there"
    if "how are you" in processed:
        return "I'm good. What about you?"
    return "I do not understand what you are saying"
