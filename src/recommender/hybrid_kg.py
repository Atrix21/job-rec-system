import networkx as nx
from typing import List, Dict, Any, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class HybridKG:
    """Hybrid Knowledge Graph for jobs, resumes, and skills/technologies, with weights, similarity, and embeddings."""
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.graph = nx.Graph()
        self.jobs = {}
        self.resumes = {}
        self.skills = set()
        self.skill_synonyms = self._default_skill_synonyms()
        self.model = SentenceTransformer(model_name)
        self.job_embeddings = {}  # job_id -> np.array
        self.resume_embeddings = {}  # resume_id -> np.array

    def _default_skill_synonyms(self):
        # Simple synonym/relatedness dictionary for demo
        return {
            'Python': ['Programming', 'Scripting'],
            'SQL': ['Databases', 'Data Management'],
            'Machine Learning': ['ML', 'AI', 'Artificial Intelligence'],
            'Deep Learning': ['Neural Networks'],
            'Data Analysis': ['Analytics', 'Data Analytics'],
            'TensorFlow': ['Deep Learning', 'ML'],
            'PyTorch': ['Deep Learning', 'ML'],
            'React': ['Frontend', 'Web Development'],
            'Node.js': ['Backend', 'Web Development'],
            'AWS': ['Cloud', 'Cloud Computing'],
            'Docker': ['Containers'],
            'Kubernetes': ['Containers', 'Orchestration'],
            'Excel': ['Spreadsheets'],
            'Power BI': ['Data Visualization'],
            'Tableau': ['Data Visualization'],
            'Linux': ['Unix'],
            'CI/CD': ['DevOps'],
            'Agile': ['Scrum', 'Project Management'],
            'Jira': ['Project Management'],
            'Confluence': ['Documentation'],
        }

    def add_skill_similarity_edges(self):
        for skill, similars in self.skill_synonyms.items():
            for sim in similars:
                if skill in self.skills and sim in self.skills:
                    self.graph.add_edge(skill, sim, type='similar_skill', weight=0.7)

    def add_job(self, job_id: str, title: str, description: str, required_skills: List[str], optional_skills: Optional[List[str]] = None):
        self.graph.add_node(job_id, type='job', title=title, description=description)
        self.jobs[job_id] = {
            'title': title,
            'description': description,
            'required_skills': required_skills,
            'optional_skills': optional_skills or []
        }
        # Add required skills (weight 1.0)
        for skill in required_skills:
            self.graph.add_node(skill, type='skill')
            self.graph.add_edge(job_id, skill, type='requires', weight=1.0)
            self.skills.add(skill)
        # Add optional skills (weight 0.5)
        for skill in (optional_skills or []):
            self.graph.add_node(skill, type='skill')
            self.graph.add_edge(job_id, skill, type='optional', weight=0.5)
            self.skills.add(skill)
        # Compute and store job embedding
        self.job_embeddings[job_id] = self.model.encode(description)

    def add_resume(self, resume_id: str, name: str, summary: str, priority_skills: List[str], other_skills: Optional[List[str]] = None):
        self.graph.add_node(resume_id, type='resume', name=name, summary=summary)
        self.resumes[resume_id] = {
            'name': name,
            'summary': summary,
            'priority_skills': priority_skills,
            'other_skills': other_skills or []
        }
        # Add priority skills (weight 1.2)
        for skill in priority_skills:
            self.graph.add_node(skill, type='skill')
            self.graph.add_edge(resume_id, skill, type='priority', weight=1.2)
            self.skills.add(skill)
        # Add other skills (weight 0.7)
        for skill in (other_skills or []):
            self.graph.add_node(skill, type='skill')
            self.graph.add_edge(resume_id, skill, type='has', weight=0.7)
            self.skills.add(skill)
        # Compute and store resume embedding
        self.resume_embeddings[resume_id] = self.model.encode(summary)

    def add_job_to_job_similarity_edges(self, threshold: float = 0.7):
        # Add edges between jobs with similar descriptions (cosine sim > threshold)
        job_ids = list(self.jobs.keys())
        embs = np.array([self.job_embeddings[jid] for jid in job_ids])
        sims = cosine_similarity(embs)
        for i, jid1 in enumerate(job_ids):
            for j, jid2 in enumerate(job_ids):
                if i < j and sims[i, j] > threshold:
                    self.graph.add_edge(jid1, jid2, type='similar_job', weight=sims[i, j])

    def recommend_jobs_hybrid(self, resume_id: str, top_k: int = 5, alpha: float = 0.5, beta: float = 0.3) -> List[Dict[str, Any]]:
        """
        Hybrid: combine KG overlap, Personalized PageRank, and embedding similarity.
        alpha: weight for overlap, beta: weight for embedding, (1-alpha-beta): weight for PageRank
        """
        # KG Overlap (weighted)
        resume_node = resume_id
        resume_skills = set(self.resumes[resume_id]['priority_skills'] + self.resumes[resume_id]['other_skills'])
        job_scores_overlap = {}
        for job_id, job in self.jobs.items():
            score = 0.0
            for skill in job['required_skills']:
                if skill in resume_skills:
                    score += 1.0
                else:
                    # Check for similar skills
                    for sim in self.skill_synonyms.get(skill, []):
                        if sim in resume_skills:
                            score += 0.7
            for skill in job['optional_skills']:
                if skill in resume_skills:
                    score += 0.5
                else:
                    for sim in self.skill_synonyms.get(skill, []):
                        if sim in resume_skills:
                            score += 0.35
            total = len(job['required_skills']) + 0.5 * len(job['optional_skills'])
            if total > 0:
                job_scores_overlap[job_id] = score / total
        # Personalized PageRank
        seeds = {n: 1.0 if n in resume_skills else 0.0 for n in self.graph.nodes}
        pr = nx.pagerank(self.graph, personalization=seeds, alpha=0.85, max_iter=100)
        job_scores_pr = {jid: pr[jid] for jid in self.jobs if jid in pr}
        # Embedding similarity
        resume_emb = self.resume_embeddings[resume_id]
        job_embs = np.array([self.job_embeddings[jid] for jid in self.jobs])
        emb_sims = cosine_similarity([resume_emb], job_embs)[0]
        job_ids = list(self.jobs.keys())
        job_scores_emb = {jid: emb_sims[i] for i, jid in enumerate(job_ids)}
        # Combine
        all_jobs = set(job_scores_overlap) | set(job_scores_pr) | set(job_scores_emb)
        combined = {}
        for jid in all_jobs:
            combined[jid] = (
                alpha * job_scores_overlap.get(jid, 0) +
                beta * job_scores_emb.get(jid, 0) +
                (1 - alpha - beta) * job_scores_pr.get(jid, 0)
            )
        ranked = sorted(combined.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [{
            'job_id': jid,
            'title': self.jobs[jid]['title'],
            'score': score,
            'description': self.jobs[jid]['description']
        } for jid, score in ranked] 