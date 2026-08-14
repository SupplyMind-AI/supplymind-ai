import { FormEvent, useMemo, useState } from "react";
import {
  BookOpen,
  ChevronDown,
  ChevronUp,
  FileText,
  Search as SearchIcon,
  Sparkles,
} from "lucide-react";
import { api } from "../api";
import {
  AsyncButton,
  Card,
  Header,
  SectionTitle,
} from "../components";

function cleanExcerpt(result: any) {
  const raw =
    result.excerpt ??
    result.text ??
    result.content ??
    result.page_content ??
    "";

  return String(raw)
    .replace(/\s+/g, " ")
    .replace(/---+/g, " ")
    .trim();
}

export default function Search() {
  const [query, setQuery] = useState(
    "What is the escalation policy for shipment delays?",
  );
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [expanded, setExpanded] = useState<number | null>(null);

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

  const displayResults = useMemo(
    () =>
      results.map((result, index) => ({
        ...result,
        rank: index + 1,
        title:
          result.title ??
          result.document_title ??
          result.metadata?.title ??
          result.source ??
          `Knowledge source ${index + 1}`,
        score: Number(
          result.score ??
            result.similarity_score ??
            result.similarity ??
            0,
        ),
        excerpt: cleanExcerpt(result),
        source:
          result.source ??
          result.metadata?.source ??
          result.metadata?.filename ??
          "Enterprise knowledge",
      })),
    [results],
  );

  return (
    <>
      <Header
        eyebrow="PINECONE · ENTERPRISE KNOWLEDGE"
        title="Semantic Search"
        subtitle="Find policies, SLAs, incident reports and operating procedures by meaning, not keywords."
      />

      <Card className="search-hero">
        <form className="search-command" onSubmit={submit}>
          <SearchIcon size={21} />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search company knowledge…"
          />
          <AsyncButton
            loading={loading}
            loadingText="Searching"
            className="primary"
          >
            <Sparkles size={16} />
            Search knowledge
          </AsyncButton>
        </form>
        {error && <div className="error">{error}</div>}
      </Card>

      <div className="search-layout search-layout-fixed">
        <Card>
          <SectionTitle
            title="Knowledge results"
            subtitle={`${displayResults.length} semantically relevant sources`}
          />

          <div className="knowledge-results-v2">
            {displayResults.map((result, index) => {
              const isExpanded = expanded === index;
              const excerpt =
                isExpanded || result.excerpt.length <= 360
                  ? result.excerpt
                  : `${result.excerpt.slice(0, 360)}…`;

              return (
                <article
                  className="knowledge-card"
                  key={result.id ?? index}
                >
                  <div className="knowledge-rank">
                    {String(result.rank).padStart(2, "0")}
                  </div>

                  <div className="knowledge-main">
                    <div className="knowledge-card-head">
                      <div className="knowledge-title-wrap">
                        <div className="knowledge-icon">
                          <FileText size={19} />
                        </div>
                        <div>
                          <b>{result.title}</b>
                          <small>{result.source}</small>
                        </div>
                      </div>

                      <div className="similarity-score">
                        <span>Match</span>
                        <strong>{Math.round(result.score * 100)}%</strong>
                      </div>
                    </div>

                    <p className="knowledge-excerpt">{excerpt}</p>

                    <div className="knowledge-footer">
                      <div className="source-chips">
                        {result.type && <span>{result.type}</span>}
                        {result.metadata?.page && (
                          <span>Page {result.metadata.page}</span>
                        )}
                        <span>
                          <BookOpen size={12} />
                          Grounded source
                        </span>
                      </div>

                      {result.excerpt.length > 360 && (
                        <button
                          className="text-button"
                          onClick={() =>
                            setExpanded(isExpanded ? null : index)
                          }
                        >
                          {isExpanded ? (
                            <>
                              Collapse <ChevronUp size={14} />
                            </>
                          ) : (
                            <>
                              Read evidence <ChevronDown size={14} />
                            </>
                          )}
                        </button>
                      )}
                    </div>

                    <div className="similarity-track">
                      <span
                        style={{
                          width: `${Math.max(
                            8,
                            Math.min(100, result.score * 100),
                          )}%`,
                        }}
                      />
                    </div>
                  </div>
                </article>
              );
            })}

            {!displayResults.length && (
              <div className="premium-empty-state">
                <SearchIcon size={31} />
                <b>Search your enterprise knowledge</b>
                <p>
                  Ask about delay policies, SLAs, escalation,
                  disruptions or operating procedures.
                </p>
              </div>
            )}
          </div>
        </Card>

        <div className="search-side-panel semantic-helper-column">
          <Card>
            <span className="side-panel-kicker">HOW TO READ RESULTS</span>
            <h3>Evidence ranked by semantic similarity</h3>
            <p>
              Higher match scores indicate stronger semantic alignment
              with the question. The AI Assistant can combine these
              sources with shipment and model context.
            </p>
          </Card>

          <Card>
            <span className="side-panel-kicker">QUICK QUERIES</span>
            {[
              "When should a delay be escalated?",
              "What is the customer notification SLA?",
              "What should we do during severe weather?",
            ].map((item) => (
              <button
                className="quick-query"
                key={item}
                onClick={() => setQuery(item)}
              >
                {item}
              </button>
            ))}
          </Card>
        </div>
      </div>
    </>
  );
}
