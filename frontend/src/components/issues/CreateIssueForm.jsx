import { useState } from "react";
import { createIssue } from "../../api/issues";
import usePermissions from "../../hooks/usePermissions";

export default function CreateIssueForm({ onCreated }) {
  const { can } = usePermissions();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);

  // RBAC protection (frontend layer)
  if (!can("create_incident")) return null;

  const handleCreate = async () => {
    if (!title || !description) {
      alert("Fill all fields");
      return;
    }

    try {
      setLoading(true);

      await createIssue({
        title,
        description,
        priority: "medium",
      });

      setTitle("");
      setDescription("");

      onCreated(); // reload issues list
    } catch (err) {
      console.error(err);
      alert("Failed to create issue");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-4 rounded shadow mb-6">
      <h2 className="font-semibold mb-3">Create Incident</h2>

      <div className="flex gap-2">
        <input
          className="border p-2 flex-1"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <input
          className="border p-2 flex-1"
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <button
          onClick={handleCreate}
          disabled={loading}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          {loading ? "Creating..." : "Create"}
        </button>
      </div>
    </div>
  );
}