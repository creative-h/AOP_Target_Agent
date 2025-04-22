#!/usr/bin/env python3
# coding: utf-8

"""
Streamlit app for the AOP Target Breakdown Agent system.
This app provides a user-friendly interface for interacting with the agent system.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import sys
import os
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define functions to generate mock data directly in the app
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
            {"month": "March", "vilt_target": aop_targets["vilt_target"] * 0.06, "ilt_target": aop_targets["ilt_target"] * 0.06},
            {"month": "April", "vilt_target": aop_targets["vilt_target"] * 0.08, "ilt_target": aop_targets["ilt_target"] * 0.08},
            {"month": "May", "vilt_target": aop_targets["vilt_target"] * 0.09, "ilt_target": aop_targets["ilt_target"] * 0.09},
            {"month": "June", "vilt_target": aop_targets["vilt_target"] * 0.13, "ilt_target": aop_targets["ilt_target"] * 0.13},
            {"month": "July", "vilt_target": aop_targets["vilt_target"] * 0.09, "ilt_target": aop_targets["ilt_target"] * 0.09},
            {"month": "August", "vilt_target": aop_targets["vilt_target"] * 0.08, "ilt_target": aop_targets["ilt_target"] * 0.08},
            {"month": "September", "vilt_target": aop_targets["vilt_target"] * 0.09, "ilt_target": aop_targets["ilt_target"] * 0.09},
            {"month": "October", "vilt_target": aop_targets["vilt_target"] * 0.08, "ilt_target": aop_targets["ilt_target"] * 0.08},
            {"month": "November", "vilt_target": aop_targets["vilt_target"] * 0.08, "ilt_target": aop_targets["ilt_target"] * 0.08},
            {"month": "December", "vilt_target": aop_targets["vilt_target"] * 0.08, "ilt_target": aop_targets["ilt_target"] * 0.08}
        ],
        "weekly": [
            {"week": "Week 1", "vilt_target": aop_targets["vilt_target"] * 0.02, "ilt_target": aop_targets["ilt_target"] * 0.02, "tasks": ["Confirm trainers for Week 1 sessions", "Send reminders to registered participants", "Prepare training materials and environments", "Review feedback from previous week's sessions"]},
            {"week": "Week 2", "vilt_target": aop_targets["vilt_target"] * 0.02, "ilt_target": aop_targets["ilt_target"] * 0.02, "tasks": ["Confirm trainers for Week 2 sessions", "Send reminders to registered participants", "Prepare training materials and environments", "Review feedback from previous week's sessions"]},
            {"week": "Week 3", "vilt_target": aop_targets["vilt_target"] * 0.02, "ilt_target": aop_targets["ilt_target"] * 0.02, "tasks": ["Confirm trainers for Week 3 sessions", "Send reminders to registered participants", "Prepare training materials and environments", "Review feedback from previous week's sessions"]},
            {"week": "Week 4", "vilt_target": aop_targets["vilt_target"] * 0.02, "ilt_target": aop_targets["ilt_target"] * 0.02, "tasks": ["Confirm trainers for Week 4 sessions", "Send reminders to registered participants", "Prepare training materials and environments", "Review feedback from previous week's sessions"]}
        ],
        "daily": [
            {"day": "Monday", "tasks": ["Review Monday's scheduled sessions", "Check registration numbers for upcoming sessions", "Follow up on participant feedback", "Update tracking dashboards", "Coordinate with trainers and support staff"]},
            {"day": "Tuesday", "tasks": ["Review Tuesday's scheduled sessions", "Check registration numbers for upcoming sessions", "Follow up on participant feedback", "Update tracking dashboards", "Coordinate with trainers and support staff"]},
            {"day": "Wednesday", "tasks": ["Review Wednesday's scheduled sessions", "Check registration numbers for upcoming sessions", "Follow up on participant feedback", "Update tracking dashboards", "Coordinate with trainers and support staff"]},
            {"day": "Thursday", "tasks": ["Review Thursday's scheduled sessions", "Check registration numbers for upcoming sessions", "Follow up on participant feedback", "Update tracking dashboards", "Coordinate with trainers and support staff"]},
            {"day": "Friday", "tasks": ["Review Friday's scheduled sessions", "Check registration numbers for upcoming sessions", "Follow up on participant feedback", "Update tracking dashboards", "Coordinate with trainers and support staff"]}
        ]
    }
    
    # Mock gap analysis
    gap_analysis = {
        "vilt_scheduled": aop_targets["vilt_target"] * 0.8,
        "vilt_gap": aop_targets["vilt_target"] * 0.2,
        "vilt_gap_indicator": 0 if aop_targets["vilt_target"] * 0.8 >= aop_targets["vilt_target"] else aop_targets["vilt_target"] * 0.2,
        "ilt_scheduled": aop_targets["ilt_target"] * 0.7,
        "ilt_gap": aop_targets["ilt_target"] * 0.3,
        "ilt_gap_indicator": 0 if aop_targets["ilt_target"] * 0.7 >= aop_targets["ilt_target"] else aop_targets["ilt_target"] * 0.3,
        "competency_gaps": {
            "technical": {
                "scheduled": aop_targets["competency_targets"].get("technical", 0) * 0.75,
                "gap": aop_targets["competency_targets"].get("technical", 0) * 0.25,
                "gap_indicator": 0 if aop_targets["competency_targets"].get("technical", 0) * 0.75 >= aop_targets["competency_targets"].get("technical", 0) else aop_targets["competency_targets"].get("technical", 0) * 0.25
            },
            "soft_skills": {
                "scheduled": aop_targets["competency_targets"].get("soft_skills", 0) * 0.85,
                "gap": aop_targets["competency_targets"].get("soft_skills", 0) * 0.15,
                "gap_indicator": 0 if aop_targets["competency_targets"].get("soft_skills", 0) * 0.85 >= aop_targets["competency_targets"].get("soft_skills", 0) else aop_targets["competency_targets"].get("soft_skills", 0) * 0.15
            },
            "leadership": {
                "scheduled": aop_targets["competency_targets"].get("leadership", 0) * 0.65,
                "gap": aop_targets["competency_targets"].get("leadership", 0) * 0.35,
                "gap_indicator": 0 if aop_targets["competency_targets"].get("leadership", 0) * 0.65 >= aop_targets["competency_targets"].get("leadership", 0) else aop_targets["competency_targets"].get("leadership", 0) * 0.35
            }
        }
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
        },
        {
            "risk_area": "Leadership Competency Development",
            "current_value": "65%",
            "target_value": "90%",
            "risk_level": "High",
            "impact": "Significant gap in leadership skills development",
            "mitigation": "Schedule additional leadership workshops and coaching sessions"
        }
    ]
    
    # Mock opportunities
    opportunities = [
        {
            "opportunity": "Schedule 3 additional Python Bootcamps",
            "impact": "Will meet Technical Learning Hours target and increase competency goal by 15%",
            "resources_needed": "2 trainers, virtual lab environment",
            "timeframe": "Next 2 months"
        },
        {
            "opportunity": "Convert 2 ILT sessions to VILT format",
            "impact": "Increase participation by 25% and reduce delivery costs",
            "resources_needed": "Updated materials, virtual platform setup",
            "timeframe": "Next month"
        },
        {
            "opportunity": "Implement leadership microlearning series",
            "impact": "Close leadership competency gap by 20%",
            "resources_needed": "Content development, platform integration",
            "timeframe": "Next 3 months"
        }
    ]
    
    # Mock diagnostic report
    diagnostic_report = {
        "report_date": datetime.now().strftime("%Y-%m-%d"),
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
        ],
        "summary": "The learning plan is currently at risk for meeting AOP targets. Immediate action is required in the identified risk areas, particularly in leadership competency development."
    }
    
    # Combine all results
    return {
        "target_breakdown": target_breakdown,
        "gap_analysis": gap_analysis,
        "risk_assessment": risk_assessment,
        "opportunities": opportunities,
        "diagnostic_report": diagnostic_report
    }

# Define a wrapper for run_aop_target_agent to avoid import issues
def run_aop_target_agent(aop_targets, mock_mode=True):
    """Wrapper function to run the AOP Target Agent"""
    # In a real implementation, this would call the actual agent
    # For now, we'll just use the mock results for demonstration
    return generate_mock_results(aop_targets)

# Set page configuration
st.set_page_config(
    page_title="AOP Target Breakdown Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #0D47A1;
    }
    .card {
        border-radius: 5px;
        padding: 20px;
        background-color: #f9f9f9;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .metric-card {
        text-align: center;
        padding: 15px;
        border-radius: 5px;
        background-color: #e3f2fd;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1565C0;
    }
    .metric-label {
        font-size: 1rem;
        color: #424242;
    }
    .risk-high {
        color: #D32F2F;
        font-weight: bold;
    }
    .risk-medium {
        color: #F57C00;
        font-weight: bold;
    }
    .risk-low {
        color: #388E3C;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main function to run the Streamlit app"""
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/business-report.png", width=100)
        st.markdown("## AOP Target Agent")
        st.markdown("This tool helps Global Learning Delivery (GLDs) break down Annual Operating Plan (AOP) targets into actionable timeframes.")
        
        # Input form
        st.markdown("### Input AOP Targets")
        
        vilt_target = st.number_input("VILT Target (sessions)", min_value=0, value=500, step=10)
        ilt_target = st.number_input("ILT Target (sessions)", min_value=0, value=200, step=10)
        learning_hours_target = st.number_input("Learning Hours Target", min_value=0, value=10000, step=500)
        
        st.markdown("### Competency Targets (hours)")
        technical_target = st.number_input("Technical", min_value=0, value=6000, step=500)
        soft_skills_target = st.number_input("Soft Skills", min_value=0, value=2000, step=500)
        leadership_target = st.number_input("Leadership", min_value=0, value=2000, step=500)
        
        # Use mock mode for demonstration
        mock_mode = st.checkbox("Use Mock Mode", value=True, help="Use mock data for demonstration purposes")
        
        # Run button
        run_button = st.button("Run Analysis")
    
    # Main content
    st.markdown('<h1 class="main-header">AOP Target Breakdown Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p>Breaking down Annual Operating Plan targets into actionable timeframes for Global Learning Delivery</p>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'results' not in st.session_state:
        st.session_state.results = None
    
    # Process when Run button is clicked
    if run_button:
        with st.spinner("Running AOP Target Analysis..."):
            # Prepare AOP targets
            aop_targets = {
                "vilt_target": vilt_target,
                "ilt_target": ilt_target,
                "learning_hours_target": learning_hours_target,
                "competency_targets": {
                    "technical": technical_target,
                    "soft_skills": soft_skills_target,
                    "leadership": leadership_target
                }
            }
            
            # Run the agent or generate mock results
            if mock_mode:
                results = generate_mock_results(aop_targets)
                st.success("Mock analysis completed!")
            else:
                try:
                    results = run_aop_target_agent(aop_targets, mock_mode=True)
                    st.success("Analysis completed successfully!")
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
                    results = None
            
            # Store results in session state
            st.session_state.results = results
    
    # Display results if available
    if st.session_state.results:
        results = st.session_state.results
        
        # Create tabs for different sections
        tabs = st.tabs(["Target Breakdown", "Gap Analysis", "Risk Assessment", "Opportunities", "Diagnostic Report"])
        
        # Tab 1: Target Breakdown
        with tabs[0]:
            st.markdown('<h2 class="sub-header">Target Breakdown</h2>', unsafe_allow_html=True)
            
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<div class="metric-card">'
                            f'<div class="metric-value">{results["target_breakdown"]["annual"]["vilt_target"]}</div>'
                            '<div class="metric-label">Annual VILT Target</div>'
                            '</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="metric-card">'
                            f'<div class="metric-value">{results["target_breakdown"]["annual"]["ilt_target"]}</div>'
                            '<div class="metric-label">Annual ILT Target</div>'
                            '</div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="metric-card">'
                            f'<div class="metric-value">{results["target_breakdown"]["annual"]["learning_hours_target"]}</div>'
                            '<div class="metric-label">Learning Hours Target</div>'
                            '</div>', unsafe_allow_html=True)
            
            # Quarterly breakdown
            st.markdown("### Quarterly Breakdown")
            
            # Convert quarterly data to DataFrame
            quarterly_data = []
            for q in results["target_breakdown"]["quarterly"]:
                if isinstance(q, dict) and "quarter" in q:
                    quarterly_data.append({
                        "Quarter": q["quarter"],
                        "VILT Target": int(q["vilt_target"]),
                        "ILT Target": int(q["ilt_target"])
                    })
                elif isinstance(q, dict) and "timeframe_name" in q:
                    quarterly_data.append({
                        "Quarter": q["timeframe_name"],
                        "VILT Target": int(q["vilt_target"]),
                        "ILT Target": int(q["ilt_target"])
                    })
            
            if quarterly_data:
                df_quarterly = pd.DataFrame(quarterly_data)
                
                # Create a bar chart for quarterly breakdown
                fig = px.bar(df_quarterly, x="Quarter", y=["VILT Target", "ILT Target"], 
                            barmode="group", title="Quarterly Training Targets",
                            color_discrete_sequence=["#1E88E5", "#FFC107"])
                
                fig.update_layout(
                    xaxis_title="Quarter",
                    yaxis_title="Number of Sessions",
                    legend_title="Target Type",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Display quarterly data as a table
                st.dataframe(df_quarterly, use_container_width=True)
            
            # Monthly breakdown
            st.markdown("### Monthly Breakdown")
            
            # Convert monthly data to DataFrame
            monthly_data = []
            for m in results["target_breakdown"]["monthly"]:
                if isinstance(m, dict) and "month" in m:
                    monthly_data.append({
                        "Month": m["month"],
                        "VILT Target": int(m["vilt_target"]),
                        "ILT Target": int(m["ilt_target"])
                    })
                elif isinstance(m, dict) and "timeframe_name" in m:
                    monthly_data.append({
                        "Month": m["timeframe_name"],
                        "VILT Target": int(m["vilt_target"]),
                        "ILT Target": int(m["ilt_target"])
                    })
            
            if monthly_data:
                df_monthly = pd.DataFrame(monthly_data)
                
                # Create a line chart for monthly breakdown
                fig = px.line(df_monthly, x="Month", y=["VILT Target", "ILT Target"], 
                            title="Monthly Training Targets",
                            markers=True, color_discrete_sequence=["#1E88E5", "#FFC107"])
                
                fig.update_layout(
                    xaxis_title="Month",
                    yaxis_title="Number of Sessions",
                    legend_title="Target Type",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Weekly and daily tasks
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Weekly Tasks")
                for week in results["target_breakdown"]["weekly"]:
                    if "tasks" in week:
                        st.markdown(f"**{week.get('timeframe_name', week.get('week', 'Week'))}**")
                        for task in week["tasks"]:
                            st.markdown(f"- {task}")
            
            with col2:
                st.markdown("### Daily Tasks")
                for day in results["target_breakdown"]["daily"]:
                    if "tasks" in day:
                        st.markdown(f"**{day.get('day', 'Day')}**")
                        for task in day["tasks"]:
                            st.markdown(f"- {task}")
        
        # Tab 2: Gap Analysis
        with tabs[1]:
            st.markdown('<h2 class="sub-header">Gap Analysis</h2>', unsafe_allow_html=True)
            
            gap_analysis = results["gap_analysis"]
            
            # Create metrics for gap analysis
            col1, col2 = st.columns(2)
            
            with col1:
                # VILT Gap
                vilt_scheduled = gap_analysis.get("vilt_scheduled", 0)
                vilt_target = results["target_breakdown"]["annual"]["vilt_target"]
                vilt_gap = gap_analysis.get("vilt_gap", 0)
                vilt_gap_indicator = gap_analysis.get("vilt_gap_indicator", 0)
                
                # Create a gauge chart for VILT progress
                vilt_percent = min(100, int((vilt_scheduled / vilt_target) * 100)) if vilt_target > 0 else 0
                
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=vilt_percent,
                    title={"text": "VILT Progress"},
                    gauge={
                        "axis": {"range": [0, 100], "tickwidth": 1},
                        "bar": {"color": "#1E88E5"},
                        "steps": [
                            {"range": [0, 50], "color": "#FFCDD2"},
                            {"range": [50, 80], "color": "#FFECB3"},
                            {"range": [80, 100], "color": "#C8E6C9"}
                        ],
                        "threshold": {
                            "line": {"color": "red", "width": 4},
                            "thickness": 0.75,
                            "value": 100
                        }
                    }
                ))
                
                fig.update_layout(height=250)
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown('<div class="card">'
                            f'<p><strong>VILT Target:</strong> {vilt_target}</p>'
                            f'<p><strong>Scheduled:</strong> {vilt_scheduled}</p>'
                            f'<p><strong>Gap:</strong> {vilt_gap}</p>'
                            f'<p><strong>Gap Indicator:</strong> {vilt_gap_indicator} (0 = No Gap)</p>'
                            '</div>', unsafe_allow_html=True)
            
            with col2:
                # ILT Gap
                ilt_scheduled = gap_analysis.get("ilt_scheduled", 0)
                ilt_target = results["target_breakdown"]["annual"]["ilt_target"]
                ilt_gap = gap_analysis.get("ilt_gap", 0)
                ilt_gap_indicator = gap_analysis.get("ilt_gap_indicator", 0)
                
                # Create a gauge chart for ILT progress
                ilt_percent = min(100, int((ilt_scheduled / ilt_target) * 100)) if ilt_target > 0 else 0
                
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=ilt_percent,
                    title={"text": "ILT Progress"},
                    gauge={
                        "axis": {"range": [0, 100], "tickwidth": 1},
                        "bar": {"color": "#FFC107"},
                        "steps": [
                            {"range": [0, 50], "color": "#FFCDD2"},
                            {"range": [50, 80], "color": "#FFECB3"},
                            {"range": [80, 100], "color": "#C8E6C9"}
                        ],
                        "threshold": {
                            "line": {"color": "red", "width": 4},
                            "thickness": 0.75,
                            "value": 100
                        }
                    }
                ))
                
                fig.update_layout(height=250)
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown('<div class="card">'
                            f'<p><strong>ILT Target:</strong> {ilt_target}</p>'
                            f'<p><strong>Scheduled:</strong> {ilt_scheduled}</p>'
                            f'<p><strong>Gap:</strong> {ilt_gap}</p>'
                            f'<p><strong>Gap Indicator:</strong> {ilt_gap_indicator} (0 = No Gap)</p>'
                            '</div>', unsafe_allow_html=True)
            
            # Competency gaps
            st.markdown("### Competency Gaps")
            
            competency_gaps = gap_analysis.get("competency_gaps", {})
            if competency_gaps:
                # Create a DataFrame for competency gaps
                competency_data = []
                for competency, gap_data in competency_gaps.items():
                    competency_data.append({
                        "Competency": competency.capitalize(),
                        "Target": results["target_breakdown"]["annual"]["competency_targets"].get(competency, 0),
                        "Scheduled": gap_data.get("scheduled", 0),
                        "Gap": gap_data.get("gap", 0),
                        "Gap Indicator": gap_data.get("gap_indicator", 0)
                    })
                
                df_competency = pd.DataFrame(competency_data)
                
                # Create a bar chart for competency gaps
                fig = px.bar(df_competency, x="Competency", y=["Target", "Scheduled"], 
                            barmode="group", title="Competency Targets vs. Scheduled",
                            color_discrete_sequence=["#1E88E5", "#4CAF50"])
                
                fig.update_layout(
                    xaxis_title="Competency",
                    yaxis_title="Hours",
                    legend_title="Type",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Display competency data as a table
                st.dataframe(df_competency, use_container_width=True)
        
        # Tab 3: Risk Assessment
        with tabs[2]:
            st.markdown('<h2 class="sub-header">Risk Assessment</h2>', unsafe_allow_html=True)
            
            risk_assessment = results["risk_assessment"]
            
            # Group risks by level
            high_risks = [risk for risk in risk_assessment if risk.get("risk_level") == "High"]
            medium_risks = [risk for risk in risk_assessment if risk.get("risk_level") == "Medium"]
            low_risks = [risk for risk in risk_assessment if risk.get("risk_level") == "Low"]
            
            # Create a pie chart for risk distribution
            risk_counts = [len(high_risks), len(medium_risks), len(low_risks)]
            risk_labels = ["High", "Medium", "Low"]
            
            fig = px.pie(
                values=risk_counts,
                names=risk_labels,
                title="Risk Distribution",
                color_discrete_sequence=["#D32F2F", "#F57C00", "#388E3C"]
            )
            
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
            
            # Display risks by level
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<h3 class="risk-high">High Risks</h3>', unsafe_allow_html=True)
                if high_risks:
                    for risk in high_risks:
                        st.markdown('<div class="card">'
                                    f'<p><strong>Area:</strong> {risk.get("risk_area", "")}</p>'
                                    f'<p><strong>Current:</strong> {risk.get("current_value", "")}</p>'
                                    f'<p><strong>Target:</strong> {risk.get("target_value", "")}</p>'
                                    f'<p><strong>Impact:</strong> {risk.get("impact", "")}</p>'
                                    f'<p><strong>Mitigation:</strong> {risk.get("mitigation", "")}</p>'
                                    '</div>', unsafe_allow_html=True)
                else:
                    st.info("No high risks identified")
            
            with col2:
                st.markdown('<h3 class="risk-medium">Medium Risks</h3>', unsafe_allow_html=True)
                if medium_risks:
                    for risk in medium_risks:
                        st.markdown('<div class="card">'
                                    f'<p><strong>Area:</strong> {risk.get("risk_area", "")}</p>'
                                    f'<p><strong>Current:</strong> {risk.get("current_value", "")}</p>'
                                    f'<p><strong>Target:</strong> {risk.get("target_value", "")}</p>'
                                    f'<p><strong>Impact:</strong> {risk.get("impact", "")}</p>'
                                    f'<p><strong>Mitigation:</strong> {risk.get("mitigation", "")}</p>'
                                    '</div>', unsafe_allow_html=True)
                else:
                    st.info("No medium risks identified")
            
            with col3:
                st.markdown('<h3 class="risk-low">Low Risks</h3>', unsafe_allow_html=True)
                if low_risks:
                    for risk in low_risks:
                        st.markdown('<div class="card">'
                                    f'<p><strong>Area:</strong> {risk.get("risk_area", "")}</p>'
                                    f'<p><strong>Current:</strong> {risk.get("current_value", "")}</p>'
                                    f'<p><strong>Target:</strong> {risk.get("target_value", "")}</p>'
                                    f'<p><strong>Impact:</strong> {risk.get("impact", "")}</p>'
                                    f'<p><strong>Mitigation:</strong> {risk.get("mitigation", "")}</p>'
                                    '</div>', unsafe_allow_html=True)
                else:
                    st.info("No low risks identified")
        
        # Tab 4: Opportunities
        with tabs[3]:
            st.markdown('<h2 class="sub-header">Opportunities</h2>', unsafe_allow_html=True)
            
            opportunities = results["opportunities"]
            
            if opportunities:
                for i, opportunity in enumerate(opportunities):
                    st.markdown('<div class="card">'
                                f'<h3>{i+1}. {opportunity.get("opportunity", "")}</h3>'
                                f'<p><strong>Impact:</strong> {opportunity.get("impact", "")}</p>'
                                f'<p><strong>Resources Needed:</strong> {opportunity.get("resources_needed", "")}</p>'
                                f'<p><strong>Timeframe:</strong> {opportunity.get("timeframe", "")}</p>'
                                '</div>', unsafe_allow_html=True)
            else:
                st.info("No opportunities identified")
        
        # Tab 5: Diagnostic Report
        with tabs[4]:
            st.markdown('<h2 class="sub-header">Diagnostic Report</h2>', unsafe_allow_html=True)
            
            diagnostic_report = results["diagnostic_report"]
            
            # Summary
            if "summary" in diagnostic_report:
                st.markdown(f"### Summary")
                st.markdown(f"{diagnostic_report['summary']}")
            
            # Create columns for strengths and weaknesses
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Strengths")
                for strength in diagnostic_report.get("strengths", []):
                    st.markdown(f"- {strength}")
            
            with col2:
                st.markdown("### Weaknesses")
                for weakness in diagnostic_report.get("weaknesses", []):
                    st.markdown(f"- {weakness}")
            
            # Future risks and recommendations
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Future Risks")
                for risk in diagnostic_report.get("future_risks", []):
                    st.markdown(f"- {risk}")
            
            with col2:
                st.markdown("### Recommendations")
                for recommendation in diagnostic_report.get("recommendations", []):
                    st.markdown(f"- {recommendation}")
            
            # Export options
            st.markdown("### Export Report")
            
            export_format = st.selectbox("Select export format", ["JSON", "CSV"])
            
            if st.button("Export Report"):
                if export_format == "JSON":
                    # Convert to JSON
                    json_data = json.dumps(results, indent=2)
                    st.download_button(
                        label="Download JSON",
                        data=json_data,
                        file_name=f"aop_target_report_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )
                else:
                    # Create a simple CSV for diagnostic report
                    csv_data = "Category,Item\n"
                    
                    for strength in diagnostic_report.get("strengths", []):
                        csv_data += f"Strength,\"{strength}\"\n"
                    
                    for weakness in diagnostic_report.get("weaknesses", []):
                        csv_data += f"Weakness,\"{weakness}\"\n"
                    
                    for risk in diagnostic_report.get("future_risks", []):
                        csv_data += f"Future Risk,\"{risk}\"\n"
                    
                    for recommendation in diagnostic_report.get("recommendations", []):
                        csv_data += f"Recommendation,\"{recommendation}\"\n"
                    
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name=f"aop_target_report_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
    else:
        # Display instructions if no results yet
        st.info("Enter your AOP targets in the sidebar and click 'Run Analysis' to get started.")
        
        # Sample screenshot or placeholder
        st.image("https://img.icons8.com/color/452/business-report.png", width=300)
        
        st.markdown("""
        ### What this tool does:
        
        1. **Target Breakdown**: Converts annual targets into quarterly, monthly, weekly, and daily tasks
        2. **Gap Analysis**: Shows where you stand against your targets with '0 = No Gap' indicators
        3. **Risk Assessment**: Identifies potential issues in meeting targets
        4. **Opportunity Identification**: Suggests specific actions to help meet goals
        5. **Diagnostic Reports**: Provides insights on strengths, weaknesses, and future risks for Global Learning Delivery
        
        Enter your AOP targets in the sidebar to get started!
        """)

if __name__ == "__main__":
    main()
