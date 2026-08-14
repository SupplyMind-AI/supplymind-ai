import { FormEvent, useState } from "react";
import { BookOpen, Database, Search, Sparkles } from "lucide-react";
import { motion } from "framer-motion";
import { api } from "../api";
import { AsyncButton, Card, Header, SectionTitle } from "../components";

export default function RagExplorer() {
  const [query, setQuery] = useState("What should operations do when a high-risk shipment is likely to be delayed?");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    setLoading(true); setError(""); setResult(null);
    try {
      setResult(await api<any>("/rag/query", { method: "POST", body: JSON.stringify({ query, top_k: 5 }) }));
    } catch (caught) { setError(String(caught)); }
    finally { setLoading(false); }
  }

  return <>
    <Header eyebrow="RAG · PINECONE · GROUNDED ANSWERS" title="RAG Explorer" subtitle="Retrieve enterprise evidence and generate a grounded answer with visible source chunks." />
    <Card className="rag-query-card">
      <form className="search-command" onSubmit={submit}>
        <Search size={20}/><input value={query} onChange={e=>setQuery(e.target.value)} />
        <AsyncButton loading={loading} loadingText="Retrieving" className="primary"><Sparkles size={16}/> Run RAG</AsyncButton>
      </form>
      {loading && <div className="rag-pipeline">
        {["Embed question","Search Pinecone","Rank evidence","Generate grounded answer"].map((x,i)=><motion.div key={x} animate={{opacity:[.35,1,.35]}} transition={{duration:1.2,repeat:Infinity,delay:i*.15}}><span>{i+1}</span>{x}</motion.div>)}
      </div>}
      {error && <div className="error">{error}</div>}
    </Card>

    {result && <div className="rag-grid">
      <Card className="rag-answer"><SectionTitle title="Grounded answer" subtitle={result.grounded ? `${result.evidence?.length ?? 0} retrieved evidence chunks` : "No supporting evidence found"} action={<Sparkles size={18}/>}/><p>{result.answer}</p></Card>
      <Card><SectionTitle title="Retrieval evidence" subtitle="Source chunks ranked by semantic similarity" action={<Database size={18}/>}/>
        <div className="rag-evidence-list">{(result.evidence ?? []).map((hit:any,index:number)=><article key={hit.id ?? index} className="rag-evidence">
          <div className="rag-evidence-head"><span>{String(index+1).padStart(2,"0")}</span><div><b>{hit.metadata?.filename ?? hit.metadata?.title ?? "Enterprise source"}</b><small>{Math.round(Number(hit.score ?? 0)*100)}% semantic match</small></div><BookOpen size={16}/></div>
          <p>{hit.text}</p><div className="similarity-track"><span style={{width:`${Math.max(5,Number(hit.score ?? 0)*100)}%`}}/></div>
        </article>)}</div>
      </Card>
    </div>}
  </>;
}
