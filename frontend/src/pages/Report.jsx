import { useEffect, useState } from "react";

function Report() {
    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(true);

    const [modalTitle, setModalTitle] = useState("");
    const [modalContent, setModalContent] = useState("");

    useEffect(() => {
        async function fetchReport() {
            try {
                const repoId = localStorage.getItem("repo_id");

                if (!repoId) {
                    alert("Repository not found.");
                    return;
                }

                const response = await fetch("http://127.0.0.1:5000/review", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        repo_id: repoId,
                        query: "Generate a complete security report.",
                    }),
                });

                const data = await response.json();
                setReport(data.review);
            } catch (error) {
                console.error("Error fetching report:", error);
            } finally {
                setLoading(false);
            }
        }

        fetchReport();
    }, []);

    const openModal = (title, content) => {
        setModalTitle(title);
        setModalContent(content);
    };

    const closeModal = () => {
        setModalTitle("");
        setModalContent("");
    };

    const renderLongText = (text, title) => {
        if (!text) return "-";

        if (text.length <= 100) return text;

        return (
            <>
                {text.substring(0, 100)}...
                <button
                    onClick={() => openModal(title, text)}
                    className="ml-2 text-blue-600 hover:underline font-medium"
                >
                    Read More
                </button>
            </>
        );
    };

    if (loading) {
        return (
            <div className="text-center mt-20 text-2xl">
                Generating Security Report...
            </div>
        );
    }

    if (!report) {
        return (
            <div className="text-center mt-20 text-red-600">
                Failed to load report.
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <h1 className="text-4xl font-bold text-center text-[#2e3d4c] mb-8">
                Security Report
            </h1>

            <div className="grid md:grid-cols-4 gap-6 mb-10">
                <div className="bg-red-100 rounded-xl p-6 text-center">
                    <h2 className="text-2xl font-bold text-red-600">{report.summary?.critical ?? 0}</h2>
                    <p>Critical</p>
                </div>

                <div className="bg-orange-100 rounded-xl p-6 text-center">
                    <h2 className="text-2xl font-bold text-orange-600">{report.summary?.high ?? 0}</h2>
                    <p>High</p>
                </div>

                <div className="bg-yellow-100 rounded-xl p-6 text-center">
                    <h2 className="text-2xl font-bold text-yellow-600">{report.summary?.medium ?? 0}</h2>
                    <p>Medium</p>
                </div>

                <div className="bg-green-100 rounded-xl p-6 text-center">
                    <h2 className="text-2xl font-bold text-green-600">{report.summary?.low ?? 0}</h2>
                    <p>Low</p>
                </div>
            </div>

            <div className="bg-white rounded-xl shadow p-6 overflow-x-auto">
                <table className="w-full border-collapse">
                    <thead className="border-b bg-gray-50">
                        <tr>
                            <th className="text-left p-3">File</th>
                            <th className="text-left p-3">Rule</th>
                            <th className="text-left p-3">OWASP</th>
                            <th className="text-left p-3">Severity</th>
                            <th className="text-left p-3">Description</th>
                            <th className="text-left p-3">Recommendation</th>
                        </tr>
                    </thead>

                    <tbody>
                        {(report.issues || []).map((issue, index) => (
                            <tr key={index} className="border-b hover:bg-gray-50">
                                <td className="p-3 whitespace-nowrap">{issue.file}</td>
                                <td className="p-3">{issue.rule}</td>
                                <td className="p-3 whitespace-nowrap">{issue.owasp_category || "-"}</td>

                                <td className={`p-3 font-semibold ${
                                    issue.severity === "Critical"
                                        ? "text-red-600"
                                        : issue.severity === "High"
                                        ? "text-orange-600"
                                        : issue.severity === "Medium"
                                        ? "text-yellow-600"
                                        : "text-green-600"
                                }`}>
                                    {issue.severity}
                                </td>

                                <td className="p-3 max-w-sm">
                                    {renderLongText(issue.description, "Issue Description")}
                                </td>

                                <td className="p-3 max-w-sm">
                                    {renderLongText(issue.recommendation, "Recommendation")}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                {(!report.issues || report.issues.length === 0) && (
                    <div className="text-center py-8 text-gray-500">
                        No issues found.
                    </div>
                )}
            </div>

            {modalContent && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-xl shadow-xl w-11/12 md:w-2/3 lg:w-1/2 max-h-[80vh] overflow-hidden">
                        <div className="flex justify-between items-center border-b p-5">
                            <h2 className="text-2xl font-bold">{modalTitle}</h2>

                            <button
                                onClick={closeModal}
                                className="text-2xl text-gray-500 hover:text-black"
                            >
                                ×
                            </button>
                        </div>

                        <div className="p-5 overflow-y-auto max-h-[60vh] whitespace-pre-wrap leading-7 text-gray-700">
                            {modalContent}
                        </div>

                        <div className="border-t p-4 flex justify-end">
                            <button
                                onClick={closeModal}
                                className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg"
                            >
                                Close
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Report;
