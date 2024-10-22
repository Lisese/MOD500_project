import subprocess

def run_script(script_name):
    print(f"Running {script_name}...")
    try:
        subprocess.run(['python3', script_name], check=True)
    except subprocess.CalledProcessError:
        print(f"Error running {script_name}. Continuing with the rest of the analysis.")

if __name__ == "__main__":
    # Run existing analysis scripts
    run_script('fetch_tourism_data.py')
    run_script('fetch_weather_data.py')
    
    # Temporarily comment out the social media analysis
    # run_script('analyze_social_media.py')
    
    run_script('financial_analysis.py')

    # Generate decision tree and influence diagram
    run_script('generate_diagrams.py')

    # Convert the decision analysis report to PDF
    run_script('convert_to_pdf.py')

    print("\nAnalysis complete. Please check the generated files and PDF report.")
    print("Next steps:")
    print("1. Review the PDF report for a comprehensive overview of all analyses")
    print("2. Examine the decision tree and influence diagram for visual representation of the decision process")
    print("3. Use the insights from all analyses to make informed decisions about the campervan rental business")
    print("Note: Social media analysis was skipped due to API issues. Consider updating this component separately.")
