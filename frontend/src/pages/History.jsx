import { useEffect, useState } from "react";

const API = "http://127.0.0.1:5000";

export default function History() {
  const [history, setHistory] = useState([]);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchHistory() {
      try {
        const res = await fetch(`${API}/history`);
        const data = await res.json();

        if (!cancelled && data.success) {
          setHistory(data.history ?? []);
        }
      } catch (err) {
        console.error(err);
      }
    }

    fetchHistory();

    return () => {
      cancelled = true;
    };
  }, []);

  const refreshHistory = async () => {
    try {
      const res = await fetch(`${API}/history`);
      const data = await res.json();

      if (data.success) {
        setHistory(data.history ?? []);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const openHistory = async (id) => {
    const res = await fetch(`${API}/history/${id}`);
    const data = await res.json();

    if (data.success) {
      setSelected(data.history);
    }
  };

  const deleteHistory = async (id) => {
    if (!window.confirm("Delete this review?")) return;

    await fetch(`${API}/history/${id}`, {
      method: "DELETE",
    });

    await refreshHistory();
    setSelected(null);
  };

  const clearHistory = async () => {
    if (!window.confirm("Delete all history?")) return;

    await fetch(`${API}/history`, {
      method: "DELETE",
    });

    setHistory([]);
    setSelected(null);
  };

  return (
  <div className="min-h-screen bg-gray-100 p-8">
    <div className="max-w-6xl mx-auto">

      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-4xl font-bold text-gray-800">
          Review History
        </h1>

        <button
          onClick={clearHistory}
          className="bg-[#2e3d4c] hover:bg-[#243240] text-white px-5 py-2 rounded-lg transition duration-200 shadow-md"
        >
          Clear All
        </button>
      </div>

      {/* Empty State */}
      {history.length === 0 ? (
        <div className="bg-white rounded-xl shadow-lg p-12 text-center">
          <h2 className="text-2xl font-semibold text-gray-500">
            No Review History Found
          </h2>

          <p className="mt-3 text-gray-400">
            Your previous code reviews will appear here.
          </p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 gap-6">
          {history.map((item) => (
            <div
              key={item.history_id}
              className="bg-white rounded-xl shadow-lg p-6 border border-gray-200 hover:shadow-xl transition duration-300"
            >
              <h2 className="text-xl font-bold text-gray-800 mb-3">
                {item.query}
              </h2>

              <div className="space-y-2 text-gray-600">
                <p>
                  <span className="font-semibold">Repository:</span>{" "}
                  {item.repo_id}
                </p>

                <p>
                  <span className="font-semibold">Created:</span>{" "}
                  {item.created_at}
                </p>
              </div>

              <div className="flex gap-3 mt-6">
                <button
                  onClick={() => openHistory(item.history_id)}
                  className="flex-1 bg-[#2e3d4c] hover:bg-[#243240] text-white py-2 rounded-lg transition duration-200"
                >
                  View Review
                </button>

                <button
                  onClick={() => deleteHistory(item.history_id)}
                  className="flex-1 border border-red-500 text-red-500 hover:bg-red-500 hover:text-white py-2 rounded-lg transition duration-200"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Review Details */}
      {selected && (
        <div className="mt-10 bg-white rounded-xl shadow-xl p-8">

          <h2 className="text-2xl font-bold text-gray-800 mb-5">
            Review Details
          </h2>

          <pre className="bg-gray-900 text-green-400 rounded-lg p-6 overflow-auto text-sm whitespace-pre-wrap">
            {JSON.stringify(selected.review, null, 2)}
          </pre>
        </div>
      )}
    </div>
  </div>
);
}