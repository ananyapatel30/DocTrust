from pdf_utils import extract_text_from_pdf, split_text
from rag import retrieve_relevant_chunks, ask_gemini

text = extract_text_from_pdf("uploads/module-2.pdf")
chunks = split_text(text)

question = input("Ask a question: ")

relevant_chunks = retrieve_relevant_chunks(chunks, question)

print("\n========== Retrieved Chunks ==========\n")

for i, chunk in enumerate(relevant_chunks):
    print(f"\n------ Chunk {i+1} ------\n")
    print(chunk[:700])
    print("\n")

answer = ask_gemini(relevant_chunks, question)

print("\n================= ANSWER =================\n")
print(answer)