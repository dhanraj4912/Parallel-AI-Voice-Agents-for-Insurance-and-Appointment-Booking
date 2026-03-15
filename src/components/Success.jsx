export default function Success(){

  return(

    <div className="flex items-center justify-center h-screen">

      <div className="bg-white p-10 rounded-xl shadow text-center">

        <h1 className="text-3xl font-bold text-green-600">
          Appointment Confirmed
        </h1>

        <p className="mt-3">
          Your booking was successful.
        </p>

      </div>

    </div>

  )
}