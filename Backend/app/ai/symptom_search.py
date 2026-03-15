import numpy as np
from app.ai.embeddings import model,index
from app.ai.symptoms_dataset import SYMPTOMS

def find_closest_symptom(text):

    emb = model.encode([text])

    D,I = index.search(np.array(emb),1)

    return SYMPTOMS[I[0][0]]