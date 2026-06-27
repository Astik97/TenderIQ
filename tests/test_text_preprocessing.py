from backend.services.text_preprocessing import (
    normalize_whitespace,
    remove_special_characters,
    convert_to_lowercase,
    clean_text
)

sample = """
Tender Notice

Project Name : Smart City

Eligibility:

• Minimum 5 Years Experience

© Government

"""
print("========== normalize_whitespace ==========")
print(normalize_whitespace(sample))

print("\n========== remove_special_characters ==========")
print(remove_special_characters(sample))

print("\n========== convert_to_lowercase ==========")
print(convert_to_lowercase(sample))

print("\n========== clean_text ==========")
print(clean_text(sample))