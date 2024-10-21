import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import sys
import traceback

def run_script(script_name):
    print("Running {}...".format(script_name))
    try:
        result = subprocess.run(['/usr/local/bin/python3', script_name], capture_output=True, text=True, check=True)
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error running {}:".format(script_name))
        print(e.stderr)
        return "Error running {}: {}".format(script_name, e.stderr)

def create_pdf_report(data):
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Campervan Rental Business Analysis Report", ln=True, align="C")
        pdf.ln(10)

        # Content
        pdf.set_font("Arial", "", 12)
        for section, content in data.items():
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, section, ln=True)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 5, content)
            pdf.ln(5)

        # Add images
        images = ['tourism_data_plot.png', 'temperature_plot.png', 'precipitation_plot.png', 
                  'sentiment_analysis_plot.png', 'cumulative_cash_flows.png', 'npv_sensitivity.png']
        for img in images:
            if os.path.exists(img):
                pdf.add_page()
                pdf.image(img, x=10, y=10, w=190)
            else:
                pdf.add_page()
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, "Image {} not found".format(img), ln=True)

        pdf.output("campervan_rental_analysis_report.pdf")
        print("PDF report generated successfully.")
    except Exception as e:
        print("Error creating PDF report: {}".format(str(e)))
        traceback.print_exc()

if __name__ == "__main__":
    # Run all analysis scripts
    tourism_data = run_script('fetch_tourism_data.py')
    weather_data = run_script('fetch_weather_data.py')
    social_media_data = run_script('analyze_social_media.py')
    financial_data = run_script('financial_analysis.py')

    # Compile results
    report_data = {
        "Tourism Data Analysis": tourism_data,
        "Weather Data Analysis": weather_data,
        "Social Media Sentiment Analysis": social_media_data,
        "Financial Analysis": financial_data
    }

    # Create PDF report
    create_pdf_report(report_data)

    if os.path.exists("campervan_rental_analysis_report.pdf"):
        print("\nAnalysis complete. PDF report generated: campervan_rental_analysis_report.pdf")
        print("\nNext steps:")
        print("1. Review the PDF report for a comprehensive overview of all analyses")
        print("2. Use the insights from the tourism data to inform your Business Launch Decision and Pricing Strategy")
        print("3. Consider the weather data when deciding on your Operational Model and Campervan Types")
        print("4. Leverage the social media sentiment analysis for your Marketing Focus and Additional Services decisions")
        print("5. Utilize the financial analysis to guide your Fleet Size decision and overall business strategy")
        print("6. Conduct further analyses or gather more data in areas where you need additional clarity")
        print("7. Make your final decisions based on the comprehensive data and analyses provided")
    else:
        print("\nError: PDF report was not generated. Please check the error messages above.")
