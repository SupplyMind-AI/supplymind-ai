import { useEffect, useMemo, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import {
  AlertTriangle,
  BarChart3,
  Bot,
  BrainCircuit,
  FileBarChart2,
  Gauge,
  Globe2,
  LayoutDashboard,
  PackagePlus,
  Search,
  Settings,
  Sparkles,
} from "lucide-react";

import { ScreenProgress } from "./components";
import Dashboard from "./screens/Dashboard";
import Assistant from "./screens/Assistant";
import Prediction from "./screens/Prediction";
import Predictions from "./screens/Predictions";
import Alerts from "./screens/Alerts";
import Events from "./screens/Events";
import SearchScreen from "./screens/Search";
import Retraining from "./screens/Retraining";
import Monitoring from "./screens/Monitoring";
import SettingsScreen from "./screens/Settings";
import Reports from "./screens/Reports";

type Screen =
  | "dashboard"
  | "assistant"
  | "prediction"
  | "predictions"
  | "alerts"
  | "events"
  | "search"
  | "reports"
  | "monitoring"
  | "retraining"
  | "settings";

const groups = [
  {
    label: "INTELLIGENCE",
    items: [
      ["dashboard", "Command Center", LayoutDashboard],
      ["assistant", "AI Assistant", Bot],
      ["predictions", "Shipment Intelligence", BarChart3],
      ["events", "Event Monitor", Globe2],
      ["search", "Semantic Search", Search],
      ["reports", "Executive Brief", FileBarChart2],
    ],
  },
  {
    label: "OPERATIONS",
    items: [
      ["prediction", "Parcel Intake", PackagePlus],
      ["alerts", "Risk Alerts", AlertTriangle],
    ],
  },
  {
    label: "MLOPS & ADMIN",
    items: [
      ["monitoring", "Model Monitoring", Gauge],
      ["retraining", "Retraining Center", BrainCircuit],
      ["settings", "Integrations", Settings],
    ],
  },
] as const;

export default function App() {
  const [screen, setScreen] = useState<Screen>("dashboard");
  const [transitioning, setTransitioning] = useState(false);

  const navigate = (next: Screen) => {
    if (next === screen) return;
    setTransitioning(true);
    window.setTimeout(() => {
      setScreen(next);
      window.setTimeout(() => setTransitioning(false), 360);
    }, 120);
  };

  const content = useMemo(() => {
    switch (screen) {
      case "dashboard":
        return <Dashboard onNavigate={navigate} />;
      case "assistant":
        return <Assistant />;
      case "prediction":
        return <Prediction onAsk={() => navigate("assistant")} />;
      case "predictions":
        return <Predictions onOpenIntake={() => navigate("prediction")} />;
      case "alerts":
        return <Alerts />;
      case "events":
        return <Events />;
      case "search":
        return <SearchScreen />;
      case "reports":
        return <Reports />;
      case "monitoring":
        return <Monitoring />;
      case "retraining":
        return <Retraining />;
      case "settings":
        return <SettingsScreen />;
    }
  }, [screen]);

  return (
    <div className="shell">
      <ScreenProgress visible={transitioning} />

      <aside>
        <div className="brand">
          <div className="brand-mark">
            <Sparkles size={21} />
          </div>
          <div>
            <strong>
              SupplyMind <em>AI</em>
            </strong>
            <span>PREDICT · INSIGHT · DELIVER</span>
          </div>
        </div>

        <nav>
          {groups.map((group) => (
            <div className="nav-group" key={group.label}>
              <div className="nav-label">{group.label}</div>
              {group.items.map(([id, label, Icon]) => (
                <button
                  key={id}
                  className={screen === id ? "active" : ""}
                  onClick={() => navigate(id)}
                  title={label}
                >
                  <Icon size={17} />
                  <span>{label}</span>
                </button>
              ))}
            </div>
          ))}
        </nav>

        <div className="sidebar-foot">
          <span className="dot" />
          Production-ready V1
        </div>
      </aside>

      <main>
        <div className="topbar">
          <div className="searchbox">
            <Search size={16} />
            <span>Search SupplyMind</span>
            <kbd>⌘ K</kbd>
          </div>

          <div className="top-actions">
            <span className="status-pill">
              <span className="dot" /> Systems online
            </span>
            <div className="avatar">KM</div>
          </div>
        </div>

        <div className="page">
          <AnimatePresence mode="wait">
            <motion.div
              key={screen}
              initial={{ opacity: 0, y: 12, filter: "blur(4px)" }}
              animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
              exit={{ opacity: 0, y: -7, filter: "blur(3px)" }}
              transition={{ duration: 0.28, ease: [0.16, 1, 0.3, 1] }}
            >
              {content}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}
