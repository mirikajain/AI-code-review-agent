import { useState } from "react";

function UploadRepository() {
  const [githubUrl, setGithubUrl] = useState("");
  const [file, setFile] = useState(null);

  return (
    <div className="min-h-screen bg-gray-100 flex justify-center items-center px-4">
      <div className="bg-white w-full max-w-2xl rounded-2xl shadow-lg p-8">

        <h1 className="text-3xl font-bold text-center text-[#2e3d4c]">
          Upload Repository
        </h1>

        <p className="text-center text-gray-500 mt-2">
          Scan your .NET/C# repository for security vulnerabilities using AI.
        </p>

        {/* GitHub URL */}
        <div className="mt-8">
          <label className="block text-gray-700 font-medium mb-2">
            GitHub Repository URL
          </label>

          <input
            type="text"
            placeholder="https://github.com/username/repository"
            value={githubUrl}
            onChange={(e) => setGithubUrl(e.target.value)}
            className="w-full border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-[#2e3d4c]"
          />
        </div>

        {/* OR */}
        <div className="flex items-center my-8">
          <div className="flex-1 border-t"></div>
          <span className="mx-4 text-gray-400 font-medium">OR</span>
          <div className="flex-1 border-t"></div>
        </div>

        {/* ZIP Upload */}
        <div>
          <label className="block text-gray-700 font-medium mb-2">
            Upload ZIP File
          </label>

          <input
            type="file"
            accept=".zip"
            onChange={(e) => setFile(e.target.files[0])}
            className="w-full border border-dashed border-gray-400 rounded-lg p-3 cursor-pointer file:mr-4 file:px-4 file:py-2 file:border-0 file:rounded-md file:bg-[#2e3d4c] file:text-white hover:file:bg-[#425466]"
          />

          {file && (
            <p className="text-sm text-green-600 mt-2">
              Selected: {file.name}
            </p>
          )}
        </div>

        {/* Button */}
        <button
          className="w-full mt-8 bg-[#2e3d4c] text-white py-3 rounded-lg text-lg font-semibold hover:bg-[#425466] transition"
        >
          Start Security Review
        </button>

      </div>
    </div>
  );
}

export default UploadRepository;