import os
import streamlit as st
import torch
import torch.nn.functional as F
from transformers import pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")

@st.cache_resource(show_spinner = "유사도 모델 불러오는 중...")
def get_embedder():
    return pipeline("feature-extraction", model = "jhgan/ko-sroberta-multitask")

def get_embeddings(texts):
    embedder = get_embedder()
    outputs = embedder(texts, return_tensors = True)
    
    embeddings = [out.mean(dim = 1).squeeze(0) for out in outputs]
    return torch.stack(embeddings)

def sort_by_AC(target_title, title_list):
    if not target_title or not title_list:
        return []

    target_emb = get_embeddings([target_title])
    list_embs = get_embeddings(title_list)

    similarities = F.cosine_similarity(target_emb, list_embs)

    results = []
    for title, score in zip(title_list, similarities):
        results.append((title, round(score.item(), 4)))

    results.sort(key = lambda x : x[1], reverse = True)

    rst = []
    for i in results :
        rst.append(i[0])

    return rst