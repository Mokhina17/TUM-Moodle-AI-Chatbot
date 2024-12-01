import os
import PyPDF2
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

class DocStore:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        if os.path.exists('faiss_index.idx') and os.path.exists('documents.txt'):
            self.index = faiss.read_index('faiss_index.idx')
            with open('documents.txt', 'r') as f:
                self.documents = f.read().split('\n')
        else:
            self.index = faiss.IndexFlatL2(self.model.get_sentence_embedding_dimension())
            self.documents = []
            self.load_pdfs_from_folder('coursecontents')  # Load PDFs from the coursecontents folder

    def load_pdfs_from_folder(self, folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(folder_path, filename)
                self.add_document(pdf_path)

    def add_document(self, pdf_path):
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
            embedding = self.model.encode([text])
            self.index.add(embedding)
            self.documents.append(text)

    def search(self, query, k=5):
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, k)
        return [(self.documents[i], distances[0][j]) for j, i in enumerate(indices[0])]

# Example usage
if __name__ == "__main__":
    doc_store = DocStore()
    # Save the index and documents for later use
    faiss.write_index(doc_store.index, 'faiss_index.idx')
    with open('documents.txt', 'w') as f:
        for doc in doc_store.documents:
            f.write(doc + '\n')