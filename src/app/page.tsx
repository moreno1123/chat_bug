"use client"
import axios from 'axios'
import { useState } from "react";

export default function Home() {

  const [ result, setResult ] = useState<string>("")

  async function submitWithEdge(){
    const chat = await axios.post("/api/chat_with_edge");

    setResult(chat.data)
  }

  async function submitWithoutEdge(){
    const chat = await axios.post("/api/chat_without_edge");

    setResult(chat.data)
  }

  return (
    <main className="flex h-screen w-screen justify-center items-center">
      <div className='flex flex-col gap-10 max-w-lg'>
        <button onClick={e => submitWithEdge()} type='button' className='border border-white cursor-pointer p-2'>Run req with edge runtime</button>
        <button onClick={e => submitWithoutEdge()} type='button' className='border border-white cursor-pointer p-2'>Run req without edge runtime</button>
        <p>{result}</p>
      </div>
    </main>
  )
}
