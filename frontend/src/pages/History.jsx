import React from 'react'

function History() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">

      <h1 className="text-4xl font-bold text-center text-[#2e3d4c] mb-8">
        Scan History
      </h1>

      <div className="max-w-4xl mx-auto space-y-5">

        <div className="bg-white rounded-xl shadow p-5 flex justify-between items-center">

          <div>
            <h2 className="font-bold text-lg">Ecommerce.zip</h2>
            <p className="text-gray-500">
              25 June 2026
            </p>
          </div>

          <div className="text-right">
            <p className="font-semibold">12 Issues</p>
            <button className="mt-2 px-4 py-2 bg-[#2e3d4c] text-white rounded-lg">
              View Report
            </button>
          </div>

        </div>

        <div className="bg-white rounded-xl shadow p-5 flex justify-between items-center">

          <div>
            <h2 className="font-bold text-lg">Hospital.zip</h2>
            <p className="text-gray-500">
              24 June 2026
            </p>
          </div>

          <div className="text-right">
            <p className="font-semibold">7 Issues</p>
            <button className="mt-2 px-4 py-2 bg-[#2e3d4c] text-white rounded-lg">
              View Report
            </button>
          </div>

        </div>

        <div className="bg-white rounded-xl shadow p-5 flex justify-between items-center">

          <div>
            <h2 className="font-bold text-lg">Banking.zip</h2>
            <p className="text-gray-500">
              22 June 2026
            </p>
          </div>

          <div className="text-right">
            <p className="font-semibold">5 Issues</p>
            <button className="mt-2 px-4 py-2 bg-[#2e3d4c] text-white rounded-lg">
              View Report
            </button>
          </div>

        </div>

      </div>

    </div>
  );
}

export default History;

