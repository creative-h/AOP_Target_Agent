#!/usr/bin/env python
# coding: utf-8

"""
AOP Target Breakdown Agent

This agent system breaks down Annual Operating Plan (AOP) Targets into quarterly, 
monthly, weekly, and daily to-do lists for Group Learning Directors (GLDs).
It analyzes learning plans, tracks VILTs and ILTs, and provides risk assessments
and opportunity recommendations.
"""

import os
import sys
import json
import yaml
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

# Import crewAI components
from crewai import Agent, Task, Crew, LLM

# Import local modules
from .models import (
    AOPTarget, 
    LearningPlan, 
    RiskAssessment, 
    Opportunity, 
    DiagnosticReport,
    TimeframeTasks,
    TargetBreakdown
)
from .data_sources import (
    get_learning_plan_data,
    get_ievolve_data,
    get_iglance_data,
    get_aftd_data,
    get_internal_internship_data
)
from .tools import (
    analyze_learning_plan,
    calculate_gap,
    assess_risk,
    identify_opportunities,
    generate_diagnostic_report,
    breakdown_targets
)

# Load configuration
def load_config():
    """Load agent and task configurations from YAML files"""
    config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")
    
    configs = {}
    for config_type in ["agents", "tasks"]:
        config_path = os.path.join(config_dir, f"{config_type}.yaml")
        try:
            with open(config_path, "r") as file:
                configs[config_type] = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Warning: Configuration file {config_path} not found.")
            configs[config_type] = {}
    
    return configs.get("agents", {}), configs.get("tasks", {})

# Create agents
def create_agents(mock_mode=True):
    """Create the agent system for AOP target breakdown"""
    
    # Load agent and task configurations
    agents_config, tasks_config = load_config()
    
    # Initialize LLM with mock mode for testing
    llm = LLM(mock=mock_mode)
    
    print("Creating AOP Target Breakdown Agent System...")
    
    # Create Target Breakdown Agent
    target_breakdown_agent = Agent(
        role="AOP Target Breakdown Specialist",
        goal="Break down AOP targets into quarterly, monthly, weekly, and daily tasks",
        backstory="As a specialist in operational planning, you excel at breaking down annual targets into actionable timeframes that make large goals achievable.",
        llm=llm,
        tools=[breakdown_targets],
        verbose=True
    )
    
    # Create Learning Plan Analysis Agent
    learning_plan_agent = Agent(
        role="Learning Plan Analyst",
        goal="Analyze learning plans to track VILTs and ILTs and identify gaps",
        backstory="With expertise in learning and development metrics, you specialize in analyzing learning plans and identifying gaps in training delivery.",
        llm=llm,
        tools=[analyze_learning_plan, calculate_gap],
        verbose=True
    )
    
    # Create Risk Assessment Agent
    risk_assessment_agent = Agent(
        role="Risk Assessment Specialist",
        goal="Identify risk factors in learning plan execution and registration metrics",
        backstory="Your background in risk management allows you to identify potential issues in learning plan execution before they become problems.",
        llm=llm,
        tools=[assess_risk],
        verbose=True
    )
    
    # Create Opportunity Identification Agent
    opportunity_agent = Agent(
        role="Learning Opportunity Advisor",
        goal="Identify opportunities based on learning data trends",
        backstory="You have a talent for spotting patterns in learning data and translating them into actionable opportunities for improvement.",
        llm=llm,
        tools=[identify_opportunities],
        verbose=True
    )
    
    # Create Diagnostic Report Agent
    diagnostic_agent = Agent(
        role="Learning Diagnostics Expert",
        goal="Generate comprehensive diagnostic reports on skills strengths, weaknesses, and future risks",
        backstory="Your analytical skills allow you to create insightful diagnostic reports that help leaders make informed decisions about learning initiatives.",
        llm=llm,
        tools=[generate_diagnostic_report],
        verbose=True
    )
    
    # Create tasks
    target_breakdown_task = Task(
        description="Break down the annual AOP targets into quarterly, monthly, weekly, and daily to-do lists that are realistic and achievable.",
        expected_output="A structured breakdown of AOP targets across different timeframes with specific action items.",
        agent=target_breakdown_agent
    )
    
    learning_plan_task = Task(
        description="Analyze the learning plan to identify the number of VILTs and ILTs scheduled and determine if there are any gaps in meeting targets.",
        expected_output="A detailed analysis of the learning plan with gap indicators (0 = No Gap) for each target area.",
        agent=learning_plan_agent,
        context=[target_breakdown_task]
    )
    
    risk_assessment_task = Task(
        description="Identify risk factors when GLD schedules, offering registrations, and closure ratios don't match the desired numbers for AOP targets.",
        expected_output="A risk assessment report highlighting areas where targets may be missed and the severity of each risk.",
        agent=risk_assessment_agent,
        context=[target_breakdown_task, learning_plan_task]
    )
    
    opportunity_task = Task(
        description="Analyze learning data trends to identify opportunities for meeting AOP targets more effectively.",
        expected_output="A list of specific opportunities with quantifiable impacts, such as 'If you schedule 3 XYZ Bootcamp, you can meet your goal of ABC LH & DEF Competency'.",
        agent=opportunity_agent,
        context=[learning_plan_task, risk_assessment_task]
    )
    
    diagnostic_task = Task(
        description="Generate diagnostic reports for Leaders and TD on skills strengths, weaknesses, and future risks based on all available data.",
        expected_output="Comprehensive diagnostic reports that provide actionable insights for leadership decision-making.",
        agent=diagnostic_agent,
        context=[learning_plan_task, risk_assessment_task, opportunity_task]
    )
    
    # Create crew
    crew = Crew(
        agents=[
            target_breakdown_agent,
            learning_plan_agent,
            risk_assessment_agent,
            opportunity_agent,
            diagnostic_agent
        ],
        tasks=[
            target_breakdown_task,
            learning_plan_task,
            risk_assessment_task,
            opportunity_task,
            diagnostic_task
        ],
        verbose=True
    )
    
    return crew

# Main function to run the agent
def run_aop_target_agent(aop_targets, mock_mode=True):
    """Run the AOP Target Breakdown Agent system"""
    
    print("Starting AOP Target Breakdown Analysis...")
    
    # Create crew
    crew = create_agents(mock_mode=mock_mode)
    
    # Prepare input data
    input_data = {
        'aop_targets': aop_targets,
        'current_date': datetime.now().strftime("%Y-%m-%d"),
        'learning_plan_data': get_learning_plan_data(),
        'ievolve_data': get_ievolve_data(),
        'iglance_data': get_iglance_data(),
        'aftd_data': get_aftd_data(),
        'internal_internship_data': get_internal_internship_data()
    }
    
    # Run the crew
    print("Starting the crew analysis process...")
    try:
        result = crew.kickoff(inputs=input_data)
        print("AOP Target Breakdown Analysis complete!")
        return result
    except Exception as e:
        print(f"Error during crew execution: {e}")
        # Return mock results for demonstration
        return generate_mock_results(aop_targets)

def generate_mock_results(aop_targets):
    """Generate mock results for demonstration purposes"""
    
    # Mock target breakdown
    target_breakdown = {
        "annual": aop_targets,
        "quarterly": [
            {"quarter": "Q1", "vilt_target": aop_targets["vilt_target"] * 0.2, "ilt_target": aop_targets["ilt_target"] * 0.2},
            {"quarter": "Q2", "vilt_target": aop_targets["vilt_target"] * 0.3, "ilt_target": aop_targets["ilt_target"] * 0.3},
            {"quarter": "Q3", "vilt_target": aop_targets["vilt_target"] * 0.3, "ilt_target": aop_targets["ilt_target"] * 0.3},
            {"quarter": "Q4", "vilt_target": aop_targets["vilt_target"] * 0.2, "ilt_target": aop_targets["ilt_target"] * 0.2}
        ],
        "monthly": [
            {"month": "January", "vilt_target": aop_targets["vilt_target"] * 0.07, "ilt_target": aop_targets["ilt_target"] * 0.07},
            {"month": "February", "vilt_target": aop_targets["vilt_target"] * 0.07, "ilt_target": aop_targets["ilt_target"] * 0.07},
            # Additional months would be included here
        ],
        "weekly": [
            {"week": "Week 1", "vilt_target": aop_targets["vilt_target"] * 0.02, "ilt_target": aop_targets["ilt_target"] * 0.02},
            {"week": "Week 2", "vilt_target": aop_targets["vilt_target"] * 0.02, "ilt_target": aop_targets["ilt_target"] * 0.02},
            # Additional weeks would be included here
        ],
        "daily": [
            {"day": "Monday", "tasks": ["Schedule 2 VILT sessions", "Review 1 ILT curriculum"]},
            {"day": "Tuesday", "tasks": ["Conduct 1 VILT session", "Prepare materials for ILT"]},
            # Additional days would be included here
        ]
    }
    
    # Mock gap analysis
    gap_analysis = {
        "vilt_scheduled": aop_targets["vilt_target"] * 0.8,
        "vilt_gap": aop_targets["vilt_target"] * 0.2,
        "vilt_gap_indicator": 0 if aop_targets["vilt_target"] * 0.8 >= aop_targets["vilt_target"] else aop_targets["vilt_target"] * 0.2,
        "ilt_scheduled": aop_targets["ilt_target"] * 0.7,
        "ilt_gap": aop_targets["ilt_target"] * 0.3,
        "ilt_gap_indicator": 0 if aop_targets["ilt_target"] * 0.7 >= aop_targets["ilt_target"] else aop_targets["ilt_target"] * 0.3
    }
    
    # Mock risk assessment
    risk_assessment = [
        {
            "risk_area": "VILT Registration Rate",
            "current_value": "75%",
            "target_value": "85%",
            "risk_level": "Medium",
            "impact": "May miss learning hours target by 10%",
            "mitigation": "Increase marketing of VILT sessions and send reminders"
        },
        {
            "risk_area": "ILT Completion Rate",
            "current_value": "80%",
            "target_value": "90%",
            "risk_level": "Low",
            "impact": "Minimal impact on overall targets",
            "mitigation": "Monitor attendance and follow up with participants"
        }
    ]
    
    # Mock opportunities
    opportunities = [
        {
            "opportunity": "Schedule 3 additional Python Bootcamps",
            "impact": "Will meet ABC Learning Hours target and DEF Competency goal",
            "resources_needed": "2 trainers, virtual lab environment",
            "timeframe": "Next 2 months"
        },
        {
            "opportunity": "Convert 2 ILT sessions to VILT format",
            "impact": "Increase participation by 25% and reduce delivery costs",
            "resources_needed": "Updated materials, virtual platform setup",
            "timeframe": "Next month"
        }
    ]
    
    # Mock diagnostic report
    diagnostic_report = {
        "strengths": [
            "Strong technical training delivery capability",
            "High participant satisfaction in cloud computing courses",
            "Effective virtual lab environments"
        ],
        "weaknesses": [
            "Low completion rates in self-paced courses",
            "Insufficient advanced-level offerings",
            "Limited instructor availability for specialized topics"
        ],
        "future_risks": [
            "Emerging skill gaps in AI and machine learning",
            "Increasing demand for hybrid learning formats",
            "Competition from external training providers"
        ],
        "recommendations": [
            "Develop more advanced-level technical courses",
            "Implement a hybrid learning strategy",
            "Expand instructor pool for specialized topics"
        ]
    }
    
    # Combine all results
    return {
        "target_breakdown": target_breakdown,
        "gap_analysis": gap_analysis,
        "risk_assessment": risk_assessment,
        "opportunities": opportunities,
        "diagnostic_report": diagnostic_report
    }

# Example usage
if __name__ == "__main__":
    # Example AOP targets
    aop_targets = {
        "vilt_target": 500,  # Number of VILT sessions for the year
        "ilt_target": 200,   # Number of ILT sessions for the year
        "learning_hours_target": 10000,  # Total learning hours
        "competency_targets": {
            "technical": 6000,
            "soft_skills": 2000,
            "leadership": 2000
        }
    }
    
    # Run the agent with mock mode enabled
    result = run_aop_target_agent(aop_targets, mock_mode=True)
    
    # Print the results
    print("\nAOP Target Breakdown Results:")
    print(json.dumps(result, indent=2))
