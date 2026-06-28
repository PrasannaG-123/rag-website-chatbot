from sentence_transformers import SentenceTransformer
import faiss


# Example chunks
chunks = [

    "Python is a programming language",

    "Python supports machine learning",

    "Python latest version is 3.14.6"

]


# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Convert chunks to embeddings
embeddings = model.encode(chunks)


# Get vector dimension
dimension = embeddings.shape[1]


# Create FAISS index
index = faiss.IndexFlatL2(dimension)


# Store vectors
index.add(embeddings)


print("Vectors stored successfully")
question = "What is latest Python version?"


# Convert question into vector
question_embedding = model.encode([question])


# Search nearest chunk
distance, result = index.search(question_embedding, 1)


print("Best matching chunk:")

print(chunks[result[0][0]])