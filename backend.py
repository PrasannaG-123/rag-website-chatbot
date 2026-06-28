import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from sentence_transformers import SentenceTransformer
import faiss


def crawl_website(start_url):

    visited = []
    to_visit = [start_url]
    all_text = ""

    while len(to_visit) > 0 and len(visited) < 7:

        url = to_visit.pop(0)

        if url in visited:
            continue

        print("Visiting:", url)
        visited.append(url)

        try:
            response = requests.get(url, timeout=10)

        except:
            print("Could not open:", url)
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        all_text += "\n\n------ NEW PAGE ------\n\n"
        all_text += text

        links = soup.find_all("a")

        for link in links:

            href = link.get("href")

            if href:

                full_url = urljoin(url, href)

                if full_url.startswith("http") and "#" not in full_url:

                    full_url = full_url.rstrip("/")

                    if full_url not in visited and full_url not in to_visit:
                        to_visit.append(full_url)

    with open("data/all_website_data.txt", "w", encoding="utf-8") as file:
        file.write(all_text)

    print("Website data saved")


def create_chunks():

    file = open("data/all_website_data.txt", "r", encoding="utf-8")
    text = file.read()
    file.close()

    if len(text.strip()) == 0:
        print("No website text found")
        return []

    chunk_size = 1000
    chunks = []

    for i in range(0, len(text), chunk_size):

        chunk = text[i:i+chunk_size]
        chunks.append(chunk)

    print("Total chunks created:", len(chunks))
    return chunks


def build_vector_store(chunks):

    if len(chunks) == 0:
        print("No chunks found")
        return None, None

    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode(chunks)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    faiss.write_index(index, "data/faiss_index.bin")

    print("Vector database created successfully")

    return model, index


def ask_question(question, model, index, chunks):

    if model is None:
        return "Website not processed"

    question_embedding = model.encode([question])

    distance, result = index.search(question_embedding, 1)

    best_chunk = chunks[result[0][0]]

    return best_chunk.strip()