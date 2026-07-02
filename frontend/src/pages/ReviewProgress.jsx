

function ReviewProgress() {
  return (
    <div className="min-h-screen bg-gray-100 flex justify-center items-center p-6">
      <div className="bg-white w-full max-w-3xl rounded-2xl shadow-lg p-8">

        <h1 className="text-3xl font-bold text-[#2e3d4c] text-center">
          Reviewing Repository
        </h1>

        <p className="text-gray-500 text-center mt-2">
          Please wait while the AI scans your repository.
        </p>

        <div className="mt-10">
          <div className="w-full h-4 bg-gray-200 rounded-full">
            <div
              className="h-4 bg-[#2e3d4c] rounded-full"
              style={{ width: "65%" }}
            ></div>
          </div>

          <p className="text-center mt-3 font-semibold">
            65% Completed
          </p>
        </div>

        <div className="mt-10 space-y-4">

          <div className="flex justify-between bg-gray-50 p-4 rounded-lg">
            <span>✔ Repository Uploaded</span>
            <span>Done</span>
          </div>

          <div className="flex justify-between bg-gray-50 p-4 rounded-lg">
            <span>✔ Reading C# Files</span>
            <span>Done</span>
          </div>

          <div className="flex justify-between bg-gray-50 p-4 rounded-lg">
            <span>🔄 Checking OWASP Rules</span>
            <span>Running...</span>
          </div>

          <div className="flex justify-between bg-gray-50 p-4 rounded-lg">
            <span>⏳ Generating Report</span>
            <span>Waiting...</span>
          </div>

        </div>

      </div>
    </div>
  );
}

export default ReviewProgress;


