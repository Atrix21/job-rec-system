from recommender.hybrid_kg import HybridKG
from recommender.qdrant_store import QdrantVectorStore

# --- Manually Crafted Job Postings ---
manual_jobs = [
    {
        "title": "Data Scientist",
        "description": "Join our analytics team to build predictive models, analyze large datasets, and deploy machine learning solutions using Python and SQL. Collaborate with business stakeholders to deliver actionable insights.",
        "required_skills": ["Python", "Machine Learning", "SQL", "Data Analysis"],
        "optional_skills": ["TensorFlow", "Statistics", "AWS"]
    },
    {
        "title": "Frontend Developer",
        "description": "Develop modern web applications using React and TypeScript. Work closely with designers to create responsive, user-friendly interfaces. Optimize performance and ensure cross-browser compatibility.",
        "required_skills": ["React", "TypeScript", "HTML", "CSS"],
        "optional_skills": ["JavaScript", "Bootstrap", "APIs"]
    },
    {
        "title": "DevOps Engineer",
        "description": "Design and maintain CI/CD pipelines, manage cloud infrastructure on AWS, and automate deployments using Docker and Kubernetes. Ensure system reliability and scalability.",
        "required_skills": ["AWS", "Docker", "Kubernetes", "CI/CD"],
        "optional_skills": ["Linux", "Cloud Computing", "Python"]
    },
    {
        "title": "Project Manager",
        "description": "Lead agile software development teams, manage project timelines, and communicate with stakeholders. Use Jira and Confluence to track progress and documentation.",
        "required_skills": ["Project Management", "Agile", "Jira", "Leadership"],
        "optional_skills": ["Scrum", "Communication", "Confluence"]
    },
    {
        "title": "Business Analyst",
        "description": "Analyze business processes, gather requirements, and work with cross-functional teams to deliver data-driven solutions. Create reports and dashboards using Excel and Power BI.",
        "required_skills": ["Business Analysis", "Excel", "Power BI", "Communication"],
        "optional_skills": ["SQL", "Presentation", "Teamwork"]
    },
    {
        "title": "Backend Developer",
        "description": "Build and maintain server-side applications using Java and SQL. Develop RESTful APIs and ensure high performance and responsiveness to requests from the frontend.",
        "required_skills": ["Java", "SQL", "APIs", "Backend"],
        "optional_skills": ["NoSQL", "Docker", "Linux"]
    },
    {
        "title": "Full Stack Developer",
        "description": "Work on both frontend and backend of web applications. Use React, Node.js, and SQL to deliver end-to-end solutions. Collaborate with designers and product managers.",
        "required_skills": ["React", "Node.js", "SQL", "Full Stack"],
        "optional_skills": ["TypeScript", "APIs", "AWS"]
    },
    {
        "title": "QA Engineer",
        "description": "Develop and execute test plans to ensure software quality. Use automated testing tools and collaborate with developers to resolve issues.",
        "required_skills": ["Testing", "Automation", "APIs", "Problem Solving"],
        "optional_skills": ["Python", "CI/CD", "Jira"]
    },
    {
        "title": "Cloud Solutions Architect",
        "description": "Design scalable cloud architectures on AWS and Azure. Guide development teams in best practices for cloud deployments and security.",
        "required_skills": ["AWS", "Cloud Computing", "Architecture", "Security"],
        "optional_skills": ["Docker", "Kubernetes", "Linux"]
    },
    {
        "title": "Data Engineer",
        "description": "Build and optimize data pipelines using Python and Spark. Work with large datasets and ensure data quality and reliability.",
        "required_skills": ["Python", "Spark", "Data Pipelines", "ETL"],
        "optional_skills": ["SQL", "AWS", "Hadoop"]
    },
    {
        "title": "AI Researcher",
        "description": "Conduct research in artificial intelligence and machine learning. Publish papers and develop prototypes for new AI algorithms.",
        "required_skills": ["Machine Learning", "AI", "Python", "Research"],
        "optional_skills": ["Deep Learning", "TensorFlow", "PyTorch"]
    },
    {
        "title": "NLP Engineer",
        "description": "Develop natural language processing models for text analysis and chatbots. Use Python and NLP libraries to process and understand language data.",
        "required_skills": ["Python", "NLP", "Machine Learning", "Text Analysis"],
        "optional_skills": ["TensorFlow", "Deep Learning", "APIs"]
    },
    {
        "title": "Computer Vision Engineer",
        "description": "Build computer vision models for image and video analysis. Use deep learning frameworks and work with large image datasets.",
        "required_skills": ["Python", "Computer Vision", "Deep Learning", "Image Processing"],
        "optional_skills": ["TensorFlow", "PyTorch", "AWS"]
    },
    {
        "title": "Database Administrator",
        "description": "Manage and optimize SQL and NoSQL databases. Ensure data security, backup, and recovery.",
        "required_skills": ["SQL", "NoSQL", "Database Management", "Security"],
        "optional_skills": ["Linux", "Cloud Computing", "Python"]
    },
    {
        "title": "IT Project Manager",
        "description": "Oversee IT projects from inception to completion. Manage teams, budgets, and timelines. Use Agile methodologies and tools like Jira.",
        "required_skills": ["Project Management", "Agile", "Jira", "IT"],
        "optional_skills": ["Scrum", "Leadership", "Communication"]
    },
    {
        "title": "BI Developer",
        "description": "Develop business intelligence solutions using Power BI and SQL. Create dashboards and reports for business users.",
        "required_skills": ["Power BI", "SQL", "Data Visualization", "BI"],
        "optional_skills": ["Excel", "ETL", "Python"]
    },
    {
        "title": "ETL Developer",
        "description": "Design and implement ETL processes for data integration. Work with SQL and Python to move and transform data.",
        "required_skills": ["ETL", "SQL", "Python", "Data Integration"],
        "optional_skills": ["AWS", "Hadoop", "Spark"]
    },
    {
        "title": "Software Engineer",
        "description": "Develop and maintain software applications using Java and C++. Collaborate with cross-functional teams to deliver high-quality products.",
        "required_skills": ["Java", "C++", "Software Development", "Problem Solving"],
        "optional_skills": ["Python", "APIs", "Testing"]
    },
    {
        "title": "Systems Analyst",
        "description": "Analyze and improve IT systems. Gather requirements and design solutions to meet business needs.",
        "required_skills": ["Systems Analysis", "Business Analysis", "SQL", "Communication"],
        "optional_skills": ["Project Management", "Excel", "Presentation"]
    },
    {
        "title": "Network Engineer",
        "description": "Design, implement, and maintain network infrastructure. Troubleshoot network issues and ensure security.",
        "required_skills": ["Networking", "Security", "Linux", "Troubleshooting"],
        "optional_skills": ["AWS", "Cloud Computing", "Python"]
    },
    {
        "title": "Security Analyst",
        "description": "Monitor and respond to security incidents. Conduct vulnerability assessments and implement security best practices.",
        "required_skills": ["Security", "Vulnerability Assessment", "Incident Response", "Linux"],
        "optional_skills": ["Python", "Cloud Computing", "Networking"]
    },
    {
        "title": "Mobile App Developer",
        "description": "Develop mobile applications for iOS and Android platforms. Use React Native and ensure high performance and usability.",
        "required_skills": ["React Native", "Mobile Development", "JavaScript", "APIs"],
        "optional_skills": ["iOS", "Android", "Testing"]
    },
    {
        "title": "Web Developer",
        "description": "Build and maintain websites using HTML, CSS, and JavaScript. Ensure responsive design and cross-browser compatibility.",
        "required_skills": ["HTML", "CSS", "JavaScript", "Web Development"],
        "optional_skills": ["React", "Bootstrap", "APIs"]
    },
    {
        "title": "Solutions Engineer",
        "description": "Work with clients to design and implement technical solutions. Provide pre-sales support and technical expertise.",
        "required_skills": ["Solutions Design", "Client Interaction", "Technical Expertise", "Presentation"],
        "optional_skills": ["APIs", "Cloud Computing", "Python"]
    },
    {
        "title": "Technical Lead",
        "description": "Lead a team of engineers to deliver software projects. Mentor team members and ensure best practices are followed.",
        "required_skills": ["Leadership", "Software Development", "Mentoring", "Project Management"],
        "optional_skills": ["Agile", "Scrum", "Communication"]
    },
    {
        "title": "Support Engineer",
        "description": "Provide technical support to customers. Troubleshoot issues and resolve problems efficiently.",
        "required_skills": ["Technical Support", "Troubleshooting", "Communication", "Customer Service"],
        "optional_skills": ["APIs", "Linux", "Cloud Computing"]
    }
]


# --- Build Hybrid KG ---
def load_all():
    kg = HybridKG()
    job_id_to_int = {}
    int_to_job_id = {}
    for i, job in enumerate(manual_jobs):
        job_id = f"job_{i+1}"
        kg.add_job(job_id, job["title"], job["description"], job["required_skills"], job["optional_skills"])
        job_id_to_int[job_id] = i
        int_to_job_id[i] = job_id
    kg.add_job(
        "job_generic",
        "Generalist",
        "We are looking for a motivated individual to join our team. Responsibilities include working on various projects, collaborating with others, and learning new skills as needed. Good communication and teamwork are required.",
        ["Communication", "Teamwork"],
        ["Problem Solving", "Presentation"]
    )
    generic_job_int_id = len(job_id_to_int)
    job_id_to_int["job_generic"] = generic_job_int_id
    int_to_job_id[generic_job_int_id] = "job_generic"
    kg.add_skill_similarity_edges()
    kg.add_job_to_job_similarity_edges(threshold=0.7)
    resumes = [
        {
            'resume_id': 'resume_1',
            'name': 'Alice',
            'summary': 'Experienced data scientist with expertise in Python, machine learning, and cloud computing. Built scalable ML pipelines and deployed models on AWS.',
            'priority_skills': ['Python', 'Machine Learning', 'AWS', 'Data Analysis'],
            'other_skills': ['SQL', 'TensorFlow', 'Statistics', 'Linux']
        },
        {
            'resume_id': 'resume_2',
            'name': 'Bob',
            'summary': 'Frontend developer skilled in React, Node.js, and TypeScript. Developed modern web apps and collaborated with designers and backend teams.',
            'priority_skills': ['React', 'Node.js', 'TypeScript', 'HTML'],
            'other_skills': ['CSS', 'APIs', 'JavaScript', 'Bootstrap']
        },
        {
            'resume_id': 'resume_3',
            'name': 'Carol',
            'summary': 'Project manager with strong leadership and communication skills. Led agile teams and delivered projects using Jira and Confluence.',
            'priority_skills': ['Project Management', 'Leadership', 'Agile', 'Jira'],
            'other_skills': ['Scrum', 'Communication', 'Confluence', 'Teamwork']
        },
        {
            'resume_id': 'resume_4',
            'name': 'Zara',
            'summary': 'Expert in quantum cryptography and blockchain consensus algorithms. Looking for research roles in quantum computing.',
            'priority_skills': ['Quantum Cryptography', 'Blockchain', 'Consensus Algorithms', 'Quantum Computing'],
            'other_skills': ['Distributed Systems', 'Post-Quantum Security']
        },
        # 20 more resumes
        {
            'resume_id': 'resume_5',
            'name': 'David',
            'summary': 'DevOps engineer with experience in AWS, Docker, and Kubernetes. Automated CI/CD pipelines and managed cloud deployments.',
            'priority_skills': ['AWS', 'Docker', 'Kubernetes', 'CI/CD'],
            'other_skills': ['Linux', 'Cloud Computing', 'Python']
        },
        {
            'resume_id': 'resume_6',
            'name': 'Eva',
            'summary': 'Business analyst skilled in Excel, Power BI, and SQL. Delivered actionable insights and created dashboards for management.',
            'priority_skills': ['Business Analysis', 'Excel', 'Power BI', 'Communication'],
            'other_skills': ['SQL', 'Presentation', 'Teamwork']
        },
        {
            'resume_id': 'resume_7',
            'name': 'Frank',
            'summary': 'Backend developer with expertise in Java, SQL, and RESTful APIs. Built scalable server-side applications.',
            'priority_skills': ['Java', 'SQL', 'APIs', 'Backend'],
            'other_skills': ['NoSQL', 'Docker', 'Linux']
        },
        {
            'resume_id': 'resume_8',
            'name': 'Grace',
            'summary': 'Full stack developer proficient in React, Node.js, and SQL. Delivered end-to-end web solutions.',
            'priority_skills': ['React', 'Node.js', 'SQL', 'Full Stack'],
            'other_skills': ['TypeScript', 'APIs', 'AWS']
        },
        {
            'resume_id': 'resume_9',
            'name': 'Henry',
            'summary': 'QA engineer with experience in automated testing and problem solving. Collaborated with developers to ensure software quality.',
            'priority_skills': ['Testing', 'Automation', 'APIs', 'Problem Solving'],
            'other_skills': ['Python', 'CI/CD', 'Jira']
        },
        {
            'resume_id': 'resume_10',
            'name': 'Ivy',
            'summary': 'Cloud architect with expertise in AWS, cloud computing, and security. Designed scalable cloud solutions.',
            'priority_skills': ['AWS', 'Cloud Computing', 'Architecture', 'Security'],
            'other_skills': ['Docker', 'Kubernetes', 'Linux']
        },
        {
            'resume_id': 'resume_11',
            'name': 'Jack',
            'summary': 'Data engineer skilled in Python, Spark, and ETL. Built and optimized data pipelines.',
            'priority_skills': ['Python', 'Spark', 'Data Pipelines', 'ETL'],
            'other_skills': ['SQL', 'AWS', 'Hadoop']
        },
        {
            'resume_id': 'resume_12',
            'name': 'Kathy',
            'summary': 'AI researcher with a background in machine learning and deep learning. Published papers and developed AI prototypes.',
            'priority_skills': ['Machine Learning', 'AI', 'Python', 'Research'],
            'other_skills': ['Deep Learning', 'TensorFlow', 'PyTorch']
        },
        {
            'resume_id': 'resume_13',
            'name': 'Leo',
            'summary': 'NLP engineer with experience in text analysis and chatbot development. Used Python and NLP libraries.',
            'priority_skills': ['Python', 'NLP', 'Machine Learning', 'Text Analysis'],
            'other_skills': ['TensorFlow', 'Deep Learning', 'APIs']
        },
        {
            'resume_id': 'resume_14',
            'name': 'Mona',
            'summary': 'Computer vision engineer with expertise in image processing and deep learning. Worked with large image datasets.',
            'priority_skills': ['Python', 'Computer Vision', 'Deep Learning', 'Image Processing'],
            'other_skills': ['TensorFlow', 'PyTorch', 'AWS']
        },
        {
            'resume_id': 'resume_15',
            'name': 'Nate',
            'summary': 'Database administrator experienced in SQL, NoSQL, and database management. Ensured data security and reliability.',
            'priority_skills': ['SQL', 'NoSQL', 'Database Management', 'Security'],
            'other_skills': ['Linux', 'Cloud Computing', 'Python']
        },
        {
            'resume_id': 'resume_16',
            'name': 'Olivia',
            'summary': 'IT project manager with experience in Agile and Jira. Managed teams and delivered IT projects on time.',
            'priority_skills': ['Project Management', 'Agile', 'Jira', 'IT'],
            'other_skills': ['Scrum', 'Leadership', 'Communication']
        },
        {
            'resume_id': 'resume_17',
            'name': 'Paul',
            'summary': 'BI developer skilled in Power BI, SQL, and data visualization. Created dashboards and reports.',
            'priority_skills': ['Power BI', 'SQL', 'Data Visualization', 'BI'],
            'other_skills': ['Excel', 'ETL', 'Python']
        },
        {
            'resume_id': 'resume_18',
            'name': 'Quinn',
            'summary': 'ETL developer with experience in data integration and Python. Designed and implemented ETL processes.',
            'priority_skills': ['ETL', 'SQL', 'Python', 'Data Integration'],
            'other_skills': ['AWS', 'Hadoop', 'Spark']
        },
        {
            'resume_id': 'resume_19',
            'name': 'Rita',
            'summary': 'Software engineer with expertise in Java, C++, and software development. Delivered high-quality products.',
            'priority_skills': ['Java', 'C++', 'Software Development', 'Problem Solving'],
            'other_skills': ['Python', 'APIs', 'Testing']
        },
        {
            'resume_id': 'resume_20',
            'name': 'Sam',
            'summary': 'Systems analyst skilled in business analysis and SQL. Designed solutions to meet business needs.',
            'priority_skills': ['Systems Analysis', 'Business Analysis', 'SQL', 'Communication'],
            'other_skills': ['Project Management', 'Excel', 'Presentation']
        },
        {
            'resume_id': 'resume_21',
            'name': 'Tina',
            'summary': 'Network engineer with experience in networking, security, and troubleshooting. Maintained network infrastructure.',
            'priority_skills': ['Networking', 'Security', 'Linux', 'Troubleshooting'],
            'other_skills': ['AWS', 'Cloud Computing', 'Python']
        },
        {
            'resume_id': 'resume_22',
            'name': 'Uma',
            'summary': 'Security analyst skilled in vulnerability assessment and incident response. Monitored and responded to security incidents.',
            'priority_skills': ['Security', 'Vulnerability Assessment', 'Incident Response', 'Linux'],
            'other_skills': ['Python', 'Cloud Computing', 'Networking']
        },
        {
            'resume_id': 'resume_23',
            'name': 'Victor',
            'summary': 'Mobile app developer with expertise in React Native and mobile development. Built apps for iOS and Android.',
            'priority_skills': ['React Native', 'Mobile Development', 'JavaScript', 'APIs'],
            'other_skills': ['iOS', 'Android', 'Testing']
        },
        {
            'resume_id': 'resume_24',
            'name': 'Wendy',
            'summary': 'Web developer skilled in HTML, CSS, and JavaScript. Built and maintained responsive websites.',
            'priority_skills': ['HTML', 'CSS', 'JavaScript', 'Web Development'],
            'other_skills': ['React', 'Bootstrap', 'APIs']
        },
        {
            'resume_id': 'resume_25',
            'name': 'Xander',
            'summary': 'Technical lead with experience in software development and mentoring. Led teams to deliver software projects.',
            'priority_skills': ['Leadership', 'Software Development', 'Mentoring', 'Project Management'],
            'other_skills': ['Agile', 'Scrum', 'Communication']
        },
        {
            'resume_id': 'resume_26',
            'name': 'Yara',
            'summary': 'Support engineer with expertise in technical support and troubleshooting. Provided efficient customer service.',
            'priority_skills': ['Technical Support', 'Troubleshooting', 'Communication', 'Customer Service'],
            'other_skills': ['APIs', 'Linux', 'Cloud Computing']
        }
    ]
    for r in resumes:
        kg.add_resume(r['resume_id'], r['name'], r['summary'], r['priority_skills'], r['other_skills'])
    qdrant = QdrantVectorStore()
    for int_id, job_id in int_to_job_id.items():
        job = kg.jobs[job_id]
        qdrant.upsert_job(
            int_id,
            kg.job_embeddings[job_id],
            {
                "title": job["title"],
                "description": job["description"],
                "required_skills": job["required_skills"],
                "optional_skills": job["optional_skills"]
            }
        )
    resume_id_to_int = {r['resume_id']: i for i, r in enumerate(resumes)}
    int_to_resume_id = {i: r['resume_id'] for i, r in enumerate(resumes)}
    for int_id, resume_id in int_to_resume_id.items():
        r = next(res for res in resumes if res['resume_id'] == resume_id)
        qdrant.upsert_resume(
            int_id,
            kg.resume_embeddings[resume_id],
            {
                "name": r["name"],
                "summary": r["summary"],
                "priority_skills": r["priority_skills"],
                "other_skills": r["other_skills"]
            }
        )
    jobs = [(job_id, kg.jobs[job_id]) for job_id in job_id_to_int]
    return kg, qdrant, jobs, resumes, int_to_job_id, job_id_to_int, int_to_resume_id, resume_id_to_int 