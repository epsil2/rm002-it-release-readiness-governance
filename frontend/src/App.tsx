import { useEffect, useState } from "react";

type Health = { status: string; service: string };
type Item = { id: number; name: string };
type ItemList = { items: Item[] };

const API_BASE: string = import.meta.env.VITE_API_BASE_URL ?? "";

export default function App() {
  const [health, setHealth] = useState<Health | null>(null);
  const [items, setItems] = useState<Item[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function load(): Promise<void> {
      try {
        const [healthResponse, itemsResponse] = await Promise.all([
          fetch(`${API_BASE}/health`),
          fetch(`${API_BASE}/api/v1/items`),
        ]);
        if (!healthResponse.ok || !itemsResponse.ok) {
          throw new Error(
            `API responded with ${healthResponse.status}/${itemsResponse.status}`,
          );
        }
        const healthBody = (await healthResponse.json()) as Health;
        const itemsBody = (await itemsResponse.json()) as ItemList;
        if (!cancelled) {
          setHealth(healthBody);
          setItems(itemsBody.items);
          setError(null);
        }
      } catch (cause) {
        if (!cancelled) {
          setError(cause instanceof Error ? cause.message : "request failed");
        }
      }
    }

    void load();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <main>
      <h1>IT Release Readiness & Governance</h1>
      {error !== null && <p role="alert">{error}</p>}
      <p>
        API status: <strong>{health === null ? "unknown" : health.status}</strong>
      </p>
      <section>
        <h2>Items</h2>
        <ul>
          {items.map((item) => (
            <li key={item.id}>{item.name}</li>
          ))}
        </ul>
      </section>
    </main>
  );
}
