const s = document.createElement("style");
s.textContent = `
.model-card-panel{margin-top:28px;padding:28px;border:1px solid rgba(255,255,255,.075);border-radius:24px;background:linear-gradient(135deg,rgba(17,25,37,.94),rgba(13,19,29,.94));box-shadow:0 16px 40px rgba(0,0,0,.18)}
.model-meta-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:24px}
.model-meta-grid>div{padding:18px;border:1px solid rgba(255,255,255,.07);border-radius:16px;background:rgba(255,255,255,.025)}
.model-meta-grid span{display:block;font-size:10px;letter-spacing:.12em;color:#5e6a7d;margin-bottom:8px}
.model-meta-grid strong{display:block;font-size:14px;line-height:1.4;color:#f4f7fb}
@media(max-width:900px){.model-meta-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:560px){.model-meta-grid{grid-template-columns:1fr}}
`;
document.head.appendChild(s);
