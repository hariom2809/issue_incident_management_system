import api from "./axios";

// GET all issues
export const getIssues = async () => {
  const res = await api.get("/issues/");
  return res.data;
};

// CREATE issue
export const createIssue = async (issueData) => {
  const params = new URLSearchParams(issueData);
  const res = await api.post(`/issues/?${params}`);
  return res.data;
};

// UPDATE issue status
export const updateIssueStatus = async (issueId, status) => {
  const params = new URLSearchParams({ status });
  const res = await api.patch(`/issues/${issueId}?${params}`);
  return res.data;
};

// GET current user permissions
export const getMe = async () => {
  const res = await api.get("/issues/me");
  return res.data;
};

// ASSIGN issue
export const assignIssue = async (issueId, assigned_user_id) => {
  const params = new URLSearchParams({ assigned_user_id });

  const res = await api.patch(`/issues/${issueId}/assign?${params}`);
  return res.data;
};