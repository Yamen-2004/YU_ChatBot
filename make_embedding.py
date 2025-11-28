import json
import re
from pathlib import Path
from sentence_transformers import SentenceTransformer

# المسارات الحقيقية عندك، مش مسارات فلسفية
CHUNK_FILE = Path("C:/Users/yamen/Downloads/chunking_data.json")
OUTPUT_FILE = Path("C:/Users/yamen/Downloads/embedded_chunks.json")

# تحميل model embedding
model = SentenceTransformer("all-mpnet-base-v2")

#  قراءة data كـ JSON array
data = json.loads(CHUNK_FILE.read_text(encoding="utf-8"))

if not isinstance(data, list):
    print("❌ الداتا مش array! شيّك الفايل.")
    exit()

#  embedding على النصوص فقط
texts = [re.sub(r"\s+", " ", rec.get("text", "")).strip() for rec in data]
vectors = model.encode(texts)

#  إضافة المتجه لكل record
for i, rec in enumerate(data):
    rec["embedding"] = vectors[i].tolist()

#  حفظ الفايل النهائي
OUTPUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

print("✅ embedding خلص. عدد القطع:", len(data))
print("📌 مثال أول vector طول أبعاده:", len(data[0]["embedding"]))
