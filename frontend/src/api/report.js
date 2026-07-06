const API_URL = "http://127.0.0.1:5000";

export async function getSecurityReport(repoId) {

    const response = await fetch(`${API_URL}/review`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            repo_id: repoId,
            query: "Generate a complete security report for this repository."
        })

    });

    if (!response.ok) {
        throw new Error("Failed to generate report");
    }

    return await response.json();
}