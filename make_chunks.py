import json
import re
from pathlib import Path
from uuid import uuid4
import random

INPUT_FILE = Path("C:/Users/yamen/Downloads/clean_data.json")
OUTPUT_FILE = Path("C:/Users/yamen/Downloads/chunking_data.json")

def normalize_text(t: str) -> str:
    if not t or not isinstance(t, str):
        return ""
    t = re.sub(r"\s+", " ", t)
    return t.strip()

def chunk_text(text: str, max_chars=900) -> list[str]:
    text = normalize_text(text)
    if not text:
        return []
    sentences = re.split(r'(?<=[.!؟]) ', text)
    chunks, current = [], ""
    for s in sentences:
        if len(current) + len(s) + 1 <= max_chars:
            current += s + " "
        else:
            chunks.append(current.strip())
            current = s + " "
    if current.strip():
        chunks.append(current.strip())
    return chunks

def main():
    data = json.loads(INPUT_FILE.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        print("❌ الداتا مش list! افحص ملفك.")
        return

    chunk_count = 0
    all_chunks = []

    for i, rec in enumerate(data):
        text_block = rec.get("content") or rec.get("text") or rec.get("description") or ""
        text_block = normalize_text(text_block)

        if not text_block:
            print(f"⚠️ سجل {i} فاضي نصيًا، اتخطاه.")
            continue

        chunks = chunk_text(text_block)
        if not chunks:
            print(f"⚠️ سجل {i} ما طلع منه شنكات رغم إنه مش فاضي؟ غريب.")
            continue

        for c in chunks:
            all_chunks.append({
                "chunk_id": str(uuid4()),
                "doc_id": f"doc_{i}",
                "text": c,
                "url": rec.get("url"),
                "title": rec.get("title")
            })
            chunk_count += 1

    # حفظ كـ JSONL: كل chunk في سطر منفصل بس داخل array-style ملف
    with OUTPUT_FILE.open("w", encoding="utf-8") as out:
        for ch in all_chunks:
            out.write(json.dumps(ch, ensure_ascii=False) + "\n")

    print("\n✅ الملف انحفظ و chunks اتولدت:", chunk_count)

    # عرض preview عشوائي حتى تتأكد منها
    if all_chunks:
        print("\n🔎 Preview samples:")
        for s in random.sample(all_chunks, min(3, len(all_chunks))):
            print("-", s["text"][:120], "...")

if __name__ == "__main__":
    main()
