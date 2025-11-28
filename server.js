
//THIS CODE IS FOR UPLOADING VECTORS TO MONGODB
const fs = require("fs");
const path = require("path");
const { MongoClient } = require("mongodb");

//  عدّل هذا السطر حسب Cluster URI تبعك:
const MONGO_URI = "put your MongoDB connection string here";

//  عدّل اسم الملف حسب مكان ملفك الحقيقي:
const INPUT_FILE = "C:/Users/yamen/Downloads/embedded_chunks.json";

//  اسم الـ database و الـ collection اللي بدك تخزّن فيهم:
const DB_NAME = "yourDatabaseName";
const COLLECTION_NAME = "yourCollectionName";

async function main() {
  console.log("📌 بدء قراءة الملف...");

  if (!fs.existsSync(INPUT_FILE)) {
    console.error("❌ الملف غير موجود:", INPUT_FILE);
    process.exit(1);
  }

  const raw = fs.readFileSync(INPUT_FILE, "utf8");
  let docs;
  try {
    docs = JSON.parse(raw);
  } catch (e) {
    console.error(" فشل تحليل JSON:", e.message);
    process.exit(1);
  }

  if (!Array.isArray(docs)) {
    console.error(" البيانات يجب أن تكون JSON array مش JSON object!");
    process.exit(1);
  }

  console.log(" عدد السجلات داخل الملف:", docs.length);
  console.log(" مثال أول سجل:", docs[0]);

  const client = new MongoClient(MONGO_URI);

  console.log("📌 الاتصال بالداتابيز...");
  await client.connect();
  console.log("✅ تم الاتصال!");

  const db = client.db(DB_NAME);
  const col = db.collection(COLLECTION_NAME);

  console.log("📌 بدء الإدخال للـ collection:", COLLECTION_NAME);

  let inserted = 0;
  for (const doc of docs) {
    await col.insertOne({
      chunk_id: doc.chunk_id || doc.chunk_id || `auto_${inserted++}`,
      doc_id: doc.doc_id || "unknown",
      text: doc.text,
      url: doc.url,
      embedding: doc.embedding,
    });
    inserted++;
  }

  console.log("✅ تم إدخال السجلات:", inserted);

  inserted = await col.countDocuments();
  console.log("📊 عدد السجلات داخل DB بعد الإدخال:", inserted);

  process.exit(0);
}

main();


