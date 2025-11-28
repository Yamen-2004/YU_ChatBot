const { MongoClient } = require("mongodb");

const MONGO_URI = "put your MongoDB connection string here";

async function main() {
  const client = new MongoClient(MONGO_URI);
  
  try {
    console.log("📌 الاتصال بالداتابيز...");
    await client.connect();
    console.log("✅ تم الاتصال!");

    const db = client.db("yourDatabaseName"); // استبدل باسم الداتابيز
    const col = db.collection("yourCollectionName"); // استبدل باسم الكولكشن

    // هذا الـ vector اللي بدك تبحث عنه (سؤالك)
    const myVector = [0.1, 0.2, 0.3, 0.4, 0.5]; //   استبدل بالقيم الحقيقية للـ vector
  
    console.log("📌 بدء البحث المتجهي...");
    const results = await col.aggregate([
      {
        $vectorSearch: {
          index: "vector_index",
          path: "embedding",
          queryVector: myVector,
          numCandidates: 200,
          limit: 5
        }
      },
      {
        $project: {
          text: 1,
          url: 1,
          title: 1
        }
      }
    ]).toArray();

    console.log(" أقرب Chunks:");
    console.log(results); 
  } catch (e) {
    console.error(" في خطأ بالبحث:", e);
  } finally {
    await client.close();
    process.exit(0);
  }
}

main();
