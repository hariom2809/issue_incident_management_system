import { useEffect, useState } from "react";
import { getIssues } from "../api/issues";

import CreateIssueForm from "../components/issues/CreateIssueForm";
import IssuesTable from "../components/issues/IssuesTable";

export default function Incidents() {
  const [issues, setIssues] = useState([]);
  const [loading, setLoading] = useState(true);

  // Load issues from backend
  const loadIssues = async () => {
    try {
      setLoading(true);
      const data = await getIssues();
      setIssues(data);
    } catch (err) {
      console.error("Failed loading issues", err);
      alert("Failed to load incidents");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadIssues();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Incident Dashboard</h1>

      {/* Create Incident (RBAC handled internally) */}
      <CreateIssueForm onCreated={loadIssues} />

      {/* Issues List */}
      <IssuesTable issues={issues} loading={loading} onRefresh={loadIssues} />
    </div>
  );
}
