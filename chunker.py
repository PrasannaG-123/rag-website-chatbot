file = open("data/all_website_data.txt", "r", encoding="utf-8")

# Read entire file
text = file.read()

# Close file
file.close()


# Size of each chunk
chunk_size = 500


# Empty list to store chunks
chunks = []


# Split text into chunks
for i in range(0, len(text), chunk_size):

    chunk = text[i:i + chunk_size]

    chunks.append(chunk)


# Print total chunks
print("Total chunks created:", len(chunks))


# Print first chunk only
print("\nFirst chunk:\n")

print(chunks[0])