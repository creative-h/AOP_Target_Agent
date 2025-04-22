#!/usr/bin/env python3
# coding: utf-8

"""
Example script to demonstrate the AOP Target Agent system.
This script shows how to use the agent system with sample AOP targets.
"""

import json
import sys

# Add the parent directory to the Python path
sys.path.append('/media/sf_Budgie_1/agenticLab')

# Import the run_aop_target_agent function
from aop_target_agent import run_aop_target_agent

def main():
    """Run the AOP Target Agent with sample data"""
    
    print("AOP Target Breakdown Agent Example")
    print("==================================")
    
    # Define sample AOP targets
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
    
    print(f"Sample AOP Targets:")
    print(f"- VILT Target: {aop_targets['vilt_target']} sessions")
    print(f"- ILT Target: {aop_targets['ilt_target']} sessions")
    print(f"- Learning Hours Target: {aop_targets['learning_hours_target']} hours")
    print(f"- Competency Targets:")
    for competency, target in aop_targets['competency_targets'].items():
        print(f"  - {competency.capitalize()}: {target} hours")
    
    print("\nRunning AOP Target Agent...")
    
    # Run the agent with mock mode enabled
    result = run_aop_target_agent(aop_targets, mock_mode=True)
    
    print("\nAgent Analysis Complete!")
    
    # Display summary of results
    print("\nSummary of Results:")
    print("------------------")
    
    # Target Breakdown Summary
    quarterly_breakdown = result["target_breakdown"]["quarterly"]
    print(f"Quarterly Breakdown:")
    for quarter in quarterly_breakdown:
        print(f"- {quarter['timeframe_name']}: {int(quarter['vilt_target'])} VILTs, {int(quarter['ilt_target'])} ILTs")
    
    # Gap Analysis Summary
    gap_analysis = result["gap_analysis"]
    print(f"\nGap Analysis:")
    print(f"- VILT Gap: {gap_analysis['vilt_gap']} sessions (Gap Indicator: {gap_analysis['vilt_gap_indicator']})")
    print(f"- ILT Gap: {gap_analysis['ilt_gap']} sessions (Gap Indicator: {gap_analysis['ilt_gap_indicator']})")
    
    # Risk Assessment Summary
    risk_assessment = result["risk_assessment"]
    high_risks = [risk for risk in risk_assessment if risk["risk_level"] == "High"]
    print(f"\nHigh Risk Areas: {len(high_risks)}")
    for risk in high_risks:
        print(f"- {risk['risk_area']}: {risk['impact']}")
    
    # Opportunities Summary
    opportunities = result["opportunities"]
    print(f"\nTop Opportunities: {len(opportunities)}")
    for i, opportunity in enumerate(opportunities[:3], 1):
        print(f"{i}. {opportunity['opportunity']} - {opportunity['impact']}")
    
    # Diagnostic Report Summary
    diagnostic = result["diagnostic_report"]
    print(f"\nDiagnostic Report Summary:")
    print(f"- Strengths: {len(diagnostic['strengths'])}")
    print(f"- Weaknesses: {len(diagnostic['weaknesses'])}")
    print(f"- Future Risks: {len(diagnostic['future_risks'])}")
    print(f"- Recommendations: {len(diagnostic['recommendations'])}")
    
    # Option to save full results to file
    save_option = input("\nWould you like to save the full results to a JSON file? (y/n): ")
    if save_option.lower() == 'y':
        filename = "aop_target_analysis_results.json"
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Results saved to {filename}")
    
    print("\nThank you for using the AOP Target Breakdown Agent!")

if __name__ == "__main__":
    main()
