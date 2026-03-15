import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from app.ai.symptoms_dataset import SYMPTOMS

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings for all symptoms
symptom_embeddings = model.encode(SYMPTOMS)

# FAISS index
dimension = symptom_embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(symptom_embeddings))