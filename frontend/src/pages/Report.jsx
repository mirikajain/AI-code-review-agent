import { useEffect, useState } from "react";

function Report() {

    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(true);

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
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({

                        repo_id: repoId,

                        query: "Generate a complete security report."

                    })

                });

                const data = await response.json();

                setReport(data.review);

            } catch (error) {

                console.error(error);

            } finally {

                setLoading(false);

            }

        }

        fetchReport();

    }, []);

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

                    <h2 className="text-2xl font-bold text-red-600">
                        {report.summary.critical}
                    </h2>

                    <p>Critical</p>

                </div>

                <div className="bg-orange-100 rounded-xl p-6 text-center">

                    <h2 className="text-2xl font-bold text-orange-600">
                        {report.summary.high}
                    </h2>

                    <p>High</p>

                </div>

                <div className="bg-yellow-100 rounded-xl p-6 text-center">

                    <h2 className="text-2xl font-bold text-yellow-600">
                        {report.summary.medium}
                    </h2>

                    <p>Medium</p>

                </div>

                <div className="bg-green-100 rounded-xl p-6 text-center">

                    <h2 className="text-2xl font-bold text-green-600">
                        {report.summary.low}
                    </h2>

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

                        {report.issues.map((issue, index) => (

                            <tr
                                key={index}
                                className="border-b hover:bg-gray-50"
                            >

                                <td className="p-3">

                                    {issue.file}

                                </td>

                                <td className="p-3">

                                    {issue.rule}

                                </td>

                                <td
                                    className={`p-3 font-semibold ${
                                        issue.severity === "Critical"
                                            ? "text-red-600"
                                            : issue.severity === "High"
                                            ? "text-orange-600"
                                            : issue.severity === "Medium"
                                            ? "text-yellow-600"
                                            : "text-green-600"
                                    }`}
                                >

                                    {issue.severity}

                                </td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            </div>

        </div>

    );
}

export default Report;