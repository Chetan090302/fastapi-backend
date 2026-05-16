import numpy as np
import faiss
from sentence_transformers import SentenceTransformer, CrossEncoder
from dotenv import load_dotenv
from test import call_model

load_dotenv()

documents = [
    "Transformers are powerful deep learning models used in NLP",
    "FAISS is a library for efficient similarity search",
    "Cross encoders provide accurate ranking by jointly encoding inputs",
    "Sentence transformers generate embeddings for semantic search",
    "Large language models are used in generative AI applications"
]

bi_encoder = SentenceTransformer('all-MiniLM-L6-v2', model_kwargs={"cache_dir": "./cache"})
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', model_kwargs={"cache_dir": "./cache"})

doc_embeddings = bi_encoder.encode(documents)
index_model = faiss.IndexFlatIP(doc_embeddings.shape[1])  
index_model.add(np.array(doc_embeddings,dtype=np.float32))

def search(query, top_k):
    emb_vector = bi_encoder.encode([query]).astype("float32")

    scores, indexes = index_model.search(emb_vector, top_k)
    indexes = indexes.flatten()

    vec_documents = [documents[i] for i in indexes if i != -1]

    if not vec_documents:
        return None

    cross_encoder_inp = [(query, doc) for doc in vec_documents]
    relevance_scores = cross_encoder.predict(cross_encoder_inp)

    pairs = list(zip(relevance_scores, vec_documents))
    pairs.sort(key=lambda x: x[0], reverse=True)

    for score, doc in pairs:
        print(f"Score: {score:.4f} | Doc: {doc}")

    return pairs[0][1]

def process_rag_data(rag_document: str):
    prompt = f"""
You are a strict information extraction system.

Instructions:
- Use ONLY the information provided in the context below.
- DO NOT add any external knowledge.
- DO NOT assume anything not present in the context.
- Summarize the content clearly and concisely.

Context:
{rag_document}

Output:
Provide a clear and concise summary based ONLY on the given context.
"""
    
    response = call_model(prompt)
    return response['message']['content']

def trigger_rag_document(query:str):
    rag_docs=search(query,3)
    return process_rag_data(rag_docs)

if __name__=="__main__":
    print(trigger_rag_document("what is faiss"))


