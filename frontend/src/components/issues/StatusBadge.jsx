import { useState } from "react";
import { updateIssueStatus } from "../../api/issues";
import usePermissions from "../../hooks/usePermissions";

export default function StatusBadge({ status, issueId, onUpdated }) {
  const { can } = usePermissions();
  const [updating, setUpdating] = useState(false);

  const statusStyles = {
    open: "bg-red-100 text-red-700",
    in_progress: "bg-yellow-100 text-yellow-700",
    resolved: "bg-green-100 text-green-700",
    closed: "bg-gray-200 text-gray-700",
  };

  const statuses = ["open", "in_progress", "resolved", "closed"];

  const handleChange = async (newStatus) => {
    if (newStatus === status) return;

    try {
      setUpdating(true);
      await updateIssueStatus(issueId, newStatus);
      onUpdated(); // reload issues
    } catch (err) {
      console.error(err);
      alert("Failed to update status");
    } finally {
      setUpdating(false);
    }
  };

  // 🔒 If user cannot update → show badge only
  if (!can("update_incident")) {
    return (
      <span
        className={`px-2 py-1 rounded text-sm font-medium capitalize ${
          statusStyles[status] || "bg-gray-100"
        }`}
      >
        {status.replace("_", " ")}
      </span>
    );
  }

  // ✅ Editable dropdown for authorized users
  return (
    <select
      value={status}
      disabled={updating}
      onChange={(e) => handleChange(e.target.value)}
      className={`px-2 py-1 rounded text-sm font-medium ${
        statusStyles[status] || ""
      }`}
    >
      {statuses.map((s) => (
        <option key={s} value={s}>
          {s.replace("_", " ")}
        </option>
      ))}
    </select>
  );
}