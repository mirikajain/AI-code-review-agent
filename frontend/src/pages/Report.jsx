

function Report() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">

      <h1 className="text-4xl font-bold text-center text-[#2e3d4c] mb-8">
        Security Report
      </h1>

      <div className="grid md:grid-cols-4 gap-6 mb-10">

        <div className="bg-red-100 rounded-xl p-6 text-center">
          <h2 className="text-2xl font-bold text-red-600">2</h2>
          <p>Critical</p>
        </div>

        <div className="bg-orange-100 rounded-xl p-6 text-center">
          <h2 className="text-2xl font-bold text-orange-600">4</h2>
          <p>High</p>
        </div>

        <div className="bg-yellow-100 rounded-xl p-6 text-center">
          <h2 className="text-2xl font-bold text-yellow-600">5</h2>
          <p>Medium</p>
        </div>

        <div className="bg-green-100 rounded-xl p-6 text-center">
          <h2 className="text-2xl font-bold text-green-600">3</h2>
          <p>Low</p>
        </div>

      </div>

      <div className="bg-white rounded-xl shadow p-6">

        <table className="w-full">

          <thead className="border-b">

            <tr>
              <th className="text-left p-3">File</th>
              <th className="text-left p-3">Rule</th>
              <th className="text-left p-3">Severity</th>
            </tr>

          </thead>

          <tbody>

            <tr className="border-b hover:bg-gray-50">
              <td className="p-3">LoginController.cs</td>
              <td className="p-3">SQL Injection</td>
              <td className="p-3 text-red-600 font-semibold">Critical</td>
            </tr>

            <tr className="border-b hover:bg-gray-50">
              <td className="p-3">UserService.cs</td>
              <td className="p-3">Hardcoded Password</td>
              <td className="p-3 text-orange-600 font-semibold">High</td>
            </tr>

            <tr className="hover:bg-gray-50">
              <td className="p-3">AuthController.cs</td>
              <td className="p-3">Weak Hashing</td>
              <td className="p-3 text-yellow-600 font-semibold">Medium</td>
            </tr>

          </tbody>

        </table>

      </div>

    </div>
  );
}

export default Report;


