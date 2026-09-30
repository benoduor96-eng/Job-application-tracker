import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
  timeout: 15000,
});

export async function getReportingDashboard() {
  const { data } = await api.get("/reports/dashboard/");
  return data;
}

export async function getInterviewPreparation(applicationId) {
  const { data } = await api.get(
    `/applications/${applicationId}/interview-preparation/`,
  );
  return data;
}

export async function getFollowUpSequence(applicationId) {
  const { data } = await api.get(
    `/applications/${applicationId}/follow-up-sequence/`,
  );
  return data;
}

export async function createFollowUpSequence(applicationId) {
  const { data } = await api.post(
    `/applications/${applicationId}/follow-up-sequence/`,
  );
  return data;
}

export function percentage(value) {
  return `${Number(value || 0).toFixed(1)}%`;
}
