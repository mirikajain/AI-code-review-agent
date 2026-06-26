
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="bg-[#2e3d4c] text-white px-6 py-4 flex justify-between items-center shadow-md">
      <h1 className="text-xl font-bold">AI Code Review Agent</h1>

      <div className="flex gap-14">
        <Link to="/" className="hover:text-gray-200">
          Upload
        </Link>

        <Link to="/report" className="hover:text-gray-200">
          Reports
        </Link>

        <Link to="/history" className="hover:text-gray-200">
          History
        </Link>
      </div>
    </nav>
  );
}

export default Navbar;


