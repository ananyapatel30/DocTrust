import os
from dotenv import load_dotenv

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from google import genai

# Load API key
load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def retrieve_relevant_chunks(chunks, question, top_k=5):
    """
    Retrieve the most relevant chunks using TF-IDF.
    """

    vectorizer = TfidfVectorizer(
        stop_words="english",
        lowercase=True,
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(chunks + [question])

    similarity = cosine_similarity(vectors[-1], vectors[:-1]).flatten()

    indices = similarity.argsort()[-top_k:][::-1]

    return [chunks[i] for i in indices]

def ask_gemini(chunks, question):

    context = "\n\n".join(chunks)

    prompt = f"""
You are an AI assistant that answers questions ONLY from the uploaded PDF.

Instructions:
- Answer only from the given context.
- If the answer is present, explain it clearly.
- If the answer is not available in the context, reply:
  "I could not find this information in the uploaded document."

Context:
{context}

Question:
{question}

Answer:
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text