# AOP Target Breakdown Agent

An intelligent agent system that breaks down Annual Operating Plan (AOP) Targets into actionable timeframes for Global Learning Delivery (GLDs).

## Overview

This agent system helps Global Learning Delivery (GLDs) manage their learning delivery targets by:

1. Breaking down AOP targets into quarterly, monthly, weekly, and daily to-do lists
2. Tracking VILTs and ILTs in learning plans and showing gap indicators (0 = No Gap)
3. Identifying risk factors when schedules and registrations don't match targets
4. Suggesting opportunities based on learning data trends
5. Generating diagnostic reports on skills strengths, weaknesses, and future risks

## Features

- **Target Breakdown**: Converts annual targets into actionable timeframes
- **Gap Analysis**: Uses '0' = No Gap indicator to show if GLDs are on track
- **Risk Assessment**: Identifies potential issues in meeting targets
- **Opportunity Identification**: Suggests specific actions to meet goals (e.g., "If you schedule 3 XYZ Bootcamp, you can meet your goal of ABC LH & DEF Competency")
- **Diagnostic Reports**: Provides insights for Leaders and TD on skills development

## Data Sources

The system integrates data from multiple sources:
- **iEvolve**: Learning management system data
- **iGlance**: Learning metrics and dashboards
- **AFTD**: Advanced Framework for Talent Development
- **Internal Internship**: Data from internal internship programs

## Architecture

The system is built using the crewAI framework and consists of:

1. **Agents**:
   - AOP Target Breakdown Specialist
   - Learning Plan Analyst
   - Risk Assessment Specialist
   - Learning Opportunity Advisor
   - Learning Diagnostics Expert

2. **Tools**:
   - `breakdown_targets`: Breaks down annual targets into timeframes
   - `analyze_learning_plan`: Analyzes learning plans for VILTs and ILTs
   - `calculate_gap`: Calculates gaps between targets and current plan
   - `assess_risk`: Identifies risk factors in learning plan execution
   - `identify_opportunities`: Finds opportunities based on data trends
   - `generate_diagnostic_report`: Creates comprehensive diagnostic reports

## Usage

```python
from aop_target_agent import run_aop_target_agent

# Define your AOP targets
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

# Run the agent
result = run_aop_target_agent(aop_targets)

# Access the results
target_breakdown = result["target_breakdown"]
gap_analysis = result["gap_analysis"]
risk_assessment = result["risk_assessment"]
opportunities = result["opportunities"]
diagnostic_report = result["diagnostic_report"]
```

## Requirements

- Python 3.8+
- crewAI
- pydantic
- PyYAML

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

The system uses YAML configuration files in the `config` directory:
- `agents.yaml`: Defines the roles, goals, and backstories for each agent
- `tasks.yaml`: Defines the tasks for each agent to perform

## Example Output

The system provides structured output including:

- **Target Breakdown**: Detailed breakdown of targets by timeframe
- **Gap Analysis**: Analysis of gaps between targets and current plan
- **Risk Assessment**: Identified risk factors with severity and mitigation suggestions
- **Opportunities**: Specific opportunities to meet or exceed targets
- **Diagnostic Report**: Comprehensive report on strengths, weaknesses, and future risks






# cd /home/lubuntu && source myenv/bin/activate && cd /media/sf_Budgie_1/agenticLab/aop_target_agent && streamlit run app.py