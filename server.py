from mcp.server.fastmcp import FastMCP
from openai import OpenAI
import tempfile
from dotenv import load_dotenv
import os

load_dotenv()

#Instantiate OPENAI client
openai_client = OpenAI()

VECTOR_STORE_NAME = os.getenv("VECTOR_STORE_NAME", "default_vector_store")

#Instantiate FASTMCP mcp
mcp = FastMCP("Memories")

def list_create_vector_store():
    #list or create vectore store
    stores = openai_client.vector_stores.list()
    for store in stores:
        return store
    return openai_client.vector_stores.create(name=VECTOR_STORE_NAME)


@mcp.tool()
def save_memory(memory:str) -> dict:
    """
    Save a memory string to the vector store
    """
    vector_store = list_create_vector_store()
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as f:
        f.write(memory)
        f.flush()
        openai_client.vector_stores.files.upload_and_poll(
            vector_store_id=vector_store.id,
            file=open(f.name, "rb")
        )
    return {"status": "saved", "vector_store_id": vector_store.id}

@mcp.tool()
def search_memory(query: str):
    """
    Searches memories in the vector store and return relevant chunks of information.
    """
    vector_store = list_create_vector_store()
    results = openai_client.vector_stores.search(vector_store_id=vector_store.id, query=query)
    memory_content = [content.text for item in results.data for content in item.content if content.type == "text"]
    return {"results": memory_content}

if __name__ == "__main__":
    mcp.run()