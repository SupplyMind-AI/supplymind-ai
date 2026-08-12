const BASE=import.meta.env.VITE_API_BASE_URL??"http://localhost:8000/api";
export async function api<T>(path:string,init?:RequestInit):Promise<T>{const r=await fetch(`${BASE}${path}`,{...init,headers:{"Content-Type":"application/json",...(init?.headers??{})}});if(!r.ok)throw new Error(await r.text());return r.json() as Promise<T>}
