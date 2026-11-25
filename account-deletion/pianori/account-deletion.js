"use strict";
const CONFIG={"supabaseUrl":"https://thoblvgpiodvdyqfribv.supabase.co","anonKey":"sb_publishable_RR_4Ml7lmRjHKv7stNXv6w_vjKdyGZ1","pageUrl":"https://develophil.github.io/account-deletion/pianori/","kakaoBase":"https://thoblvgpiodvdyqfribv.supabase.co/functions/v1/kakao-login"};
const byId=(id)=>document.getElementById(id);
const statusBox=byId("status");
const PENDING_KEY="pianori_deletion_request";
let accessToken=null;
let accountSubject=null;
let accountLabel=null;

function setStatus(message,kind=""){
  statusBox.textContent=message;
  statusBox.className="status"+(kind?" "+kind:"");
}
function updateControls(){
  const signedIn=Boolean(accessToken&&accountSubject);
  byId("logout").classList.toggle("hidden",!signedIn);
  byId("delete").disabled=!signedIn||!byId("confirm").checked;
  if(signedIn)setStatus("인증 계정: "+accountLabel+"\n본인 인증이 완료되었습니다. 삭제 범위를 확인하세요. · Verified account. Review the deletion scope.","ok");
}
function base64Url(bytes){
  let binary="";for(const b of bytes)binary+=String.fromCharCode(b);
  return btoa(binary).replace(/\+/g,"-").replace(/\//g,"_").replace(/=+$/g,"");
}
async function sha256(value){
  return base64Url(new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(value))));
}
function randomVerifier(){const bytes=new Uint8Array(32);crypto.getRandomValues(bytes);return base64Url(bytes);}
function tokenPayload(token){
  try{
    const part=token.split(".")[1];if(!part)return null;
    const normalized=part.replace(/-/g,"+").replace(/_/g,"/");
    const padded=normalized+"=".repeat((4-normalized.length%4)%4);
    const bytes=Uint8Array.from(atob(padded),(char)=>char.charCodeAt(0));
    return JSON.parse(new TextDecoder().decode(bytes));
  }catch(_){return null;}
}
function subjectFromToken(token){
  const payload=tokenPayload(token);
  return payload&&typeof payload.sub==="string"&&payload.sub.length>0?payload.sub:null;
}
function labelFromToken(token){
  const payload=tokenPayload(token)||{};
  const metadata=payload.user_metadata||{};
  const provider=metadata.provider||payload.app_metadata?.provider;
  if(provider==="kakao"||String(payload.email||"").endsWith("@kakao.local")){
    const nickname=typeof metadata.nickname==="string"?metadata.nickname.trim():"";
    return nickname?"Kakao · "+nickname:"Kakao 계정";
  }
  const email=typeof payload.email==="string"?payload.email:"";
  const at=email.indexOf("@");
  if(at>0){
    const local=email.slice(0,at);const domain=email.slice(at+1);
    return "Google · "+local.slice(0,Math.min(2,local.length))+"***@"+domain;
  }
  return "Google 계정";
}
function loadPending(){
  try{
    const value=JSON.parse(localStorage.getItem(PENDING_KEY)||"null");
    if(value&&typeof value.requestId==="string"&&typeof value.subject==="string")return value;
  }catch(_){}
  return null;
}
function savePending(requestId,subject){
  localStorage.setItem(PENDING_KEY,JSON.stringify({requestId,subject}));
}
async function api(path,options={}){
  const headers=new Headers(options.headers||{});headers.set("apikey",CONFIG.anonKey);
  const response=await fetch(CONFIG.supabaseUrl+path,{...options,headers});
  let data=null;try{data=await response.json();}catch(_){data=null;}
  if(!response.ok)throw new Error("request_failed");return data;
}
function clearAddress(){history.replaceState(null,"",CONFIG.pageUrl);}

async function startGoogle(){
  const verifier=randomVerifier();
  sessionStorage.setItem("pianori_google_verifier",verifier);
  const challenge=await sha256(verifier);
  const url=new URL(CONFIG.supabaseUrl+"/auth/v1/authorize");
  url.searchParams.set("provider","google");
  url.searchParams.set("redirect_to",CONFIG.pageUrl);
  url.searchParams.set("code_challenge",challenge);
  url.searchParams.set("code_challenge_method","s256");
  location.assign(url.toString());
}
async function finishGoogle(code){
  const verifier=sessionStorage.getItem("pianori_google_verifier");
  sessionStorage.removeItem("pianori_google_verifier");
  clearAddress();
  if(!verifier)throw new Error("login_expired");
  const data=await api("/auth/v1/token?grant_type=pkce",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({auth_code:code,code_verifier:verifier})});
  if(!data||typeof data.access_token!=="string")throw new Error("login_failed");
  accessToken=data.access_token;
  accountSubject=subjectFromToken(accessToken);
  accountLabel=labelFromToken(accessToken);
  if(!accountSubject){accessToken=null;throw new Error("login_failed");}
}
async function startKakao(){
  const data=await api("/functions/v1/kakao-login/prepare",{method:"POST",headers:{"Content-Type":"application/json","Authorization":"Bearer "+CONFIG.anonKey},body:JSON.stringify({channel:"web"})});
  if(!data||typeof data.transaction!=="string"||typeof data.verifier!=="string")throw new Error("login_failed");
  sessionStorage.setItem("pianori_kakao_proof",JSON.stringify({transaction:data.transaction,verifier:data.verifier}));
  location.assign(CONFIG.kakaoBase+"/start?transaction="+encodeURIComponent(data.transaction));
}
async function finishKakao(transaction,code){
  const raw=sessionStorage.getItem("pianori_kakao_proof");
  sessionStorage.removeItem("pianori_kakao_proof");
  clearAddress();
  if(!raw)throw new Error("login_expired");
  const proof=JSON.parse(raw);
  if(proof.transaction!==transaction||typeof proof.verifier!=="string")throw new Error("login_failed");
  const data=await api("/functions/v1/kakao-login/exchange",{method:"POST",headers:{"Content-Type":"application/json","Authorization":"Bearer "+CONFIG.anonKey},body:JSON.stringify({transaction,code,verifier:proof.verifier})});
  if(!data||typeof data.access_token!=="string"||Object.hasOwn(data,"refresh_token"))throw new Error("login_failed");
  accessToken=data.access_token;
  accountSubject=subjectFromToken(accessToken);
  accountLabel=labelFromToken(accessToken);
  if(!accountSubject){accessToken=null;throw new Error("login_failed");}
}
async function deletionStatus(requestId){
  return await api("/rest/v1/rpc/get_account_deletion_status",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({p_request_id:requestId})});
}
function showReceipt(data){
  localStorage.removeItem(PENDING_KEY);accessToken=null;accountSubject=null;accountLabel=null;updateControls();
  statusBox.className="status ok receipt";
  statusBox.textContent="삭제 완료 · Deletion complete\n"+data.request_id+"\n"+data.completed_at;
}
async function recoverReceipt(){
  const pending=loadPending();if(!pending)return false;
  try{const data=await deletionStatus(pending.requestId);if(data&&data.completed_at){showReceipt(data);return true;}}catch(_){}
  return false;
}
async function deleteAccount(){
  if(window.top!==window.self||!accessToken||!accountSubject||!byId("confirm").checked)return;
  const pending=loadPending();
  const requestId=pending&&pending.subject===accountSubject?pending.requestId:crypto.randomUUID();
  savePending(requestId,accountSubject);
  byId("delete").disabled=true;setStatus("삭제 처리 중… · Deleting…");
  try{
    const data=await api("/rest/v1/rpc/delete_my_account",{method:"POST",headers:{"Content-Type":"application/json","Authorization":"Bearer "+accessToken},body:JSON.stringify({p_request_id:requestId})});
    showReceipt(data);
  }catch(_){
    if(!await recoverReceipt())setStatus("삭제를 완료하지 못했습니다. 다시 인증한 뒤 재시도해주세요. · Deletion was not completed. Verify again and retry.","error");
  }
}
async function boot(){
  const query=new URLSearchParams(location.search);const fragment=new URLSearchParams(location.hash.slice(1));
  const googleCode=query.get("code");const transaction=fragment.get("transaction");const kakaoCode=fragment.get("kakao_code");const kakaoError=fragment.get("kakao_error");
  if(query.size||fragment.size)clearAddress();
  try{
    if(googleCode)await finishGoogle(googleCode);
    else if(transaction&&kakaoCode)await finishKakao(transaction,kakaoCode);
    else if(kakaoError)throw new Error("login_cancelled");
  }catch(_){setStatus("본인 인증에 실패했습니다. 다시 시도해주세요. · Verification failed. Try again.","error");}
  updateControls();await recoverReceipt();
}
if (window.top !== window.self) {
  clearAddress();
  setStatus("이 화면은 독립된 창에서 열어주세요. · Open this page in a separate window.", "error");
} else {
byId("google").addEventListener("click",()=>startGoogle().catch(()=>setStatus("Google 인증을 시작하지 못했습니다. · Could not start Google verification.","error")));
byId("kakao").addEventListener("click",()=>startKakao().catch(()=>setStatus("카카오 인증을 시작하지 못했습니다. · Could not start Kakao verification.","error")));
byId("logout").addEventListener("click",()=>{accessToken=null;accountSubject=null;accountLabel=null;byId("confirm").checked=false;updateControls();setStatus("다른 계정으로 인증해주세요. · Verify another account.");});
byId("confirm").addEventListener("change",updateControls);
byId("delete").addEventListener("click",deleteAccount);
boot();
}
