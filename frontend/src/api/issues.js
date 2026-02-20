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