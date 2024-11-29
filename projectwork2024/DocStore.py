from datasets import Dataset

# Example corpus
corpus = [
    {"text": ""},
    {"text": ""},
    {"text": ""}
]

# Convert to Hugging Face dataset
document_store = Dataset.from_list(corpus)


