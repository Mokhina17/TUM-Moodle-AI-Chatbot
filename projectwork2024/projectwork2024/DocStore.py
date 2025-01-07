import os
import fitz 
from sentence_transformers import SentenceTransformer
import faiss

class DocStore:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = faiss.IndexFlatL2(self.model.get_sentence_embedding_dimension())
        self.documents = []
        self.load_pdfs_from_folder('coursecontents')

    def load_pdfs_from_folder(self, folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(folder_path, filename)
                self.add_document(pdf_path)
                print(f'Added document: {pdf_path}')

    def add_document(self, pdf_path):
        doc = fitz.open(pdf_path)
        text = ''
        for page_num in range(len(doc)):
            text += doc[page_num].get_text()
        chunks = self.chunk_text(text, chunk_size=512, overlap=64)
        for chunk in chunks:
            embedding = self.model.encode([chunk])
            self.index.add(embedding)
            self.documents.append(chunk)

    def chunk_text(self, text, chunk_size=512, overlap=128):
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            if end > len(text):
                end = len(text)
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap
        return chunks

    def search(self, query, k=5):
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, k)
        return [(self.documents[i], distances[0][j]) for j, i in enumerate(indices[0])]