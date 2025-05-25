from recommender.hybrid_kg import HybridKG
from recommender.qdrant_store import QdrantVectorStore
import networkx as nx
from scripts.shared_setup import load_all

SOFT_SKILLS = {
    "Communication", "Teamwork", "Presentation", "Problem Solving", "Leadership", "Customer Service",
    "Collaboration", "Time Management", "Adaptability", "Creativity", "Critical Thinking", "Organization",
    "Interpersonal Skills", "Flexibility", "Work Ethic", "Attention to Detail", "Empathy", "Conflict Resolution"
}

def is_soft_skill(skill):
    return skill in SOFT_SKILLS

def recommend_candidates_for_job(kg, qdrant, resumes, int_to_resume_id, job_id, job, top_k=5):
    job_skills = set(job['required_skills'] + job['optional_skills'])
    print(f"\n--- Top Candidates for {job['title']} ---")
    # KG Overlap (weighted, hard skill required)
    print("-- KG Overlap (weighted, hard skill required) --")
    resume_scores_overlap = {}
    for r in resumes:
        score = 0.0
        hard_skill_matched = False
        for skill in r['priority_skills']:
            if skill in job_skills:
                weight = 0.5 if is_soft_skill(skill) else 1.0
                score += weight
                if not is_soft_skill(skill):
                    hard_skill_matched = True
            else:
                for sim in kg.skill_synonyms.get(skill, []):
                    if sim in job_skills:
                        weight = 0.35 if is_soft_skill(skill) else 0.7
                        score += weight
                        if not is_soft_skill(skill):
                            hard_skill_matched = True
        for skill in r['other_skills']:
            if skill in job_skills:
                weight = 0.25 if is_soft_skill(skill) else 0.5
                score += weight
                if not is_soft_skill(skill):
                    hard_skill_matched = True
            else:
                for sim in kg.skill_synonyms.get(skill, []):
                    if sim in job_skills:
                        weight = 0.175 if is_soft_skill(skill) else 0.35
                        score += weight
                        if not is_soft_skill(skill):
                            hard_skill_matched = True
        total = sum(1.0 if not is_soft_skill(s) else 0.5 for s in r['priority_skills']) + \
                sum(0.5 if not is_soft_skill(s) else 0.25 for s in r['other_skills'])
        if total > 0 and hard_skill_matched:
            resume_scores_overlap[r['resume_id']] = score / total
    ranked_overlap = sorted(resume_scores_overlap.items(), key=lambda x: x[1], reverse=True)[:top_k]
    for rid, score in ranked_overlap:
        print(f"{rid} (score: {score:.3f})")
    # PageRank
    print("-- PageRank --")
    seeds = {n: 1.0 if n in job_skills else 0.0 for n in kg.graph.nodes}
    pr = nx.pagerank(kg.graph, personalization=seeds, alpha=0.85, max_iter=100)
    resume_scores_pr = {rid: pr[rid] for rid in kg.resume_embeddings if rid in pr}
    ranked_pr = sorted(resume_scores_pr.items(), key=lambda x: x[1], reverse=True)[:top_k]
    for rid, score in ranked_pr:
        print(f"{rid} (score: {score:.6f})")
    # Qdrant vector search (job embedding, search resumes)
    print("-- Qdrant Vector Search --")
    job_emb = kg.job_embeddings[job_id]
    qdrant_results = qdrant.search_resume(job_emb, top_k=top_k)
    for res in qdrant_results:
        resume_id = int_to_resume_id[int(res['resume_id'])]
        print(f"{resume_id} (score: {res['score']:.6f})")
    # Hybrid: use Qdrant resume search for embedding score
    print("-- Hybrid --")
    qdrant_all = qdrant.search_resume(job_emb, top_k=len(resumes))
    qdrant_score_map = {int_to_resume_id[int(res['resume_id'])]: res['score'] for res in qdrant_all}
    alpha, beta = 0.4, 0.4
    hybrid_scores = {}
    for rid in resume_scores_overlap:
        overlap = resume_scores_overlap.get(rid, 0.0)
        pr_score = resume_scores_pr.get(rid, 0.0)
        emb_score = qdrant_score_map.get(rid, 0.0)
        hybrid_scores[rid] = alpha * overlap + beta * pr_score + (1 - alpha - beta) * emb_score
    ranked_hybrid = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    for rid, score in ranked_hybrid:
        print(f"{rid} (score: {score:.3f})")

def main():
    kg, qdrant, jobs, resumes, int_to_job_id, job_id_to_int, int_to_resume_id, resume_id_to_int = load_all()
    print("\nAvailable Jobs:")
    for idx, (job_id, job) in enumerate(jobs):
        print(f"{idx+1}. {job['title']} - {job['description'][:60]}...")
    choice = input("Select a job by number: ").strip()
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(jobs):
            raise ValueError
    except Exception:
        print("Invalid selection.")
        return
    job_id, job = jobs[idx]
    recommend_candidates_for_job(kg, qdrant, resumes, int_to_resume_id, job_id, job)

if __name__ == "__main__":
    main() 