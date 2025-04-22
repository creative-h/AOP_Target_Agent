#!/usr/bin/env python
# coding: utf-8

"""
Data models for the AOP Target Breakdown Agent system.
These models define the structure of data used throughout the system.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class AOPTarget(BaseModel):
    """Annual Operating Plan (AOP) Target model"""
    vilt_target: int = Field(..., description="Target number of Virtual Instructor-Led Training (VILT) sessions")
    ilt_target: int = Field(..., description="Target number of Instructor-Led Training (ILT) sessions")
    learning_hours_target: int = Field(..., description="Target total learning hours")
    competency_targets: Dict[str, int] = Field(..., description="Targets for different competency areas")

class LearningActivity(BaseModel):
    """Model for a specific learning activity (VILT or ILT)"""
    id: str = Field(..., description="Unique identifier for the learning activity")
    title: str = Field(..., description="Title of the learning activity")
    type: str = Field(..., description="Type of learning activity (VILT or ILT)")
    duration_hours: float = Field(..., description="Duration in hours")
    competency_area: str = Field(..., description="Primary competency area addressed")
    scheduled_date: datetime = Field(..., description="Scheduled date and time")
    capacity: int = Field(..., description="Maximum number of participants")
    registrations: int = Field(0, description="Current number of registrations")
    completion_count: int = Field(0, description="Number of participants who completed the activity")

class LearningPlan(BaseModel):
    """Learning Plan model containing scheduled learning activities"""
    gld_id: str = Field(..., description="Group Learning Director (GLD) identifier")
    gld_name: str = Field(..., description="GLD name")
    department: str = Field(..., description="Department or business unit")
    activities: List[LearningActivity] = Field([], description="List of scheduled learning activities")
    
    @property
    def total_vilt_count(self) -> int:
        """Total number of VILT sessions in the plan"""
        return sum(1 for activity in self.activities if activity.type == "VILT")
    
    @property
    def total_ilt_count(self) -> int:
        """Total number of ILT sessions in the plan"""
        return sum(1 for activity in self.activities if activity.type == "ILT")
    
    @property
    def total_learning_hours(self) -> float:
        """Total learning hours in the plan"""
        return sum(activity.duration_hours * activity.completion_count for activity in self.activities)
    
    @property
    def competency_hours(self) -> Dict[str, float]:
        """Learning hours by competency area"""
        result = {}
        for activity in self.activities:
            area = activity.competency_area
            hours = activity.duration_hours * activity.completion_count
            if area in result:
                result[area] += hours
            else:
                result[area] = hours
        return result

class TimeframeTasks(BaseModel):
    """Tasks broken down by timeframe"""
    timeframe_name: str = Field(..., description="Name of the timeframe (e.g., 'Q1', 'January', 'Week 1')")
    vilt_target: float = Field(..., description="VILT target for this timeframe")
    ilt_target: float = Field(..., description="ILT target for this timeframe")
    learning_hours_target: float = Field(..., description="Learning hours target for this timeframe")
    competency_targets: Dict[str, float] = Field(..., description="Competency targets for this timeframe")
    tasks: List[str] = Field([], description="List of specific tasks for this timeframe")

class TargetBreakdown(BaseModel):
    """Breakdown of AOP targets into different timeframes"""
    annual: AOPTarget = Field(..., description="Annual targets")
    quarterly: List[TimeframeTasks] = Field([], description="Quarterly breakdown")
    monthly: List[TimeframeTasks] = Field([], description="Monthly breakdown")
    weekly: List[TimeframeTasks] = Field([], description="Weekly breakdown")
    daily: List[Dict[str, Any]] = Field([], description="Daily to-do lists")

class GapAnalysis(BaseModel):
    """Gap analysis between targets and current plan"""
    vilt_scheduled: int = Field(..., description="Number of VILT sessions scheduled")
    vilt_gap: int = Field(..., description="Gap in VILT sessions (target - scheduled)")
    vilt_gap_indicator: int = Field(..., description="Gap indicator (0 = No Gap)")
    ilt_scheduled: int = Field(..., description="Number of ILT sessions scheduled")
    ilt_gap: int = Field(..., description="Gap in ILT sessions (target - scheduled)")
    ilt_gap_indicator: int = Field(..., description="Gap indicator (0 = No Gap)")
    learning_hours_scheduled: float = Field(..., description="Learning hours scheduled")
    learning_hours_gap: float = Field(..., description="Gap in learning hours")
    learning_hours_gap_indicator: float = Field(..., description="Gap indicator for learning hours")
    competency_gaps: Dict[str, Dict[str, float]] = Field(..., description="Gaps by competency area")

class RiskFactor(BaseModel):
    """Risk factor identified in the learning plan"""
    risk_area: str = Field(..., description="Area where risk is identified")
    current_value: str = Field(..., description="Current value or metric")
    target_value: str = Field(..., description="Target value or metric")
    risk_level: str = Field(..., description="Risk level (Low, Medium, High)")
    impact: str = Field(..., description="Potential impact if risk materializes")
    mitigation: str = Field(..., description="Suggested mitigation actions")

class RiskAssessment(BaseModel):
    """Assessment of risks in meeting AOP targets"""
    gld_id: str = Field(..., description="GLD identifier")
    assessment_date: datetime = Field(..., description="Date of assessment")
    risk_factors: List[RiskFactor] = Field([], description="Identified risk factors")
    overall_risk_level: str = Field(..., description="Overall risk level for meeting AOP targets")

class Opportunity(BaseModel):
    """Opportunity identified based on learning data trends"""
    opportunity: str = Field(..., description="Description of the opportunity")
    impact: str = Field(..., description="Expected impact if implemented")
    resources_needed: str = Field(..., description="Resources needed to implement")
    timeframe: str = Field(..., description="Timeframe for implementation")
    priority: str = Field("Medium", description="Priority level (Low, Medium, High)")

class DiagnosticReport(BaseModel):
    """Diagnostic report on skills strengths, weaknesses, and future risks"""
    gld_id: str = Field(..., description="GLD identifier")
    report_date: datetime = Field(..., description="Date of report generation")
    strengths: List[str] = Field([], description="Identified strengths")
    weaknesses: List[str] = Field([], description="Identified weaknesses")
    future_risks: List[str] = Field([], description="Potential future risks")
    recommendations: List[str] = Field([], description="Recommendations for improvement")
    competency_analysis: Dict[str, Any] = Field({}, description="Detailed analysis by competency area")
