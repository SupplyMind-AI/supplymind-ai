const API_BASE =
  import.meta.env.VITE_API_BASE_URL ??
  "http://localhost:8000/api";

export async function api<T = any>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(
      body || `${response.status} ${response.statusText}`,
    );
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export async function safeApi<T>(
  path: string,
  fallback: T,
): Promise<T> {
  try {
    return await api<T>(path);
  } catch {
    return fallback;
  }
}

export function getApiBase() {
  return API_BASE;
}
