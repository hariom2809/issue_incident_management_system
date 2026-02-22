import { useState } from "react";
import { assignIssue } from "../../api/issues";
import usePermissions from "../../hooks/usePermissions";

export default function AssignUserSelect({
  issueId,
  assignedUser,
  users = [],
  onUpdated,
}) {
  const { can } = usePermissions();
  const [loading, setLoading] = useState(false);

  // 🔒 RBAC — read-only view
  if (!can("assign_incident")) {
    return <span>{assignedUser?.username || "Unassigned"}</span>;
  }

  const handleAssign = async (userId) => {
    try {
      setLoading(true);
      await assignIssue(issueId, userId);
      onUpdated();
    } catch (err) {
      console.error(err);
      alert("Assignment failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <select
      disabled={loading}
      value={assignedUser?.id || ""}
      onChange={(e) => handleAssign(e.target.value)}
      className="border p-1 rounded"
    >
      <option value="">Unassigned</option>

      {users.map((user) => (
        <option key={user.id} value={user.id}>
          {user.username}
        </option>
      ))}
    </select>
  );
}