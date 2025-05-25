# Hybrid Job & Candidate Recommendation System

This project is an advanced job and candidate recommender system that combines a knowledge graph (KG) with semantic vector search using Qdrant. It supports both job recommendations for candidates (resumes) and candidate recommendations for job postings, using a hybrid of graph-based and embedding-based methods.

## Features

- **Hybrid Knowledge Graph**
  - Jobs, resumes, and skills are represented as nodes and edges
  - Skill similarity and job-to-job similarity are modeled in the KG
- **Semantic Vector Search**
  - Uses Sentence Transformers to generate embeddings for jobs and resumes
  - Qdrant is used for fast, scalable vector search
- **Flexible Recommendation**
  - Weighted skill overlap (with hard skill requirement)
  - Personalized PageRank on the KG
  - Qdrant-based semantic similarity
  - Hybrid scoring combining all methods
- **Easy Data Management**
  - All job postings and resumes are defined in `src/scripts/shared_setup.py`
  - Add or modify jobs/resumes by editing this file

## Project Structure

```
job-rec-system/
  src/
    recommender/
      hybrid_kg.py
      qdrant_store.py
      text_processor.py
    scripts/
      job_recommender.py
      candidate_recommender.py
      shared_setup.py
    main.py
  requirements.txt
  .env
  README.md
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Download the spaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```
3. Start a Qdrant instance (default: `http://localhost:6333`). Set the URL in `.env` if needed:
   ```
   QDRANT_URL=http://localhost:6333
   ```

## Usage

Run the main entry point:
```bash
python src/main.py
```
You will be prompted to choose:
- `1` for **Job Recommender** (find jobs for a candidate)
- `2` for **Candidate Recommender** (find candidates for a job)

Both recommenders will print sample jobs, resumes, and top recommendations using all hybrid methods.

## How It Works

- **All job postings and resumes are defined in `shared_setup.py`**
- The system builds a knowledge graph and generates embeddings for all jobs and resumes
- Jobs and resumes are upserted into Qdrant for vector search
- Recommendations are made using:
  - Weighted skill overlap (with hard skill requirement)
  - Personalized PageRank
  - Qdrant vector similarity
  - Hybrid scoring (combining the above)

## Adding Jobs or Resumes
- Edit `src/scripts/shared_setup.py` to add new job postings or resumes
- No need to change the recommender scripts

## Requirements
- Python 3.8+
- Qdrant running locally or remotely
- `requirements.txt` dependencies
- spaCy English model (`en_core_web_sm`)

## Notes
- No external job APIs, salary, or location filtering is included in this version
- All data is synthetic and for demonstration purposes

---
For further customization, extend the KG or scoring logic in `recommender/hybrid_kg.py` and `scripts/shared_setup.py`. 
