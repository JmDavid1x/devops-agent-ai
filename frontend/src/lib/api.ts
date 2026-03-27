const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const API_KEY = process.env.NEXT_PUBLIC_API_KEY ?? "";

async function fetchAPI(endpoint: string, options?: RequestInit) {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options?.headers as Record<string, string>),
  };
  if (API_KEY) {
    headers["X-API-Key"] = API_KEY;
  }
  return fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });
}

export interface ChatStreamEvent {
  type: "conversation_id" | "status" | "tools_used" | "content" | "done" | "error";
  data?: string | string[];
}

export function sendMessage(message: string, conversationId?: string) {
  return fetchAPI("/api/chat", {
    method: "POST",
    body: JSON.stringify({ message, conversation_id: conversationId }),
  });
}

export async function sendMessageStream(
  message: string,
  conversationId: string | null,
  onEvent: (event: ChatStreamEvent) => void,
) {
  const response = await fetchAPI("/api/chat/stream", {
    method: "POST",
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  const reader = response.body?.getReader();
  if (!reader) throw new Error("No response body");

  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";

    for (const line of lines) {
      if (line.startsWith("data: ")) {
        try {
          const event = JSON.parse(line.slice(6)) as ChatStreamEvent;
          onEvent(event);
        } catch {
          // skip malformed events
        }
      }
    }
  }
}

export function getConversations() {
  return fetchAPI("/api/conversations/");
}

export function getConversation(id: string) {
  return fetchAPI(`/api/conversations/${id}`);
}

export function deleteConversation(id: string) {
  return fetchAPI(`/api/conversations/${id}`, { method: "DELETE" });
}

export function getServices() {
  return fetchAPI("/api/services");
}

export function createService(data: { name: string; url: string; check_interval_seconds?: number; timeout_seconds?: number }) {
  return fetchAPI("/api/services", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function deleteService(id: string) {
  return fetchAPI(`/api/services/${id}`, { method: "DELETE" });
}

export function checkServiceNow(id: string) {
  return fetchAPI(`/api/services/${id}/check`, { method: "POST" });
}

export function getServiceHistory(id: string, limit: number = 20) {
  return fetchAPI(`/api/services/${id}/history?limit=${limit}`);
}

export function getContainers() {
  return fetchAPI("/api/docker/containers");
}

export function restartContainer(id: string) {
  return fetchAPI(`/api/docker/containers/${id}/restart`, { method: "POST" });
}

export function stopContainer(id: string) {
  return fetchAPI(`/api/docker/containers/${id}/stop`, { method: "POST" });
}

export function startContainer(id: string) {
  return fetchAPI(`/api/docker/containers/${id}/start`, { method: "POST" });
}

export function getContainerStats(id: string) {
  return fetchAPI(`/api/docker/containers/${id}/stats`);
}

export function getLogs() {
  return fetchAPI("/api/logs");
}
