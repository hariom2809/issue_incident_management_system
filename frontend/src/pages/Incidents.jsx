import { useEffect, useState } from "react";
import { getIssues, createIssue } from "../api/issues";

export default function Incidents() {
  const [issues, setIssues] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const loadIssues = async () => {
    try {
      const data = await getIssues();
      setIssues(data);
    } catch (err) {
      console.error("Failed loading issues", err);
    }
  };

  useEffect(() => {
    loadIssues();
  }, []);

  const handleCreate = async () => {
    if (!title || !description) {
      alert("Fill all fields");
      return;
    }

    await createIssue({
      title,
      description,
      priority: "medium",
    });

    setTitle("");
    setDescription("");

    loadIssues(); // refresh table
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Incidents</h1>

      {/* Create Issue */}
      <div className="bg-white p-4 rounded shadow mb-6">
        <h2 className="font-semibold mb-2">Create Issue</h2>

        <input
          className="border p-2 mr-2"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <input
          className="border p-2 mr-2"
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <button
          onClick={handleCreate}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Create
        </button>
      </div>

      {/* Issues Table */}
      <table className="w-full border">
        <thead className="bg-gray-200">
          <tr>
            <th className="p-2 border">Title</th>
            <th className="p-2 border">Priority</th>
            <th className="p-2 border">Status</th>
          </tr>
        </thead>

        <tbody>
          {issues.map((issue) => (
            <tr key={issue.id}>
              <td className="p-2 border">{issue.title}</td>
              <td className="p-2 border">{issue.priority}</td>
              <td className="p-2 border">{issue.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}