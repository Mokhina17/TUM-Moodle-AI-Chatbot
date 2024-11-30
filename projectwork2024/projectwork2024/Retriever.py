from transformers import DPRContextEncoder, DPRContextEncoderTokenizer
from transformers import DPRQuestionEncoder, DPRQuestionEncoderTokenizer

# Load context and question encoders
ctx_encoder = DPRContextEncoder.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")
ctx_tokenizer = DPRContextEncoderTokenizer.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")
q_encoder = DPRQuestionEncoder.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
q_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained("facebook/dpr-question_encoder-single-nq-base")

# Encode the corpus
def encode_corpus(corpus):
    embeddings = []
    for doc in corpus["text"]:
        inputs = ctx_tokenizer(doc, return_tensors="pt", truncation=True, padding=True)
        embeddings.append(ctx_encoder(**inputs).pooler_output.detach().numpy())
    return embeddings

document_embeddings = encode_corpus(document_store)

#to be continued