from sentence_transformers import SentenceTransformer
import faiss


# Read file
file = open("data/all_website_data.txt", "r", encoding="utf-8")

text = file.read()

file.close()
sentences = text.split(".")


chunks = []

current_chunk = ""


for sentence in sentences:

    if len(current_chunk) + len(sentence) < 500:

        current_chunk += sentence + "."

    else:

        chunks.append(current_chunk)

        current_chunk = sentence + "."


if current_chunk:

    chunks.append(current_chunk)


# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Create embeddings
embeddings = model.encode(chunks)


# Create FAISS
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)


print("Real website vectors stored successfully")

question = input("Ask question: ")


# Convert question
question_embedding = model.encode([question])


# Search similar chunk
distance, result = index.search(question_embedding, 1)


print("\nRelevant answer found:\n")

print(chunks[result[0][0]])