import type{ReactNode}from"react";
export function Header({title,subtitle,action}:{title:string;subtitle:string;action?:ReactNode}){return <header className="header"><div><h1>{title}</h1><p>{subtitle}</p></div>{action}</header>}
export function Card({children,className=""}:{children:ReactNode;className?:string}){return <section className={`card ${className}`}>{children}</section>}
export function Metric({label,value,delta}:{label:string;value:any;delta?:string}){return <Card className="metric"><span>{label}</span><strong>{value}</strong>{delta&&<small>{delta}</small>}</Card>}
export function RiskBadge({level}:{level:string}){return <span className={`badge ${level}`}>{level}</span>}
export function Empty({children}:{children:ReactNode}){return <div className="empty">{children}</div>}
