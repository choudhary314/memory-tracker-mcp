# memory-tracker-mcp

A simple **MCP server** that lets you save short notes ("memories") into an **OpenAI Vector Store** and later search them.

This project exposes two MCP tools:

- `save_memory(memory: str)` — stores a memory string in a vector store
- `search_memory(query: str)` — searches stored memories and returns relevant text chunks

## How it works

Internally, the server:

1. Lists existing OpenAI vector stores (or creates one if none exists)
2. Writes the memory text to a temporary `.txt` file
3. Uploads that file to the vector store
4. Uses vector store search to retrieve relevant chunks for queries

## Requirements

- Python **3.14+** (see `.python-version`)
- An OpenAI API key

## Configuration

Set environment variables:

- `OPENAI_API_KEY` (required)
- `VECTOR_STORE_NAME` (optional, defaults to `default_vector_store`)

Example:

```bash
export OPENAI_API_KEY="..."
export VECTOR_STORE_NAME="memories"
```

## Install

This repo uses `pyproject.toml`.

If you use **uv**:

```bash
uv sync
```

Or with **pip** (inside a virtualenv):

```bash
pip install -e .
```

## Run

Start the MCP server:

```bash
python server.py
```

## Tools

### `save_memory`

Saves a memory string to the configured vector store.

**Input**:

- `memory` — text to store

**Returns**:

```json
{ "status": "saved", "vector_store_id": "..." }
```

### `search_memory`

Searches the vector store for relevant chunks.

**Input**:

- `query` — search text

**Returns**:

```json
{ "results": ["...", "..."] }
```

## Notes / limitations

- The server currently returns the **first vector store found** from the OpenAI account; if none exist it creates one named `VECTOR_STORE_NAME`.
- Memories are uploaded as temporary text files.
