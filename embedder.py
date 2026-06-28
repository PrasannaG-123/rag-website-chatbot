from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Example chunks
chunks = [

    "Python is a programming language",

    "Python supports machine learning",

    "Python latest version is 3.14.6"

]


# Convert chunks to vectors
embeddings = model.encode(chunks)


print("Embeddings created successfully")

print(embeddings)