import { FormEvent, useState } from "react";
import { FileText, Search as SearchIcon, Sparkles } from "lucide-react";
import { api } from "../api";
import {
  Card,
  Header,
  SectionTitle,
} from "../components";

export default function Search() {
  const [query, setQuery] = useState(
    "What is the escalation policy for shipment delays?",
  );
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await api<any>("/search", {
        method: "POST",
        body: JSON.stringify({ query }),
      });

      setResults(
        Array.isArray(response)
          ? response
          : response.results ?? response.matches ?? [],
      );
    } catch (caught) {
      setError(String(caught));
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Header
        eyebrow="PINECONE · ENTERPRISE KNOWLEDGE"
        title="Semantic Search"
        subtitle="Find policies, SLAs, incident reports and operating procedures by meaning."
      />

      <Card className="search-hero">
        <form className="search-command" onSubmit={submit}>
          <SearchIcon size={19} />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search company knowledge…"
          />
          <button className="primary" disabled={loading}>
            <Sparkles size={15} />
            {loading ? "Searching…" : "Search knowledge"}
          </button>
        </form>
        {error && <div className="error">{error}</div>}
      </Card>

      <Card>
        <SectionTitle
          title="Knowledge results"
          subtitle={`${results.length} semantically relevant sources`}
        />

        <div className="knowledge-results">
          {results.map((result, index) => (
            <div className="knowledge-result" key={result.id ?? index}>
              <div className="knowledge-icon">
                <FileText size={18} />
              </div>
              <div>
                <div className="knowledge-result-head">
                  <b>
                    {result.title ??
                      result.document_title ??
                      result.source ??
                      `Document ${index + 1}`}
                  </b>
                  <span>
                    {Number(
                      result.score ??
                        result.similarity_score ??
                        result.similarity ??
                        0,
                    ).toFixed(2)}
                  </span>
                </div>
                <p>
                  {result.excerpt ??
                    result.text ??
                    result.content ??
                    result.page_content ??
                    "Relevant enterprise knowledge result."}
                </p>
                <div className="source-chips">
                  {result.type && <span>{result.type}</span>}
                  {result.source && <span>{result.source}</span>}
                  {result.metadata?.page && (
                    <span>Page {result.metadata.page}</span>
                  )}
                </div>
              </div>
            </div>
          ))}

          {!results.length && (
            <div className="table-empty">
              Run a semantic search to explore indexed knowledge.
            </div>
          )}
        </div>
      </Card>
    </>
  );
}
