import { useNavigate } from "react-router-dom"

export default function Dashboard(){

  const navigate = useNavigate()

  return(

    <div className="p-10">

      <h1 className="text-3xl font-bold text-primary mb-6">
        Patient Dashboard
      </h1>

      <div className="grid grid-cols-2 gap-6">

        <div className="bg-white p-6 rounded-xl shadow">

          <h2 className="text-xl font-semibold mb-4">
            Patient Details
          </h2>

          <p>Name: John Doe</p>
          <p>Blood Group: O+</p>
          <p>Age: 32</p>

        </div>

        <div className="bg-white p-6 rounded-xl shadow">

          <h2 className="text-xl font-semibold mb-4">
            AI Assistant
          </h2>

          <button
          onClick={()=>navigate("/assistant")}
          className="bg-primary text-white px-5 py-3 rounded-lg"
          >
            Start Assistant
          </button>

        </div>

      </div>

    </div>
  )
}