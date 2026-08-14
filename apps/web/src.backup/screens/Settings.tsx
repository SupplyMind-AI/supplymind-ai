import { useEffect, useState } from "react";
import {
  Bot,
  CloudSun,
  Database,
  Globe2,
  Network,
  Search,
  Sparkles,
} from "lucide-react";
import { safeApi } from "../api";
import {
  Card,
  Header,
  SectionTitle,
  StatusLine,
} from "../components";

const integrations = [
  {
    key: "postgresql",
    title: "PostgreSQL",
    description: "Operational shipments, predictions and monitoring",
    icon: Database,
  },
  {
    key: "pinecone",
    title: "Pinecone Vector DB",
    description: "Enterprise knowledge and semantic retrieval",
    icon: Search,
  },
  {
    key: "open_meteo",
    title: "Open-Meteo",
    description: "Route weather intelligence",
    icon: CloudSun,
  },
  {
    key: "gdelt",
    title: "GDELT",
    description: "Global disruption intelligence",
    icon: Globe2,
  },
  {
    key: "openai",
    title: "OpenAI",
    description: "Assistant reasoning and structured extraction",
    icon: Bot,
  },
  {
    key: "langsmith",
    title: "LangSmith",
    description: "Tracing and AI workflow observability",
    icon: Network,
  },
];

export default function Settings() {
  const [settings, setSettings] = useState<any>({});

  useEffect(() => {
    void safeApi<any>("/settings", {}).then(setSettings);
  }, []);

  return (
    <>
      <Header
        eyebrow="ADMIN · READ ONLY"
        title="Integrations & System"
        subtitle="Production configuration, integration health and active model metadata. Secrets are never exposed."
      />

      <div className="integration-grid">
        {integrations.map((item) => {
          const Icon = item.icon;
          const configured =
            settings[item.key]?.configured ??
            settings[item.key]?.connected ??
            true;

          return (
            <Card className="integration-card" key={item.key}>
              <div className="integration-card-head">
                <div className="integration-card-icon">
                  <Icon size={20} />
                </div>
                <span className={`health ${configured ? "ok" : "warn"}`}>
                  {configured ? "Connected" : "Check"}
                </span>
              </div>
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </Card>
          );
        })}
      </div>

      <div className="grid2">
        <Card>
          <SectionTitle
            title="Environment"
            subtitle="Production metadata"
          />
          <StatusLine
            label="Environment"
            value={settings.environment ?? "production"}
          />
          <StatusLine
            label="LLM model"
            value={settings.llm_model ?? "Configured"}
          />
          <StatusLine
            label="Embedding model"
            value={settings.embedding_model ?? "text-embedding-3-small"}
          />
          <StatusLine
            label="Active ML model"
            value={settings.active_model ?? "Champion"}
          />
        </Card>

        <Card>
          <SectionTitle
            title="Architecture"
            subtitle="Current V1 runtime"
            action={<Sparkles size={18} />}
          />
          <div className="architecture-stack">
            <span>React / Vercel</span>
            <i>↓</i>
            <span>FastAPI / Render</span>
            <i>↓</i>
            <span>PostgreSQL · Pinecone · External Intelligence</span>
          </div>
        </Card>
      </div>
    </>
  );
}
