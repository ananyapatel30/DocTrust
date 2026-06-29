from pdf_utils import extract_text_from_pdf, split_text

text = extract_text_from_pdf("uploads/module-2.pdf")

print("=" * 50)
print("First 500 characters:\n")
print(text[:500])

chunks = split_text(text)

print("\nTotal Chunks:", len(chunks))

print("\nFirst Chunk:\n")
print(chunks[0])