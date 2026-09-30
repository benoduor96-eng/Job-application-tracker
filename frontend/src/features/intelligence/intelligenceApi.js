import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
  timeout: 15000,
});

export async function getCareerSummary() {
  const { data } = await api.get("/intelligence/summary/");
  return data;
}

export async function getPipelinePriority() {
  const { data } = await api.get("/intelligence/pipeline-priority/");
  return data.items || [];
}

export async function previewJobDescription(rawText) {
  const { data } = await api.post("/intelligence/descriptions/preview/", {
    raw_text: rawText,
  });
  return data;
}

export async function matchSkills(payload) {
  const { data } = await api.post("/intelligence/skill-match/advanced/", payload);
  return data;
}

export async function generateFollowUps(applicationIds = [], create = false) {
  const { data } = await api.post("/intelligence/follow-ups/", {
    application_ids: applicationIds,
    create,
  });
  return data;
}

export async function completeCareerTask(id) {
  const { data } = await api.post(
    `/intelligence/tasks/${id}/complete/`,
  );
  return data;
}

export async function listCareerTasks(params = {}) {
  const { data } = await api.get("/intelligence/tasks/", { params });
  return data;
}

export async function listJobDescriptions(params = {}) {
  const { data } = await api.get("/intelligence/descriptions/", { params });
  return data;
}

export async function createJobDescription(payload) {
  const { data } = await api.post("/intelligence/descriptions/", payload);
  return data;
}

export async function analyzeJobDescription(id) {
  const { data } = await api.post(
    `/intelligence/descriptions/${id}/analyze/`,
  );
  return data;
}

export async function getJobMatch(id) {
  const { data } = await api.get(
    `/intelligence/descriptions/${id}/match/`,
  );
  return data;
}

export async function getResumeTargeting(id) {
  const { data } = await api.get(
    `/intelligence/descriptions/${id}/resume_targeting/`,
  );
  return data;
}

export function formatScore(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "—";
  }
  return `${Number(value).toFixed(1)}%`;
}

export function scoreTone(value) {
  const score = Number(value);
  if (score >= 80) return "excellent";
  if (score >= 60) return "good";
  if (score >= 40) return "watch";
  return "low";
}
