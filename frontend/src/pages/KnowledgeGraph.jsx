import { useEffect, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";
const API = "http://127.0.0.1:5000";

export default function KnowledgeGraph() {
    const [graph, setGraph] = useState({
        nodes: [],
        links: []
    });

    const [loading, setLoading] = useState(true);

    const [selectedNode, setSelectedNode] = useState(null);

    useEffect(() => {
        async function loadGraph() {
            try {
                const repoId = localStorage.getItem("repo_id");

                if (!repoId) {
                    alert("Repository not found.");
                    return;
                }

                const response = await fetch(
                    `${API}/repository/${repoId}/graph`
                );

                const data = await response.json();

                if (data.success) {
                    console.log(data.graph);
                    setGraph(data.graph);
                    console.log(data.graph.nodes.length);
                    console.log(data.graph.links.length);
                }

            } catch (error) {
                console.error(error);
            } finally {
                setLoading(false);
            }
        }

        loadGraph();
    }, []);

    function nodeColor(node) {

        switch (node.type) {

            case "Repository":
                return "#2563eb";

            case "File":
                return "#16a34a";

            case "Class":
                return "#9333ea";

            case "Method":
                return "#ea580c";

            case "Interface":
                return "#ca8a04";

            case "Issue":
                return "#dc2626";

            default:
                return "#6b7280";
        }
    }

    if (loading) {
        return (
            <div className="text-center text-2xl mt-20">
                Loading Knowledge Graph...
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-100">

            <h1 className="text-4xl font-bold text-center py-6 text-[#2e3d4c]">
                Repository Knowledge Graph
            </h1>

            <div className="flex h-[85vh]">

                {/* Graph */}

                <div className="flex-1 bg-white rounded-xl shadow mx-5">

                    <ForceGraph2D

                        graphData={graph}

                        nodeLabel="label"

                        nodeColor={nodeColor}

                        d3VelocityDecay={0.45}

                        d3AlphaDecay={0.03}

                        cooldownTicks={300}
                        nodeRelSize={6}

                        nodeVal={(node) => {
                            if (node.type === "Repository") return 20;
                            if (node.type === "File") return 8;
                            if (node.type === "Issue") return 6;
                            return 4;
                        }}

                        linkColor={() => "#cfcfcf"}

                        linkWidth={0.6}

                        onNodeClick={async (node) => {

                            const response = await fetch(

                                `${API}/node/${node.id}`

                            );

                            const data = await response.json();

                            if (data.success) {

                                setSelectedNode(data.details);

                            }

                        }}

                        nodeCanvasObject={(node, ctx, globalScale) => {

                            let radius = 4;

                            if (node.type === "Repository") radius = 12;
                            else if (node.type === "File") radius = 7;
                            else if (node.type === "Issue") radius = 6;

                            ctx.beginPath();
                            ctx.arc(node.x, node.y, radius, 0, 2 * Math.PI);
                            ctx.fillStyle = nodeColor(node);
                            ctx.fill();

                            // Show labels only when zoomed in
                            if (globalScale > 2) {

                                const fontSize = 12 / globalScale;

                                ctx.font = `${fontSize}px Sans-Serif`;
                                ctx.fillStyle = "#000";

                                ctx.fillText(
                                    node.label,
                                    node.x + 8,
                                    node.y + 4
                                );
                            }
                        }}
                    />

                </div>

                {/* Side Panel */}

                <div className="w-80 bg-white rounded-xl shadow mr-5 p-5">

                    <h2 className="text-2xl font-bold mb-5">
                        Node Details
                    </h2>

                    {selectedNode && (

                        <div>

                            <h2 className="text-xl font-bold mb-4">

                                {selectedNode.properties.name ||
                                    selectedNode.properties.path ||
                                    selectedNode.properties.id}

                            </h2>

                            <p>

                                <b>Type:</b>

                                {selectedNode.type}

                            </p>

                            <hr className="my-4" />

                            <h3 className="font-bold">

                                Properties

                            </h3>

                            {

                                Object.entries(selectedNode.properties).map(

                                    ([key, value]) => (

                                        <div key={key}>

                                            <b>{key}</b> : {String(value)}

                                        </div>

                                    )

                                )

                            }

                            <hr className="my-4" />

                            <h3 className="font-bold">

                                Connected Nodes

                            </h3>

                            {

                                selectedNode.children.map((child, index) => (

                                    <div key={index}

                                        className="mb-3">

                                        <div>

                                            <b>

                                                {child.relationship}

                                            </b>

                                        </div>

                                        <div>

                                            {

                                                child.target.join(",")

                                            }

                                        </div>

                                        <div>

                                            {

                                                child.properties.name ||

                                                child.properties.path ||

                                                child.properties.rule ||

                                                "Node"

                                            }

                                        </div>

                                    </div>

                                ))

                            }

                        </div>

                    )}

                    <hr className="my-6" />

                    <h3 className="font-bold mb-3">
                        Legend
                    </h3>

                    <div className="space-y-2 text-sm">

                        <div className="flex items-center gap-2">
                            <div className="w-4 h-4 rounded-full bg-blue-600"></div>
                            Repository
                        </div>

                        <div className="flex items-center gap-2">
                            <div className="w-4 h-4 rounded-full bg-green-600"></div>
                            File
                        </div>

                        <div className="flex items-center gap-2">
                            <div className="w-4 h-4 rounded-full bg-purple-600"></div>
                            Class
                        </div>

                        <div className="flex items-center gap-2">
                            <div className="w-4 h-4 rounded-full bg-orange-600"></div>
                            Method
                        </div>

                        <div className="flex items-center gap-2">
                            <div className="w-4 h-4 rounded-full bg-yellow-500"></div>
                            Interface
                        </div>

                        <div className="flex items-center gap-2">
                            <div className="w-4 h-4 rounded-full bg-red-600"></div>
                            Issue
                        </div>

                    </div>

                </div>

            </div>

        </div>
    );
}