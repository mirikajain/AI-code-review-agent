import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import UploadRepository from "./pages/UploadRepository";
import Report from "./pages/Report";
import History from "./pages/History";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<UploadRepository />} />
        <Route path="/report" element={<Report />} />
        <Route path="/history" element={<History />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
