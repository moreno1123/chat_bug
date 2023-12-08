import { Chroma } from "langchain/vectorstores/chroma";
import { OpenAIEmbeddings } from "langchain/embeddings/openai";
import { env } from "process";
import { ChatOpenAI } from "langchain/chat_models/openai";
import { ConversationalRetrievalQAChain } from "langchain/chains";
import { NextResponse } from "next/server";
import { StreamingTextResponse, LangChainStream } from "ai";

export const runtime = 'edge';

export async function POST(req:Request) {
  try {
    const { stream, handlers } = LangChainStream();
  
    const vectorStore = await Chroma.fromExistingCollection(
      new OpenAIEmbeddings(),
      {
        url: env.CHROMA_DB_SERVER,
        collectionName: "b5877065-aa52-4641-93ef-98966b3deb11",
      },
    );
  
    const streamingModel = new ChatOpenAI({
      temperature: 0,
      modelName: 'gpt-3.5-turbo',
      streaming: true,
      verbose: true
    });
  
    const chain = ConversationalRetrievalQAChain.fromLLM(
      streamingModel,
      vectorStore.asRetriever(),
    );

    chain.call({
      question: "What is the privacy policy?",
      chat_history: []
    }, [handlers]);

    return new StreamingTextResponse(stream);
  } catch (error:any) {
    return NextResponse.json({error: error.toString()},{status:500});
  }
}