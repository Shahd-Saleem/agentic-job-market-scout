import json
import os
from langchain_core.tools import tool

def load_jobs_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "data", "mock_jobs.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@tool
def search_jobs(query: str, location: str, user_skills: list[str] = None) -> str:
    """
    Search available tech and AI job openings based on keywords and location. 
    Automatically calculates match percentage and missing skills for each job.
    """
    jobs = load_jobs_data()
    results = []
    
    query_lower = query.lower()
    loc_lower = location.lower()
    user = set(s.lower() for s in (user_skills or []))
    
    for job in jobs:
        loc_match = loc_lower in job["location"].lower()
        title_match = query_lower in job["title"].lower()
        desc_match = query_lower in job["description"].lower()
        skill_match = any(query_lower in skill.lower() for skill in job["required_skills"])
        
        if loc_match and (title_match or desc_match or skill_match or not query_lower):
            required = set(s.lower() for s in job["required_skills"])
            if user and required:
                matched = required.intersection(user)
                missing = required - user
                match_percentage = int((len(matched) / len(required)) * 100)
            else:
                missing = required
                match_percentage = 0
            
            job_copy = job.copy()
            job_copy["match_percentage"] = f"{match_percentage}%"
            job_copy["missing_skills"] = list(missing)
            results.append(job_copy)
            
    if not results:
        return f"No exact job matches found for '{query}' in '{location}'. Try broadening your search terms!"
        
    return json.dumps(results, indent=2)

@tool
def analyze_skill_gaps(user_skills: list[str], target_role: str) -> str:
    """
    Analyze the skill gaps between a candidate's current skills and a specific target role.
    """
    jobs = load_jobs_data()
    target_job = next((j for j in jobs if target_role.lower() in j["title"].lower() or target_role.lower() in j["company"].lower()), None)
    
    if not target_job:
        return f"Could not find a specific benchmark role matching '{target_role}'."
        
    required = set(s.lower() for s in target_job["required_skills"])
    user = set(s.lower() for s in user_skills)
    
    missing = required - user
    matched = required.intersection(user)
    
    match_percentage = int((len(matched) / len(required)) * 100) if required else 100
    
    report = {
        "target_role": target_job["title"],
        "company": target_job["company"],
        "match_percentage": f"{match_percentage}%",
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "recommendation": "Ready to apply!" if match_percentage >= 75 else "Recommended to upskill in missing areas before applying."
    }
    
    return json.dumps(report, indent=2)