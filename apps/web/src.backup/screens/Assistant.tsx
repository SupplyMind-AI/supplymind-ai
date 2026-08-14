import {
  FormEvent,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import {
  Bot,
  CheckCircle2,
  Paperclip,
  Send,
  Sparkles,
  UserRound,
} from "lucide-react";
import { api } from "../api";
import {
  Card,
  Header,
  ToolActivity,
} from "../components";

type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  citations?: any[];
  confidence?: string;
};

const suggestions = [
  "Why is this shipment at risk?",
  "Which shipments have the highest delay probability?",
  "What external events could affect European deliveries?",
  "Which policy applies when a shipment is late?",
];

const activityTemplates = [
  {
    label: "Understanding request",
    detail: "Classifying the investigation and required evidence.",
  },
  {
    label: "Loading operational context",
    detail: "Checking shipment and saved prediction data.",
  },
  {
    label: "Checking external intelligence",
    detail: "Reviewing weather and disruption context when relevant.",
  },
  {
    label: "Searching enterprise knowledge",
    detail: "Retrieving semantically relevant policies and documents.",
  },
  {
    label: "Synthesizing grounded answer",
    detail: "Combining evidence into an operational recommendation.",
  },
];

export default function Assistant() {
  const [shipmentId, setShipmentId] = useState("TEST-BERLIN-001");
  const [question, setQuestion] = useState(
    "Why is this shipment at risk?",
  );
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "I’m SupplyMind’s operations intelligence assistant. I can investigate shipment risk using operational data, ML predictions, external disruption intelligence and enterprise knowledge.",
    },
  ]);
  const [loading, setLoading] = useState(false);
  const [stepIndex, setStepIndex] = useState(-1);
  const [elapsed, setElapsed] = useState(0);
  const timerRef = useRef<number | null>(null);

  useEffect(() => {
    if (!loading) return;

    const start = performance.now();

    timerRef.current = window.setInterval(() => {
      const seconds = (performance.now() - start) / 1000;
      setElapsed(seconds);

      const index = Math.min(
        activityTemplates.length - 1,
        Math.floor(seconds / 1.1),
      );
      setStepIndex(index);
    }, 100);

    return () => {
      if (timerRef.current) {
        window.clearInterval(timerRef.current);
      }
    };
  }, [loading]);

  const steps = useMemo(
    () =>
      activityTemplates.map((item, index) => ({
        ...item,
        state:
          !loading && stepIndex >= activityTemplates.length - 1
            ? ("done" as const)
            : index < stepIndex
              ? ("done" as const)
              : index === stepIndex
                ? ("active" as const)
                : ("waiting" as const),
      })),
    [loading, stepIndex],
  );

  async function submit(event?: FormEvent) {
    event?.preventDefault();
    if (!question.trim() || loading) return;

    const currentQuestion = question.trim();
    setMessages((current) => [
      ...current,
      {
        id: crypto.randomUUID(),
        role: "user",
        content: currentQuestion,
      },
    ]);
    setQuestion("");
    setLoading(true);
    setStepIndex(0);
    setElapsed(0);

    try {
      const response = await api<any>("/assistant", {
        method: "POST",
        body: JSON.stringify({
          shipment_id: shipmentId || null,
          question: currentQuestion,
          message: currentQuestion,
        }),
      });

      setStepIndex(activityTemplates.length - 1);

      setMessages((current) => [
        ...current,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content:
            response.answer ??
            response.response ??
            response.message ??
            JSON.stringify(response, null, 2),
          citations:
            response.citations ??
            response.sources ??
            [],
          confidence:
            response.confidence ??
            response.confidence_level,
        },
      ]);
    } catch (caught) {
      setMessages((current) => [
        ...current,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content:
            `I couldn't complete that investigation. ${String(caught)}`,
        },
      ]);
    } finally {
      setLoading(false);
      setStepIndex(activityTemplates.length - 1);
    }
  }

  return (
    <>
      <Header
        eyebrow="LANGGRAPH · GROUNDED INVESTIGATION"
        title="AI Assistant"
        subtitle="Investigate shipment risk using operational data, ML inference, disruptions and enterprise knowledge."
      />

      <div className="assistant-layout">
        <div className="assistant-main">
          <Card className="chat-card">
            <div className="chat-header">
              <div>
                <div className="bot-avatar">
                  <Bot size={20} />
                </div>
                <div>
                  <b>SupplyMind Intelligence</b>
                  <span>
                    <span className="dot" /> LangGraph coordinator online
                  </span>
                </div>
              </div>
              <span className="model-pill">Grounded AI</span>
            </div>

            <div className="chat-context-bar">
              <span>Shipment context</span>
              <input
                value={shipmentId}
                onChange={(e) => setShipmentId(e.target.value)}
                placeholder="Optional shipment ID"
              />
            </div>

            <div className="chat-messages">
              {messages.map((message) => (
                <div
                  className={`chat-message ${message.role}`}
                  key={message.id}
                >
                  <div className="chat-avatar">
                    {message.role === "assistant" ? (
                      <Sparkles size={16} />
                    ) : (
                      <UserRound size={16} />
                    )}
                  </div>
                  <div className="chat-bubble">
                    <div className="chat-role">
                      {message.role === "assistant"
                        ? "SupplyMind"
                        : "You"}
                    </div>
                    <div className="chat-content">
                      {message.content}
                    </div>
                    {message.confidence && (
                      <span className="confidence-chip">
                        Confidence · {message.confidence}
                      </span>
                    )}
                    {message.citations &&
                      message.citations.length > 0 && (
                        <div className="source-chips">
                          {message.citations
                            .slice(0, 6)
                            .map((source: any, index: number) => (
                              <span key={index}>
                                <CheckCircle2 size={11} />
                                {source.title ??
                                  source.name ??
                                  source.source ??
                                  `Source ${index + 1}`}
                              </span>
                            ))}
                        </div>
                      )}
                  </div>
                </div>
              ))}

              {loading && (
                <div className="chat-message assistant">
                  <div className="chat-avatar">
                    <Sparkles size={16} />
                  </div>
                  <div className="typing-bubble">
                    <span />
                    <span />
                    <span />
                  </div>
                </div>
              )}
            </div>

            <div className="suggestions">
              {suggestions.map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => setQuestion(suggestion)}
                >
                  {suggestion}
                </button>
              ))}
            </div>

            <form className="chat-composer" onSubmit={submit}>
              <button type="button" className="composer-icon">
                <Paperclip size={17} />
              </button>
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask SupplyMind about shipments, risk, disruptions or policies…"
                rows={2}
              />
              <button
                className="send-button"
                type="submit"
                disabled={loading}
              >
                <Send size={17} />
              </button>
            </form>
          </Card>
        </div>

        <div className="assistant-side">
          <ToolActivity
            steps={steps}
            elapsed={elapsed}
            active={loading}
          />

          <Card>
            <div className="assistant-side-note">
              <Sparkles size={18} />
              <div>
                <b>Evidence-first answers</b>
                <p>
                  Responses are designed to combine saved shipment data,
                  predictions, weather, external events and retrieved
                  enterprise knowledge.
                </p>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </>
  );
}
