import { Chroma } from "langchain/vectorstores/chroma";
import { OpenAIEmbeddings } from "langchain/embeddings/openai";
import { env } from "process";

export default async function vector(){
  const vectorStore = await Chroma.fromExistingCollection(
    new OpenAIEmbeddings(),
    {
      url: env.CHROMA_DB_SERVER,
      collectionName: "b5877065-aa52-4641-93ef-98966b3deb11",
    },
  );

  console.log("vectorStorevectorStorevectorStorevectorStorevectorStorevectorStorevectorStorevectorStore")
  console.log(vectorStore)
  console.log("vectorStorevectorStorevectorStorevectorStorevectorStorevectorStorevectorStorevectorStore")

  return vectorStore;
}