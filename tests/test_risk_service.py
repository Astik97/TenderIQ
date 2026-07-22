from backend.services.risk_service import analyze_risk

difference = {"added": ["payment", "45"],"removed": ["30"]}

risk = analyze_risk(similarity=22.03,difference=difference)

print("=" * 60)

print("Risk Analysis")

print("=" * 60)

for key, value in risk.items():

    print(f"{key} : {value}")   