
import requests
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import PyPDF2

from llm import generate_answer


# ==========================
# WEBSITE CRAWLER
# ==========================
def crawl_website(start_url):

    visited = []
    to_visit = [start_url]
    all_data = []

    base_domain = urlparse(start_url).netloc

    while len(to_visit) > 0 and len(visited) < 3:

        url = to_visit.pop(0)

        if url in visited:
            continue

        print("Visiting:", url)
        visited.append(url)

        try:
            response = requests.get(
                url,
                timeout=5,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

        except Exception as e:
            print("Could not open:", url)
            print(e)
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # remove unwanted tags
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.extract()

        text = soup.get_text(separator=" ")

        lines = [line.strip() for line in text.splitlines()]

        clean_text = " ".join(line for line in lines if line)

        all_data.append({
            "url": url,
            "text": clean_text
        })

        links = soup.find_all("a")

        for link in links:

            href = link.get("href")

            if href:

                full_url = urljoin(url, href)

                if full_url.startswith("http"):

                    domain = urlparse(full_url).netloc

                    if domain == base_domain:

                        if "#" not in full_url:

                            full_url = full_url.rstrip("/")

                            if full_url not in visited and full_url not in to_visit:
                                to_visit.append(full_url)

    print("Website crawling finished")

    return all_data


# ==========================
# CHUNKING
# ==========================
def create_chunks(all_data):

    chunks = []

    for page in all_data:

        text = page["text"]
        source = page["url"]

        paragraphs = text.split(".")

        current_chunk = ""

        for para in paragraphs:

            if len(current_chunk) + len(para) < 700:

                current_chunk += para + "."

            else:

                if len(current_chunk.strip()) > 100:

                    chunks.append({
                        "text": current_chunk,
                        "source": source
                    })

                current_chunk = para + "."

        if len(current_chunk.strip()) > 100:

            chunks.append({
                "text": current_chunk,
                "source": source
            })

    print("Chunks created:", len(chunks))

    return chunks


# ==========================
# VECTOR STORE
# ==========================
def build_vector_store(chunks):

    if len(chunks) == 0:
        return None, None

    texts = []

    for chunk in chunks:
        texts.append(chunk["text"])

    print("Loading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode(texts)

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    print("Vector DB ready")

    return model, index


# ==========================
# RETRIEVAL
# ==========================
def retrieve_context(question, model, index, chunks):

    question_embedding = model.encode([question])

    question_embedding = np.array(question_embedding).astype("float32")

    distances, results = index.search(question_embedding, 3)

    context = ""
    sources = []

    for i in results[0]:

        chunk = chunks[i]

        context += chunk["text"] + "\n\n"

        if chunk["source"] not in sources:
            sources.append(chunk["source"])

    return context, sources


# ==========================
# FINAL ANSWER
# ==========================
def ask_question(question, model, index, chunks):

    if model is None:
        return "Website not processed"

    context, sources = retrieve_context(
        question,
        model,
        index,
        chunks
    )

    print("Retrieved context")

    final_answer = generate_answer(
        context,
        question
    )

    print("LLM generated answer")

    source_text = "\n\nSources:\n"

    for s in sources:
        source_text += s + "\n"

    return final_answer + source_text

# ==========================
# PDF READER
# ==========================

# ==========================
# PDF READER
# ==========================
def read_pdf(file_path):

    all_data = []

    text = ""

    try:

        with open(file_path, "rb") as file:

            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted + " "

    except Exception as e:

        print("PDF Error:", e)

        return []

    all_data.append({
        "url": "Uploaded PDF",
        "text": text
    })

    print("PDF Loaded Successfully")

    return all_data