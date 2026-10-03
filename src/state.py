from typing import List, Optional
from pydantic import BaseModel, Field

class UserProfileState(BaseModel):
    industry: Optional[str] = Field(default=None, description="The user's professional industry (e.g., AI Engineering, Backend, Data Science)")
    seniority: Optional[str] = Field(default=None, description="Seniority level (e.g., Fresher, Mid, Senior)")
    tech_stack: List[str] = Field(default_factory=list, description="List of programming languages, frameworks, and tools the user knows")
    certifications: List[str] = Field(default_factory=list, description="List of certifications held by the user")
    projects: List[str] = Field(default_factory=list, description="Key projects built by the user")
    target_location: Optional[str] = Field(default=None, description="Target job location (e.g., Dubai, Riyadh)")
    
    is_complete: bool = Field(default=False, description="Flag indicating if all necessary profile info has been collected")