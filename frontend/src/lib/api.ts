const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function fetchAPI(endpoint: string, options?: RequestInit) {
  return fetch(`${BASE_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });
}

export function sendMessage(message: string) {
  return fetchAPI("/api/chat", {
    method: "POST",
    body: JSON.stringify({ message }),
  });
}

export function getServices() {
  return fetchAPI("/api/services");
}

export function getContainers() {
  return fetchAPI("/api/containers");
}

export function getDeployments() {
  return fetchAPI("/api/deployments");
}

export function getLogs() {
  return fetchAPI("/api/logs");
}
