from backend.services.semantic_similarity_service import *

pairs = [

    (
        "Payment shall be completed within 30 days.",

        "Payment must be completed within thirty days."
    ),

    (
        "Bid Security is mandatory.",

        "EMD must be submitted."
    ),

    (
        "Delivery within 90 days.",

        "Bananas are yellow."
    )

]

for first, second in pairs:

    embedding1 = generate_embedding(first)

    embedding2 = generate_embedding(second)

    score = calculate_similarity(embedding1,embedding2)

    print("--------------------------------")

    print(first)

    print(second)

    print(score)
    