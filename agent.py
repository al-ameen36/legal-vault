import os
import logging
import sys
from dotenv import load_dotenv
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Define the storage directory for persistence
PERSIST_DIR = "./storage"

# Check if storage already exists, and only index if it doesn't
if not os.path.exists(PERSIST_DIR):
    # Load documents and create the index if storage does not exist
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    # Store the index for later use
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # Load the existing index from storage
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

# Query the index
query_engine = index.as_query_engine()
# Uncomment to test a query
# response = query_engine.query("I need help. I was sexually abused")
# print(response)
