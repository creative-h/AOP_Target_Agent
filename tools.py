#!/usr/bin/env python
# coding: utf-8

"""
Tools for the AOP Target Breakdown Agent.
These tools provide the core functionality for the agent system.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import math
import json
from crewai.tools import tool

# Import data models
from .models import (
    AOPTarget, 
    LearningPlan, 
    RiskAssessment, 
    Opportunity, 
    DiagnosticReport,
    TimeframeTasks,
    TargetBreakdown,
    GapAnalysis
)

@tool("Break down AOP targets into timeframes")
def breakdown_targets(aop_targets: Dict[str, Any]) -> Dict[str, Any]:
    """
    Break down annual AOP targets into quarterly, monthly, weekly, and daily tasks.
    
    Args:
        aop_targets: Dictionary containing the annual targets
        
    Returns:
        Dictionary with target breakdowns for different timeframes
    """
    # Convert input to AOPTarget model
    annual_targets = {
        "vilt_target": aop_targets.get("vilt_target", 0),
        "ilt_target": aop_targets.get("ilt_target", 0),
        "learning_hours_target": aop_targets.get("learning_hours_target", 0),
        "competency_targets": aop_targets.get("competency_targets", {})
    }
    
    # Create quarterly breakdown (distribution weights by quarter)
    quarterly_weights = [0.25, 0.30, 0.25, 0.20]  # Q1, Q2, Q3, Q4
    quarterly_breakdown = []
    
    for i, weight in enumerate(quarterly_weights):
        quarter = f"Q{i+1}"
        quarterly_targets = {
            "timeframe_name": quarter,
            "vilt_target": annual_targets["vilt_target"] * weight,
            "ilt_target": annual_targets["ilt_target"] * weight,
            "learning_hours_target": annual_targets["learning_hours_target"] * weight,
            "competency_targets": {k: v * weight for k, v in annual_targets["competency_targets"].items()},
            "tasks": [
                f"Plan {quarter} VILT and ILT schedule",
                f"Allocate resources for {quarter} training delivery",
                f"Set up tracking for {quarter} learning metrics"
            ]
        }
        quarterly_breakdown.append(quarterly_targets)
    
    # Create monthly breakdown (12 months)
    monthly_weights = [0.08, 0.08, 0.09, 0.09, 0.09, 0.12, 0.08, 0.08, 0.09, 0.08, 0.06, 0.06]  # Jan-Dec
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    monthly_breakdown = []
    
    for i, (month, weight) in enumerate(zip(months, monthly_weights)):
        monthly_targets = {
            "timeframe_name": month,
            "vilt_target": annual_targets["vilt_target"] * weight,
            "ilt_target": annual_targets["ilt_target"] * weight,
            "learning_hours_target": annual_targets["learning_hours_target"] * weight,
            "competency_targets": {k: v * weight for k, v in annual_targets["competency_targets"].items()},
            "tasks": [
                f"Schedule {math.ceil(annual_targets['vilt_target'] * weight)} VILT sessions",
                f"Schedule {math.ceil(annual_targets['ilt_target'] * weight)} ILT sessions",
                f"Monitor registration and completion rates",
                f"Adjust schedule based on demand and feedback"
            ]
        }
        monthly_breakdown.append(monthly_targets)
    
    # Create weekly breakdown (sample for 4 weeks)
    weekly_breakdown = []
    for i in range(1, 5):
        week = f"Week {i}"
        # Assuming 4 weeks per month on average
        weekly_weight = monthly_weights[0] / 4  # Using January as reference
        weekly_targets = {
            "timeframe_name": week,
            "vilt_target": annual_targets["vilt_target"] * weekly_weight,
            "ilt_target": annual_targets["ilt_target"] * weekly_weight,
            "learning_hours_target": annual_targets["learning_hours_target"] * weekly_weight,
            "competency_targets": {k: v * weekly_weight for k, v in annual_targets["competency_targets"].items()},
            "tasks": [
                f"Confirm trainers for {week} sessions",
                f"Send reminders to registered participants",
                f"Prepare training materials and environments",
                f"Review feedback from previous week's sessions"
            ]
        }
        weekly_breakdown.append(weekly_targets)
    
    # Create daily to-do lists (sample for 5 days)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    daily_breakdown = []
    
    for day in days:
        daily_tasks = {
            "day": day,
            "tasks": [
                f"Review {day}'s scheduled sessions",
                f"Check registration numbers for upcoming sessions",
                f"Follow up on participant feedback",
                f"Update tracking dashboards",
                f"Coordinate with trainers and support staff"
            ]
        }
        daily_breakdown.append(daily_tasks)
    
    # Combine all breakdowns
    return {
        "annual": annual_targets,
        "quarterly": quarterly_breakdown,
        "monthly": monthly_breakdown,
        "weekly": weekly_breakdown,
        "daily": daily_breakdown
    }

@tool("Analyze learning plan to track VILTs and ILTs")
def analyze_learning_plan(learning_plan_data: Dict[str, Any], aop_targets: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze the learning plan to track VILTs and ILTs and identify any gaps.
    
    Args:
        learning_plan_data: Learning plan data containing scheduled activities
        aop_targets: Dictionary containing the annual targets
        
    Returns:
        Analysis of the learning plan with counts and metrics
    """
    # Process learning plan data
    total_vilt_count = 0
    total_ilt_count = 0
    total_learning_hours = 0
    competency_hours = {}
    
    # Aggregate data across all GLDs
    for plan in learning_plan_data:
        # Count VILT and ILT sessions
        for activity in plan.get("activities", []):
            if activity.get("type") == "VILT":
                total_vilt_count += 1
            elif activity.get("type") == "ILT":
                total_ilt_count += 1
            
            # Calculate learning hours
            duration = activity.get("duration_hours", 0)
            completions = activity.get("completion_count", 0)
            hours = duration * completions
            total_learning_hours += hours
            
            # Aggregate by competency area
            competency = activity.get("competency_area")
            if competency:
                if competency in competency_hours:
                    competency_hours[competency] += hours
                else:
                    competency_hours[competency] = hours
    
    # Calculate registration and completion metrics
    registration_rates = []
    completion_rates = []
    for plan in learning_plan_data:
        for activity in plan.get("activities", []):
            capacity = activity.get("capacity", 0)
            registrations = activity.get("registrations", 0)
            completions = activity.get("completion_count", 0)
            
            if capacity > 0:
                registration_rates.append(registrations / capacity)
            if registrations > 0:
                completion_rates.append(completions / registrations)
    
    avg_registration_rate = sum(registration_rates) / len(registration_rates) if registration_rates else 0
    avg_completion_rate = sum(completion_rates) / len(completion_rates) if completion_rates else 0
    
    # Prepare analysis results
    analysis = {
        "total_vilt_count": total_vilt_count,
        "total_ilt_count": total_ilt_count,
        "total_learning_hours": total_learning_hours,
        "competency_hours": competency_hours,
        "avg_registration_rate": avg_registration_rate,
        "avg_completion_rate": avg_completion_rate,
        "gld_breakdown": []
    }
    
    # Add per-GLD breakdown
    for plan in learning_plan_data:
        gld_vilt_count = sum(1 for activity in plan.get("activities", []) if activity.get("type") == "VILT")
        gld_ilt_count = sum(1 for activity in plan.get("activities", []) if activity.get("type") == "ILT")
        
        gld_analysis = {
            "gld_id": plan.get("gld_id"),
            "gld_name": plan.get("gld_name"),
            "department": plan.get("department"),
            "vilt_count": gld_vilt_count,
            "ilt_count": gld_ilt_count
        }
        analysis["gld_breakdown"].append(gld_analysis)
    
    return analysis

@tool("Calculate gap between targets and current plan")
def calculate_gap(learning_plan_analysis: Dict[str, Any], aop_targets: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate the gap between AOP targets and the current learning plan.
    Uses '0' to indicate no gap (on track).
    
    Args:
        learning_plan_analysis: Analysis of the current learning plan
        aop_targets: Dictionary containing the annual targets
        
    Returns:
        Gap analysis with indicators
    """
    # Extract values from inputs
    vilt_target = aop_targets.get("vilt_target", 0)
    ilt_target = aop_targets.get("ilt_target", 0)
    learning_hours_target = aop_targets.get("learning_hours_target", 0)
    competency_targets = aop_targets.get("competency_targets", {})
    
    vilt_scheduled = learning_plan_analysis.get("total_vilt_count", 0)
    ilt_scheduled = learning_plan_analysis.get("total_ilt_count", 0)
    learning_hours_scheduled = learning_plan_analysis.get("total_learning_hours", 0)
    competency_hours = learning_plan_analysis.get("competency_hours", {})
    
    # Calculate gaps
    vilt_gap = vilt_target - vilt_scheduled
    ilt_gap = ilt_target - ilt_scheduled
    learning_hours_gap = learning_hours_target - learning_hours_scheduled
    
    # Calculate gap indicators (0 = No Gap)
    vilt_gap_indicator = 0 if vilt_scheduled >= vilt_target else vilt_gap
    ilt_gap_indicator = 0 if ilt_scheduled >= ilt_target else ilt_gap
    learning_hours_gap_indicator = 0 if learning_hours_scheduled >= learning_hours_target else learning_hours_gap
    
    # Calculate competency gaps
    competency_gaps = {}
    for competency, target in competency_targets.items():
        actual = competency_hours.get(competency, 0)
        gap = target - actual
        gap_indicator = 0 if actual >= target else gap
        
        competency_gaps[competency] = {
            "target": target,
            "actual": actual,
            "gap": gap,
            "gap_indicator": gap_indicator
        }
    
    # Create gap analysis result
    gap_analysis = {
        "vilt_scheduled": vilt_scheduled,
        "vilt_gap": vilt_gap,
        "vilt_gap_indicator": vilt_gap_indicator,
        "ilt_scheduled": ilt_scheduled,
        "ilt_gap": ilt_gap,
        "ilt_gap_indicator": ilt_gap_indicator,
        "learning_hours_scheduled": learning_hours_scheduled,
        "learning_hours_gap": learning_hours_gap,
        "learning_hours_gap_indicator": learning_hours_gap_indicator,
        "competency_gaps": competency_gaps
    }
    
    return gap_analysis

@tool("Assess risk factors in learning plan execution")
def assess_risk(gap_analysis: Dict[str, Any], learning_plan_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Identify risk factors when GLD schedules, offering registrations, and closure ratios
    don't match the desired numbers for AOP targets.
    
    Args:
        gap_analysis: Gap analysis between targets and current plan
        learning_plan_analysis: Analysis of the learning plan
        
    Returns:
        List of identified risk factors with severity and mitigation suggestions
    """
    risk_factors = []
    
    # Check VILT gap
    vilt_gap = gap_analysis.get("vilt_gap", 0)
    if vilt_gap > 0:
        vilt_risk = {
            "risk_area": "VILT Session Count",
            "current_value": str(gap_analysis.get("vilt_scheduled", 0)),
            "target_value": str(gap_analysis.get("vilt_scheduled", 0) + vilt_gap),
            "risk_level": "High" if vilt_gap > 50 else "Medium" if vilt_gap > 20 else "Low",
            "impact": f"May miss VILT target by {vilt_gap} sessions",
            "mitigation": "Schedule additional VILT sessions, prioritizing high-impact courses"
        }
        risk_factors.append(vilt_risk)
    
    # Check ILT gap
    ilt_gap = gap_analysis.get("ilt_gap", 0)
    if ilt_gap > 0:
        ilt_risk = {
            "risk_area": "ILT Session Count",
            "current_value": str(gap_analysis.get("ilt_scheduled", 0)),
            "target_value": str(gap_analysis.get("ilt_scheduled", 0) + ilt_gap),
            "risk_level": "High" if ilt_gap > 20 else "Medium" if ilt_gap > 10 else "Low",
            "impact": f"May miss ILT target by {ilt_gap} sessions",
            "mitigation": "Schedule additional ILT sessions, consider converting some to VILT format"
        }
        risk_factors.append(ilt_risk)
    
    # Check learning hours gap
    learning_hours_gap = gap_analysis.get("learning_hours_gap", 0)
    if learning_hours_gap > 0:
        hours_risk = {
            "risk_area": "Learning Hours",
            "current_value": str(int(gap_analysis.get("learning_hours_scheduled", 0))),
            "target_value": str(int(gap_analysis.get("learning_hours_scheduled", 0) + learning_hours_gap)),
            "risk_level": "High" if learning_hours_gap > 1000 else "Medium" if learning_hours_gap > 500 else "Low",
            "impact": f"May miss learning hours target by {int(learning_hours_gap)} hours",
            "mitigation": "Increase session capacity and promote registration"
        }
        risk_factors.append(hours_risk)
    
    # Check competency gaps
    competency_gaps = gap_analysis.get("competency_gaps", {})
    for competency, gap_data in competency_gaps.items():
        if gap_data.get("gap", 0) > 0:
            competency_risk = {
                "risk_area": f"{competency} Competency",
                "current_value": str(int(gap_data.get("actual", 0))),
                "target_value": str(int(gap_data.get("target", 0))),
                "risk_level": "High" if gap_data.get("gap", 0) > 500 else "Medium" if gap_data.get("gap", 0) > 200 else "Low",
                "impact": f"May miss {competency} competency target by {int(gap_data.get('gap', 0))} hours",
                "mitigation": f"Prioritize {competency} courses in upcoming schedule"
            }
            risk_factors.append(competency_risk)
    
    # Check registration rate
    avg_registration_rate = learning_plan_analysis.get("avg_registration_rate", 0)
    if avg_registration_rate < 0.8:  # Less than 80% registration rate
        registration_risk = {
            "risk_area": "Registration Rate",
            "current_value": f"{int(avg_registration_rate * 100)}%",
            "target_value": "80%",
            "risk_level": "High" if avg_registration_rate < 0.6 else "Medium",
            "impact": "Low registration rates may lead to session cancellations and inefficient resource use",
            "mitigation": "Improve communication and marketing of learning opportunities"
        }
        risk_factors.append(registration_risk)
    
    # Check completion rate
    avg_completion_rate = learning_plan_analysis.get("avg_completion_rate", 0)
    if avg_completion_rate < 0.85:  # Less than 85% completion rate
        completion_risk = {
            "risk_area": "Completion Rate",
            "current_value": f"{int(avg_completion_rate * 100)}%",
            "target_value": "85%",
            "risk_level": "High" if avg_completion_rate < 0.7 else "Medium",
            "impact": "Low completion rates reduce effective learning hours and competency development",
            "mitigation": "Implement pre-session preparation and post-session follow-up"
        }
        risk_factors.append(completion_risk)
    
    return risk_factors

@tool("Identify opportunities based on learning data trends")
def identify_opportunities(gap_analysis: Dict[str, Any], risk_assessment: List[Dict[str, Any]], 
                          learning_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Identify opportunities based on learning data trends to help meet AOP targets.
    
    Args:
        gap_analysis: Gap analysis between targets and current plan
        risk_assessment: Risk assessment results
        learning_data: Combined learning data from various sources
        
    Returns:
        List of identified opportunities with expected impact
    """
    opportunities = []
    
    # Extract key data points
    vilt_gap = gap_analysis.get("vilt_gap", 0)
    ilt_gap = gap_analysis.get("ilt_gap", 0)
    learning_hours_gap = gap_analysis.get("learning_hours_gap", 0)
    competency_gaps = gap_analysis.get("competency_gaps", {})
    
    # Opportunity 1: Convert ILT to VILT if appropriate
    if ilt_gap > 0 and vilt_gap > 0:
        # Assuming VILT sessions can accommodate more participants
        opportunity = {
            "opportunity": f"Convert {min(5, ilt_gap)} ILT sessions to VILT format",
            "impact": f"Increase capacity by approximately {min(5, ilt_gap) * 15} participants and reduce delivery costs",
            "resources_needed": "Updated materials, virtual platform setup, trainer preparation",
            "timeframe": "Next 4-6 weeks"
        }
        opportunities.append(opportunity)
    
    # Opportunity 2: Focus on high-gap competency areas
    high_gap_competencies = []
    for competency, gap_data in competency_gaps.items():
        if gap_data.get("gap", 0) > 200:  # Significant gap
            high_gap_competencies.append((competency, gap_data.get("gap", 0)))
    
    if high_gap_competencies:
        # Sort by gap size (descending)
        high_gap_competencies.sort(key=lambda x: x[1], reverse=True)
        top_competency, top_gap = high_gap_competencies[0]
        
        opportunity = {
            "opportunity": f"Schedule 3 additional {top_competency} bootcamps",
            "impact": f"Will address approximately {min(top_gap, 300)} learning hours of the {top_competency} competency gap",
            "resources_needed": f"Specialized {top_competency} trainers, dedicated learning environments",
            "timeframe": "Next quarter"
        }
        opportunities.append(opportunity)
    
    # Opportunity 3: Improve completion rates
    high_risk_areas = [risk for risk in risk_assessment if risk.get("risk_level") == "High"]
    if any(risk.get("risk_area") == "Completion Rate" for risk in high_risk_areas):
        opportunity = {
            "opportunity": "Implement a structured follow-up program for all courses",
            "impact": "Could improve completion rates by 15-20%, adding approximately 500-1000 learning hours",
            "resources_needed": "Learning experience team, automated reminder system",
            "timeframe": "Immediate implementation"
        }
        opportunities.append(opportunity)
    
    # Opportunity 4: Leverage internal internship programs
    opportunity = {
        "opportunity": "Integrate learning objectives into internal internship programs",
        "impact": "Can generate 200-300 additional learning hours while providing practical experience",
        "resources_needed": "Coordination with internship program managers, learning objective alignment",
        "timeframe": "Next internship cycle"
    }
    opportunities.append(opportunity)
    
    # Opportunity 5: Batch scheduling of related courses
    opportunity = {
        "opportunity": "Create learning paths with batch scheduling of related courses",
        "impact": "Can increase registration rates by 25% through clear progression paths",
        "resources_needed": "Learning path design, coordinated scheduling",
        "timeframe": "Next planning cycle"
    }
    opportunities.append(opportunity)
    
    return opportunities

@tool("Generate diagnostic reports for Leaders and TD")
def generate_diagnostic_report(gap_analysis: Dict[str, Any], risk_assessment: List[Dict[str, Any]], 
                             opportunities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate diagnostic reports for Leaders and TD on skills strengths, weaknesses, and future risks.
    
    Args:
        gap_analysis: Gap analysis between targets and current plan
        risk_assessment: Risk assessment results
        opportunities: Identified opportunities
        
    Returns:
        Comprehensive diagnostic report with actionable insights
    """
    # Identify strengths (areas with no gap or exceeding targets)
    strengths = []
    
    if gap_analysis.get("vilt_gap_indicator", 0) == 0:
        strengths.append("VILT delivery is on track to meet or exceed targets")
    
    if gap_analysis.get("ilt_gap_indicator", 0) == 0:
        strengths.append("ILT delivery is on track to meet or exceed targets")
    
    for competency, gap_data in gap_analysis.get("competency_gaps", {}).items():
        if gap_data.get("gap_indicator", 0) == 0:
            strengths.append(f"{competency} competency development is on track to meet or exceed targets")
    
    # If we don't have any identified strengths, add some generic ones
    if not strengths:
        strengths = [
            "Strong foundation in technical training delivery",
            "Effective learning content development capabilities",
            "Established learning delivery infrastructure"
        ]
    
    # Identify weaknesses (areas with significant gaps)
    weaknesses = []
    
    if gap_analysis.get("vilt_gap_indicator", 0) > 50:
        weaknesses.append(f"Significant gap in VILT delivery ({gap_analysis.get('vilt_gap', 0)} sessions below target)")
    
    if gap_analysis.get("ilt_gap_indicator", 0) > 20:
        weaknesses.append(f"Significant gap in ILT delivery ({gap_analysis.get('ilt_gap', 0)} sessions below target)")
    
    for competency, gap_data in gap_analysis.get("competency_gaps", {}).items():
        if gap_data.get("gap_indicator", 0) > 200:
            weaknesses.append(f"Significant gap in {competency} competency development ({int(gap_data.get('gap', 0))} hours below target)")
    
    # Extract high-risk areas
    high_risks = [risk for risk in risk_assessment if risk.get("risk_level") == "High"]
    future_risks = []
    
    for risk in high_risks:
        future_risks.append(f"{risk.get('risk_area')}: {risk.get('impact')}")
    
    # Add some generic future risks if we don't have enough
    if len(future_risks) < 3:
        additional_risks = [
            "Increasing demand for specialized technical skills may outpace current learning delivery capacity",
            "Evolving learning modalities may require significant updates to current delivery methods",
            "Competition for learning time may reduce participation and completion rates"
        ]
        future_risks.extend(additional_risks[:3 - len(future_risks)])
    
    # Generate recommendations based on opportunities and risks
    recommendations = []
    
    for opportunity in opportunities[:3]:  # Take top 3 opportunities
        recommendations.append(f"{opportunity.get('opportunity')} - {opportunity.get('impact')}")
    
    # Add recommendations based on high risks
    for risk in high_risks[:2]:  # Take top 2 high risks
        recommendations.append(f"Address {risk.get('risk_area')} risk through {risk.get('mitigation')}")
    
    # Create the diagnostic report
    diagnostic_report = {
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "strengths": strengths,
        "weaknesses": weaknesses,
        "future_risks": future_risks,
        "recommendations": recommendations,
        "summary": f"The learning plan is currently {'on track' if not weaknesses else 'at risk'} for meeting AOP targets. "
                  f"{'Immediate action is required in the identified risk areas.' if weaknesses else 'Continue monitoring progress and implementing identified opportunities.'}"
    }
    
    return diagnostic_report
