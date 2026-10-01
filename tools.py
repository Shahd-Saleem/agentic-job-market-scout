import json
import os
from langchain_core.tools import tool

@tool
def search_jobs(location: str, industry: str, seniority: str, user_skills: list[str]) -> str:
    """
    Search for job postings in mock_jobs.json matching location, industry, and seniority,
    and compute a skill match score for the user.
    """
    data_path = os.path.join(os.path.dirname(__file__), "../data/mock_jobs.json")
    if not os.path.exists(data_path):
        return "Job database not found."
        
    with open(data_path, "r") as f:
        jobs = json.load(f)
        
    results = []
    user_skills_lower = [s.lower() for s in user_skills]

    for job in jobs:
        loc_match = location.lower() in job["location"].lower()
        ind_match = industry.lower() in job["industry"].lower()
        sen_match = seniority.lower() in job["seniority"].lower()
        
        if loc_match and ind_match and sen_match:
            required = job.get("required_skills", [])
            
            if required:
                matched_skills = [s for s in required if s.lower() in user_skills_lower]
                match_percentage = f"{int((len(matched_skills) / len(required)) * 100)}%"
            else:
                matched_skills = []
                match_percentage = "N/A (No requirements specified)"
            
            job_copy = job.copy()
            job_copy["match_percentage"] = match_percentage
            job_copy["matched_skills"] = matched_skills
            results.append(job_copy)
            
    if not results:
        return f"No jobs found matching location '{location}', industry '{industry}', and seniority '{seniority}'."
        
    return json.dumps(results, indent=2)


@tool
def analyze_skill_gaps(user_skills: list[str], projects: list[str], certifications: list[str], industry: str) -> str:
    """
    Analyze skill gaps by cross-referencing user skills, projects, and certifications 
    against industry baselines.
    """
    industry_baselines = {
        "ai engineering": ["Python", "Agentic AI", "LLMs", "Docker", "RAG", "Prompt Engineering"],
        "machine learning": ["Python", "PyTorch", "Scikit-Learn", "Pandas", "Docker"],
        "software engineering": ["Python/Java/JavaScript", "Data Structures", "Git", "System Design", "Docker", "SQL"],
        "web development": ["JavaScript/TypeScript", "React", "HTML/CSS", "Node.js", "REST APIs", "GitHub"],
        "consulting": ["Problem Solving", "Data Analysis", "Client Communication", "Excel/PowerPoint", "Strategic Frameworks"],
        "product management": ["User Research", "Roadmapping", "Agile/Scrum", "Data Analytics", "GitHub"],
        "cybersecurity": ["Network Security", "Python", "Linux", "SIEM", "Penetration Testing", "IAM"],
        "data engineering": ["SQL", "Python", "Apache Spark", "Airflow", "Docker", "PostgreSQL"],
        "cloud computing": ["AWS/Azure", "Terraform", "Docker", "Kubernetes", "Linux", "CI/CD"]
    }
    
    industry_key = industry.lower()
    required_baseline = industry_baselines.get(industry_key, ["Python", "Git", "Problem Solving", "SQL"])
    
    # Combine explicit skills, projects, and certifications into one text block for holistic evaluation
    all_user_competencies = " ".join(user_skills + projects + certifications).lower()
    
    missing_skills = [s for s in required_baseline if s.lower() not in all_user_competencies]
    acquired_skills = [s for s in required_baseline if s.lower() in all_user_competencies]
    
    readiness_score = int((len(acquired_skills) / len(required_baseline)) * 100) if required_baseline else 100
    
    analysis = {
        "industry": industry,
        "readiness_score": f"{readiness_score}%",
        "acquired_core_skills": acquired_skills,
        "missing_gaps": missing_skills,
        "portfolio_projects_evaluated": len(projects),
        "certifications_evaluated": len(certifications),
        "strategic_recommendation": f"To hit 100% readiness in {industry}, prioritize building projects or gaining certifications in: {', '.join(missing_skills)}." if missing_skills else f"Your profile shows complete baseline readiness for top-tier {industry} roles!"
    }
    
    return json.dumps(analysis, indent=2)