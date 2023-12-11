"use client"
import axios from 'axios'
import { useState } from "react";

export default function Home() {

  const [ result, setResult ] = useState<string>("")
  const [ click, setClick ] = useState<boolean>(true)
  const [ clickk, setClickk ] = useState<boolean>(true)
  const [ clickkk, setClickkk ] = useState<boolean>(true)

  async function submitWithEdge(){
    if(click){
      setClick(false)
      const chat = await axios.post("/api/chat_with_edge");
      setResult(chat.data)
    }
  }

  async function submitWithoutEdge(){
    if(clickk){
      setClickk(false)
      const chat = await axios.post("/api/chat_without_edge");
      setResult(chat.data)
    }
  }

  async function submitpy(){
    if(clickkk){
      setClickkk(false)
      const chat = await axios.get("/apii/python");
      setResult(chat.data.message)
    }
  }

  return (
    <main className="flex h-screen w-screen justify-center items-center">
      <div className='flex flex-col gap-10 max-w-lg'>
        <p className='text-center'>!! !! !! Open Network tb before clicking !! !! !!</p>
        <button onClick={e => submitWithEdge()} type='button' className={`border p-2 ${click ? 'border-white cursor-pointer' : 'text-gray-800 border-gray-800 cursor-default'}`}>Run req with edge runtime</button>
        <button onClick={e => submitpy()} type='button' className={`border p-2 ${clickkk ? 'border-white cursor-pointer' : 'text-gray-800 border-gray-800 cursor-default'}`}>Py request</button>
        <button onClick={e => submitWithoutEdge()} type='button' className={`border p-2 ${clickk ? 'border-white cursor-pointer' : 'text-gray-800 border-gray-800 cursor-default'}`}>Run req without edge runtime</button>
        <p>{result}</p>
      </div>
    </main>
  )
}
