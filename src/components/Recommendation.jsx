export default function Recommendation(){

  return(

    <div className="p-10">

      <h1 className="text-3xl font-bold text-primary mb-6">
        Recommended Doctors
      </h1>

      <div className="grid grid-cols-3 gap-6">

        <div className="bg-white p-6 shadow rounded-xl">

          <h2 className="font-bold">Dr Sharma</h2>
          <p>Cardiologist</p>
          <p>Fee ₹500</p>

          <button className="mt-4 bg-primary text-white px-4 py-2 rounded">
            Book
          </button>

        </div>

      </div>

    </div>
  )
}