const BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8001/api';
export function getToken(){return localStorage.getItem('sb_token') || '';}
export function setSession(token,user){localStorage.setItem('sb_token',token);localStorage.setItem('sb_user',JSON.stringify(user));}
export function clearSession(){localStorage.removeItem('sb_token');localStorage.removeItem('sb_user');}
export function getSavedUser(){try{return JSON.parse(localStorage.getItem('sb_user')||'null')}catch{return null}}
export async function api(path, options={}){
  const headers = new Headers(options.headers || {});
  if(getToken()) headers.set('Authorization',`Bearer ${getToken()}`);
  if(options.body && !(options.body instanceof FormData) && typeof options.body !== 'string') {headers.set('Content-Type','application/json'); options={...options,body:JSON.stringify(options.body)};}
  const res=await fetch(`${BASE}${path}`,{...options,headers});
  if(!res.ok){let message=`Request failed (${res.status})`;try{const d=await res.json();message=typeof d.detail==='string'?d.detail:message}catch{};throw new Error(message)}
  if(res.status===204)return null;
  const type=res.headers.get('content-type')||'';
  return type.includes('application/json')?res.json():res.blob();
}
