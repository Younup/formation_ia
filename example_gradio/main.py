import gradio as gr
from langchain.schema import AIMessage, HumanMessage

from langchain.chat_models import init_chat_model

def predict(message, history):
    llm_openai = init_chat_model("gpt-4o-mini", model_provider="openai", api_key="")
    history_langchain_format = []
    for msg in history:
        if msg['role'] == "user":
            history_langchain_format.append(HumanMessage(content=msg['content']))
        elif msg['role'] == "assistant":
            history_langchain_format.append(AIMessage(content=msg['content']))
            
    history_langchain_format.append(HumanMessage(content=message))
    gpt_response = llm_openai.invoke(history_langchain_format)
    return gpt_response.content

gr.ChatInterface(
    predict,
    type="messages",
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Ask any question", container=False, scale=7),
    title="Chatbot with UI",
    description="Ask any question",
    theme="ocean",
    examples=["Hello", "Am I cool?", "Are tomatoes vegetables?"],
    cache_examples=True,
).launch()