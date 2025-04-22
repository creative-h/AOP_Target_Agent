#!/usr/bin/env python
# coding: utf-8

"""
Data source functions for the AOP Target Breakdown Agent.
These functions simulate retrieving data from various systems like iEvolve, iGlance, etc.
In a real implementation, these would connect to actual data sources.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Generate random dates within the current year
def random_date(start_date=None, end_date=None):
    if not start_date:
        start_date = datetime(datetime.now().year, 1, 1)
    if not end_date:
        end_date = datetime(datetime.now().year, 12, 31)
    
    delta = end_date - start_date
    random_days = random.randrange(delta.days)
    return start_date + timedelta(days=random_days)

# Mock learning activity data
def generate_learning_activities(count=50):
    """Generate mock learning activities"""
    activity_types = ["VILT", "ILT"]
    competency_areas = ["Technical", "Soft Skills", "Leadership", "Domain Knowledge", "Process"]
    course_titles = [
        "Python Programming Fundamentals", "Advanced Java Development", 
        "Cloud Architecture Principles", "DevOps Essentials",
        "Effective Communication", "Leadership Skills", 
        "Project Management", "Agile Methodologies",
        "Data Science Basics", "Machine Learning Fundamentals",
        "Cybersecurity Essentials", "Blockchain Technology"
    ]
    
    activities = []
    for i in range(count):
        activity_type = random.choice(activity_types)
        competency = random.choice(competency_areas)
        title = random.choice(course_titles)
        
        # Generate more realistic data based on activity type
        if activity_type == "VILT":
            duration = random.uniform(1.0, 4.0)  # 1-4 hours
            capacity = random.randint(15, 50)
        else:  # ILT
            duration = random.uniform(4.0, 16.0)  # 4-16 hours (1-2 days)
            capacity = random.randint(10, 30)
        
        # Generate realistic registration and completion numbers
        registrations = random.randint(int(capacity * 0.5), capacity)
        completion_rate = random.uniform(0.7, 0.95)
        completions = int(registrations * completion_rate)
        
        activity = {
            "id": f"ACT-{i+1000}",
            "title": title,
            "type": activity_type,
            "duration_hours": round(duration, 1),
            "competency_area": competency,
            "scheduled_date": random_date(),
            "capacity": capacity,
            "registrations": registrations,
            "completion_count": completions
        }
        activities.append(activity)
    
    return activities

# Mock learning plan data
def get_learning_plan_data():
    """Get mock learning plan data"""
    glds = [
        {"id": "GLD001", "name": "John Smith", "department": "Technology"},
        {"id": "GLD002", "name": "Sarah Johnson", "department": "Operations"},
        {"id": "GLD003", "name": "Michael Chen", "department": "Finance"}
    ]
    
    learning_plans = []
    for gld in glds:
        # Generate different numbers of activities for different GLDs
        activity_count = random.randint(30, 70)
        activities = generate_learning_activities(activity_count)
        
        learning_plan = {
            "gld_id": gld["id"],
            "gld_name": gld["name"],
            "department": gld["department"],
            "activities": activities
        }
        learning_plans.append(learning_plan)
    
    return learning_plans

# Mock iEvolve data
def get_ievolve_data():
    """Get mock data from iEvolve system"""
    competency_frameworks = [
        {
            "name": "Technical Skills Framework",
            "competencies": [
                {"name": "Programming", "levels": ["Basic", "Intermediate", "Advanced"]},
                {"name": "Cloud Computing", "levels": ["Basic", "Intermediate", "Advanced"]},
                {"name": "Data Science", "levels": ["Basic", "Intermediate", "Advanced"]},
                {"name": "Cybersecurity", "levels": ["Basic", "Intermediate", "Advanced"]}
            ]
        },
        {
            "name": "Soft Skills Framework",
            "competencies": [
                {"name": "Communication", "levels": ["Basic", "Intermediate", "Advanced"]},
                {"name": "Teamwork", "levels": ["Basic", "Intermediate", "Advanced"]},
                {"name": "Problem Solving", "levels": ["Basic", "Intermediate", "Advanced"]}
            ]
        },
        {
            "name": "Leadership Framework",
            "competencies": [
                {"name": "Strategic Thinking", "levels": ["Basic", "Intermediate", "Advanced"]},
                {"name": "People Management", "levels": ["Basic", "Intermediate", "Advanced"]},
                {"name": "Change Management", "levels": ["Basic", "Intermediate", "Advanced"]}
            ]
        }
    ]
    
    # Generate employee competency data
    employee_count = 500
    employees = []
    for i in range(employee_count):
        employee = {
            "id": f"EMP{i+1000}",
            "department": random.choice(["Technology", "Operations", "Finance", "Marketing", "HR"]),
            "competencies": []
        }
        
        # Assign random competencies to each employee
        for framework in competency_frameworks:
            for competency in framework["competencies"]:
                if random.random() > 0.5:  # 50% chance of having this competency
                    employee["competencies"].append({
                        "name": competency["name"],
                        "framework": framework["name"],
                        "level": random.choice(competency["levels"]),
                        "last_assessed": random_date().strftime("%Y-%m-%d")
                    })
        
        employees.append(employee)
    
    return {
        "frameworks": competency_frameworks,
        "employees": employees
    }

# Mock iGlance data
def get_iglance_data():
    """Get mock data from iGlance system"""
    departments = ["Technology", "Operations", "Finance", "Marketing", "HR"]
    learning_metrics = []
    
    for department in departments:
        # Generate quarterly metrics for each department
        for quarter in range(1, 5):
            quarter_metrics = {
                "department": department,
                "quarter": f"Q{quarter}",
                "metrics": {
                    "total_learning_hours": random.randint(1000, 3000),
                    "vilt_sessions": random.randint(20, 50),
                    "ilt_sessions": random.randint(5, 20),
                    "average_completion_rate": round(random.uniform(0.7, 0.95), 2),
                    "average_satisfaction_score": round(random.uniform(3.5, 4.8), 1),
                    "competency_improvement": {
                        "Technical": round(random.uniform(0.1, 0.3), 2),
                        "Soft Skills": round(random.uniform(0.1, 0.3), 2),
                        "Leadership": round(random.uniform(0.1, 0.3), 2)
                    }
                }
            }
            learning_metrics.append(quarter_metrics)
    
    return {
        "learning_metrics": learning_metrics,
        "current_year": datetime.now().year
    }

# Mock AFTD (Advanced Framework for Talent Development) data
def get_aftd_data():
    """Get mock data from AFTD system"""
    skill_gap_analysis = []
    departments = ["Technology", "Operations", "Finance", "Marketing", "HR"]
    skill_areas = [
        "Programming", "Cloud Computing", "Data Science", "Cybersecurity",
        "Communication", "Teamwork", "Problem Solving",
        "Strategic Thinking", "People Management", "Change Management"
    ]
    
    for department in departments:
        department_gaps = {
            "department": department,
            "skill_gaps": []
        }
        
        # Generate skill gaps for each department
        for skill in skill_areas:
            if random.random() > 0.3:  # 70% chance of having a gap in this skill
                gap = {
                    "skill": skill,
                    "current_level": round(random.uniform(1.0, 3.5), 1),
                    "target_level": round(random.uniform(3.5, 5.0), 1),
                    "gap": round(random.uniform(0.5, 2.0), 1),
                    "priority": random.choice(["Low", "Medium", "High"]),
                    "recommended_courses": random.sample([
                        "Python Programming Fundamentals", "Advanced Java Development", 
                        "Cloud Architecture Principles", "DevOps Essentials",
                        "Effective Communication", "Leadership Skills", 
                        "Project Management", "Agile Methodologies",
                        "Data Science Basics", "Machine Learning Fundamentals",
                        "Cybersecurity Essentials", "Blockchain Technology"
                    ], random.randint(1, 3))
                }
                department_gaps["skill_gaps"].append(gap)
        
        skill_gap_analysis.append(department_gaps)
    
    return {
        "skill_gap_analysis": skill_gap_analysis,
        "analysis_date": datetime.now().strftime("%Y-%m-%d")
    }

# Mock Internal Internship data
def get_internal_internship_data():
    """Get mock data from Internal Internship system"""
    internship_programs = [
        {
            "id": "INT001",
            "name": "Data Science Internship",
            "duration_weeks": 12,
            "department": "Technology",
            "skills_developed": ["Python", "Data Analysis", "Machine Learning"],
            "capacity": 20,
            "current_participants": random.randint(10, 20),
            "completion_rate": round(random.uniform(0.7, 0.95), 2),
            "satisfaction_score": round(random.uniform(3.5, 4.8), 1)
        },
        {
            "id": "INT002",
            "name": "Cloud Engineering Internship",
            "duration_weeks": 10,
            "department": "Technology",
            "skills_developed": ["AWS", "Azure", "DevOps"],
            "capacity": 15,
            "current_participants": random.randint(8, 15),
            "completion_rate": round(random.uniform(0.7, 0.95), 2),
            "satisfaction_score": round(random.uniform(3.5, 4.8), 1)
        },
        {
            "id": "INT003",
            "name": "Financial Analysis Internship",
            "duration_weeks": 8,
            "department": "Finance",
            "skills_developed": ["Financial Modeling", "Data Analysis", "Reporting"],
            "capacity": 12,
            "current_participants": random.randint(6, 12),
            "completion_rate": round(random.uniform(0.7, 0.95), 2),
            "satisfaction_score": round(random.uniform(3.5, 4.8), 1)
        },
        {
            "id": "INT004",
            "name": "Project Management Internship",
            "duration_weeks": 16,
            "department": "Operations",
            "skills_developed": ["Project Planning", "Agile", "Stakeholder Management"],
            "capacity": 10,
            "current_participants": random.randint(5, 10),
            "completion_rate": round(random.uniform(0.7, 0.95), 2),
            "satisfaction_score": round(random.uniform(3.5, 4.8), 1)
        }
    ]
    
    return {
        "internship_programs": internship_programs,
        "current_year": datetime.now().year
    }

# Test function
if __name__ == "__main__":
    # Test data generation
    learning_plans = get_learning_plan_data()
    ievolve_data = get_ievolve_data()
    iglance_data = get_iglance_data()
    aftd_data = get_aftd_data()
    internship_data = get_internal_internship_data()
    
    print(f"Generated {len(learning_plans)} learning plans")
    for plan in learning_plans:
        print(f"  GLD: {plan['gld_name']}, Activities: {len(plan['activities'])}")
    
    print(f"iEvolve data: {len(ievolve_data['employees'])} employees")
    print(f"iGlance data: {len(iglance_data['learning_metrics'])} metrics entries")
    print(f"AFTD data: {len(aftd_data['skill_gap_analysis'])} department analyses")
    print(f"Internship data: {len(internship_data['internship_programs'])} programs")
