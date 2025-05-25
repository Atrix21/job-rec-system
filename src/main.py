def main():
    print("Select recommender type:")
    print("1. Job Recommender (test script: all resumes, all jobs, full output)")
    print("2. Candidate Recommender (interactive: pick a job, see top candidates)")
    choice = input("Enter 1 or 2: ").strip()
    if choice == "1":
        import scripts.job_recommender
    elif choice == "2":
        from scripts.candidate_recommender import main as cand_main
        cand_main()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()