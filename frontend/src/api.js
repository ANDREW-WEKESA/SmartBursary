// API Base URL - uses environment variable or defaults to production backend
// Ensure /api is always included
const apiUrl = import.meta.env.VITE_API_URL || 'https://smartbursary-backend.onrender.com';
const BASE = apiUrl.endsWith('/api') ? apiUrl : `${apiUrl}/api`;

// Wake up backend on app load (for cold-start servers like Render free tier)
let backendWarmedUp = false;
async function warmUpBackend() {
  if (backendWarmedUp) return;
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 second timeout
    
    await fetch(`${apiUrl}/api/health`, {
      method: 'GET',
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);
    backendWarmedUp = true;
    console.log('✅ Backend is ready');
  } catch (e) {
    console.warn('Backend warmup attempt:', e.message);
    // Continue anyway - the actual API call will retry
  }
}

// Start warming up immediately
warmUpBackend();

export function getToken(){return localStorage.getItem('sb_token') || '';}
export function setSession(token,user){localStorage.setItem('sb_token',token);localStorage.setItem('sb_user',JSON.stringify(user));}
export function clearSession(){localStorage.removeItem('sb_token');localStorage.removeItem('sb_user');}
export function getSavedUser(){try{return JSON.parse(localStorage.getItem('sb_user')||'null')}catch{return null}}
export async function api(path, options={}){
  // Ensure backend is warm before making API calls
  if (!backendWarmedUp) {
    await warmUpBackend();
  }
  const headers = new Headers(options.headers || {});
  if(getToken()) headers.set('Authorization',`Bearer ${getToken()}`);
  if(options.body && !(options.body instanceof FormData) && typeof options.body !== 'string') {headers.set('Content-Type','application/json'); options={...options,body:JSON.stringify(options.body)};}
  const res=await fetch(`${BASE}${path}`,{...options,headers});
  if(!res.ok){let message=`Request failed (${res.status})`;try{const d=await res.json();message=typeof d.detail==='string'?d.detail:message}catch{};throw new Error(message)}
  if(res.status===204)return null;
  const type=res.headers.get('content-type')||'';
  return type.includes('application/json')?res.json():res.blob();
}
