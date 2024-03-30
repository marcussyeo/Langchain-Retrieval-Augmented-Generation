# Retrieval-Augmented Generation for PDFs

### Using LangChain and OpenAI

1. Install dependencies

```
pip install -r requirements.txt
```

2. Dump your PDF files into the data folder
3. Adjust the chunk_size and chunk_overlap under create_database.py

```python
def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, <--
        chunk_overlap=200, <--
        length_function=len,
        add_start_index=True,
    )
```

4. Create the Chroma DB

```
python create_database.py
```

5. Query the Chroma DB

```
python query_data.py "What projects have he done so far?"
```
