def create_hr_report_template():
    template = {
        "Candidate Information": {
            "Name": "",
            "Interview Date": "",
            "Role": ""
        },

        "HR Performance": {
            "Overall Score": "",
            "Summary": ""
        },

        "Strengths": [],

        "Weaknesses": [],

        "Cultural Fit Indicators": [],

        "Risk Flags": [],

        "Inconsistencies": [],

        "Recruiter Summary": ""
    }

    return template


if __name__ == "__main__":

    report = create_hr_report_template()

    print("===== STRUCTURED HR REPORT TEMPLATE =====")

    for section, value in report.items():
        print("\n" + section + ":")

        if isinstance(value, dict):
            for field in value:
                print(f"  {field}:")
        elif isinstance(value, list):
            print("  []")
        else:
            print(" ", value)