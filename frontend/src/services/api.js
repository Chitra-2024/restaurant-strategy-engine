const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function buildPayload({ restaurant_name, location, days }) {
  const payload = {};

  if (restaurant_name?.trim()) {
    payload.restaurant_name = restaurant_name.trim();
  }

  if (location?.trim()) {
    payload.location = location.trim();
  }

  if (days) {
    payload.days = Number(days);
  }

  return payload;
}

export async function fetchStrategy(filters) {
  const response = await fetch(`${API_BASE_URL}/strategy`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(buildPayload(filters)),
  });

  if (!response.ok) {
    throw new Error(`Strategy request failed with status ${response.status}`);
  }

  return response.json();
}

export async function fetchReviewFeed(filters) {
  const payload = buildPayload(filters);
  const params = new URLSearchParams();

  Object.entries(payload).forEach(([key, value]) => {
    params.set(key, String(value));
  });
  params.set("limit", "8");

  const response = await fetch(`${API_BASE_URL}/reviews?${params.toString()}`);

  if (!response.ok) {
    throw new Error(`Review request failed with status ${response.status}`);
  }

  return response.json();
}

export function getExportPdfUrl(filters) {
  const payload = buildPayload(filters);
  const params = new URLSearchParams();

  Object.entries(payload).forEach(([key, value]) => {
    params.set(key, String(value));
  });

  const query = params.toString();
  return `${API_BASE_URL}/export-pdf${query ? `?${query}` : ""}`;
}
