import StatusBadge from "./StatusBadge";

export default function IssuesTable({ issues, loading, onRefresh }) {
  if (loading) {
    return (
      <div className="bg-white p-6 rounded shadow">
        <p>Loading incidents...</p>
      </div>
    );
  }

  if (!issues.length) {
    return (
      <div className="bg-white p-6 rounded shadow">
        <p>No incidents found.</p>
      </div>
    );
  }

  return (
    <table className="w-full border bg-white shadow rounded">
      <thead className="bg-gray-200">
        <tr>
          <th className="p-2 border text-left">Title</th>
          <th className="p-2 border text-left">Priority</th>
          <th className="p-2 border text-left">Status</th>
          <th className="p-2 border text-left">Created By</th>
          <th className="p-2 border text-left">Assigned To</th>
        </tr>
      </thead>

      <tbody>
        {issues.map((issue) => (
          <tr key={issue.id} className="hover:bg-gray-50">
            <td className="p-2 border">{issue.title}</td>

            <td className="p-2 border capitalize">{issue.priority}</td>

            <td className="p-2 border">
              <StatusBadge
                status={issue.status}
                issueId={issue.id}
                onUpdated={onRefresh}
              />
            </td>

            <td className="p-2 border">{issue.created_by?.username || "—"}</td>

            <td className="p-2 border">
              {issue.assigned_to?.username || "Unassigned"}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
