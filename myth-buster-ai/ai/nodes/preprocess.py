from ai.state import State
from ai.schemas import Segment
from langchain_text_splitters import RecursiveCharacterTextSplitter

recursive_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=1000,
    chunk_overlap=0,
    length_function=len,
    is_separator_regex=False,
)

async def preprocess(state: State):
    chunks = recursive_splitter.split_text(state["original_content"])
    segments = [Segment(content=chunk, id=id) for id, chunk in enumerate(chunks)]
    return { "cleaned_content": state["original_content"].strip(), "segments": segments }