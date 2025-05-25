import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
from typing import List, Union
import logging

logger = logging.getLogger(__name__)

class TextProcessor:
    """Handles text preprocessing and embedding generation"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Initialize the text processor with specified models"""
        # Download required NLTK data
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        
        # Initialize models
        self.nlp = spacy.load('en_core_web_sm')
        self.embedding_model = SentenceTransformer(model_name)
        self.stop_words = set(stopwords.words('english'))
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text by tokenizing, removing stopwords, and lemmatizing"""
        # Tokenize and remove stopwords
        tokens = word_tokenize(text.lower())
        tokens = [t for t in tokens if t not in self.stop_words]
        
        # Lemmatize
        doc = self.nlp(" ".join(tokens))
        lemmatized = [token.lemma_ for token in doc]
        
        return " ".join(lemmatized)
    
    def create_embeddings(self, texts: Union[str, List[str]]) -> np.ndarray:
        """Create embeddings for a single text or list of texts"""
        if isinstance(texts, str):
            texts = [texts]
        
        # Preprocess texts
        processed_texts = [self.preprocess_text(text) for text in texts]
        
        # Create embeddings
        embeddings = self.embedding_model.encode(processed_texts)
        
        return embeddings
    
    def process_job_data(self, df: pd.DataFrame) -> tuple[np.ndarray, pd.DataFrame]:
        """Process job data and create embeddings"""
        # Combine relevant text fields
        text_data = df.apply(
            lambda x: f"{x['title']} {x['description']} {' '.join(x['skills'])}", 
            axis=1
        ).tolist()
        
        # Create embeddings
        embeddings = self.create_embeddings(text_data)
        
        return embeddings, df 