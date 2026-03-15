import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function App() {
  const navigate = useNavigate();

  const [email,setEmail] = useState("")
  const [password,setPassword] = useState("")

  const handleLogin = (e)=>{
    e.preventDefault()

    if(email === "test@test.com" && password === "123456"){
      localStorage.setItem("user_id","1")
      navigate("/dashboard")
    } else {
      alert("Invalid credentials")
    }
  }

  return(

    <div className="flex min-h-screen items-center justify-center">

      <div className="card w-[400px]">

        <h1 className="text-2xl font-bold text-center text-blue-600 mb-6">
          AI Medical Assistant
        </h1>

        <form onSubmit={handleLogin} className="flex flex-col gap-4">

          <input
          type="email"
          placeholder="Email"
          className="border rounded-lg p-3"
          value={email}
          onChange={(e)=>setEmail(e.target.value)}
          />

          <input
          type="password"
          placeholder="Password"
          className="border rounded-lg p-3"
          value={password}
          onChange={(e)=>setPassword(e.target.value)}
          />

          <button className="btn-primary">
            Login
          </button>

        </form>

        <p className="text-sm text-gray-500 mt-4 text-center">
          demo login → test@test.com / 123456
        </p>

      </div>

    </div>
  )
}