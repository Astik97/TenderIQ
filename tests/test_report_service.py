from backend.services.compare_service import compare_tenders
from backend.services.report_service import generate_report

text1 = """
Eligibility Criteria

Company should have 5 years experience.

Technical Specification

ISO Certified.

Payment Terms

30 days.
"""

text2 = """
Eligibility

Minimum experience 4 years.

Technical

ISO Certified Company.

Payment

Payment within 45 days.
"""

comparison = compare_tenders(text1, text2)

report = generate_report(
    "Bridge Tender",
    "Road Tender",
    comparison
)

print(report)