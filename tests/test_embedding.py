from backend.services.embedding_service import generate_embedding

text = "The bidder shall submit the EMD within 30 days."

embedding = generate_embedding(text)

print(type(embedding))
print(embedding.shape)
print(embedding[:10])

e1 = generate_embedding("The bidder shall submit EMD.")

e2 = generate_embedding("The vendor must submit the Earnest Money Deposit.")

print(e1.shape)
print(e2.shape)