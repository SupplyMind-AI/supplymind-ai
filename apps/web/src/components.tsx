import type { ReactNode } from "react";
export function Header({title,subtitle,action}:{title:string;subtitle:string;action?:ReactNode}){return <header className="screen-header"><div><h1>{title}</h1><p>{subtitle}</p></div>{action}</header>}
export function Card({children}:{children:ReactNode}){return <section className="card">{children}</section>}
export function Metric({label,value}:{label:string;value:string|number}){return <Card><span className="metric-label">{label}</span><strong className="metric-value">{value}</strong></Card>}
