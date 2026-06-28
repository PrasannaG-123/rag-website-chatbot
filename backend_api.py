from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from main_chatbot import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global storage
chunks = []
model = None
index = None


# ==========================
# PROCESS WEBSITE
# ==========================
@app.post("/process-url")
def process_url(data: dict):

    global chunks, model, index

    website_url = data["url"]

    print("STEP 1: Crawling website")

    all_data = crawl_website(website_url)

    # CHECK 1 → website crawl failed
    if len(all_data) == 0:
        return {
            "message": "Could not process website"
        }

    print("STEP 2: Creating chunks")

    chunks = create_chunks(all_data)

    # CHECK 2 → chunking failed
    if len(chunks) == 0:
        return {
            "message": "No text found on website"
        }

    print("STEP 3: Building vector database")

    model, index = build_vector_store(chunks)

    if model is None:
        return {
            "message": "Could not build vector database"
        }

    print("Website successfully processed")

    return {
        "message": "Website processed successfully"
    }

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    global chunks, model, index

    file_location = "uploaded_file.pdf"

    with open(file_location, "wb") as f:

        f.write(await file.read())

    print("STEP 1: Reading PDF")

    all_data = read_pdf(file_location)

    print("STEP 2: Creating chunks")

    chunks = create_chunks(all_data)

    print("STEP 3: Building vector database")

    model, index = build_vector_store(chunks)

    if model is None:

        return {
            "message": "Could not process PDF"
        }

    return {
        "message": "PDF processed successfully"
    }

# ==========================
# ASK QUESTION
# ==========================
@app.post("/ask-question")
def ask_user_question(data: dict):

    global chunks, model, index

    try:
        question = data["question"]

        print("QUESTION =", question)

        answer = ask_question(
            question,
            model,
            index,
            chunks
        )

        print("ANSWER =", answer)

        return {
            "answer": answer
        }

    except Exception as e:
        print("FULL ERROR =", e)

        return {
            "answer": str(e)
        }

