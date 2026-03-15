import { useContext } from "react"
import { datacontext } from "../context/UserContext"

export default function Assistant(){

  const {connect,disconnect,messages,status} = useContext(datacontext)

  return(

    <div className="flex h-screen">

      <div className="w-1/3 bg-white shadow p-6">

        <h2 className="text-xl font-bold mb-4">
          AI Medical Assistant
        </h2>

        <p>Status: {status}</p>

        <div className="flex gap-3 mt-4">

          <button
          onClick={connect}
          className="bg-green-500 text-white px-4 py-2 rounded"
          >
            Connect
          </button>

          <button
          onClick={disconnect}
          className="bg-red-500 text-white px-4 py-2 rounded"
          >
            Disconnect
          </button>

        </div>

      </div>

      <div className="flex-1 p-6 overflow-y-scroll">

        {messages.map((msg,index)=>(
          <div key={index} className="mb-3">

            <b>{msg.sender}:</b> {msg.text}

          </div>
        ))}

      </div>

    </div>
  )
}