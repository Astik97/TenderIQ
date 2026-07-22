from backend.models.comparison import Comparison

report = Comparison(1,
                    2,
                    96.8,
                    "Very Similar")

print(report)

print(report.similarity)