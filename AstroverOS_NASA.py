from dotenv import load_dotenv
load_dotenv()
from flask import Flask, jsonify, request, render_template_string
import os, requests, subprocess, sys, traceback
os.makedirs("/tmp/astroveros", exist_ok=True)
app = Flask(__name__)

GROQ_KEY = os.getenv("GROQ_API_KEY","")
NASA_KEY = os.getenv("NASA_API_KEY","DEMO_KEY")
LUSHI_LAT = -11.67
LUSHI_LON = 27.47

GROQ_MODELS = {
    "llama-3.3-70b-versatile": "🧠 70B",
    "llama-3.1-8b-instant": "⚡ 8B",
    "llama3-70b-8192": "🔥 70B Stable",
    "mixtral-8x7b-32768": "📚 Mixtral 32K",
    "gemma2-9b-it": "💎 Gemma2",
    "llama-3.2-90b-vision-preview": "👁️ 90B Vision",
    "llama-3.2-11b-vision-preview": "👁️ 11B Vision"
}

HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name=viewport content="width=device-width,initial-scale=1">
<title>AstroverOS V7 TITAN LANDING</title><script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
body{margin:0;background:#000;color:#e0e0e0;font-family:Arial;display:flex;flex-direction:column;height:100vh;overflow:hidden}
.top{background:#0a0a2a;padding:8px;border-bottom:3px solid #ff8c00;display:flex;gap:4px;flex-wrap:wrap;align-items:center}
.btn{background:#1e2142;color:#fff;border:1px solid #444;padding:6px 10px;border-radius:8px;cursor:pointer;font-size:10px}
.btn-gold{background:#ffaa00;color:#000;font-weight:bold}.btn-titan{background:#ff8c00;color:#000;font-weight:bold}.btn-teleport{background:#00ffff;color:#000;font-weight:bold;animation:blink 1s infinite}.btn-landing{background:#ff0044;color:#fff;font-weight:bold;font-size:12px;padding:10px 16px}
@keyframes blink{0%{opacity:1}50%{opacity:0.5}100%{opacity:1}}
.main{display:flex;flex:1;overflow:hidden}.sidebar{width:165px;background:#0d0f22;padding:8px;font-size:10px;overflow:auto}
.content{flex:1;overflow:auto;padding:8px;background:#020212}.module{display:none}.module.active{display:block}
.card{background:#10122a;border:1px solid #333;padding:10px;border-radius:10px;margin:6px 0}
.plot{width:100%;height:600px}.term{background:#000;color:#00ff88;padding:8px;height:140px;overflow:auto;white-space:pre-wrap;font-family:monospace;font-size:10px;border-radius:6px}
textarea,select,input{width:100%;background:#000;color:#0f0;border:1px solid #333;border-radius:6px;padding:6px;margin:3px 0}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px}.kpi{background:#1a1e40;padding:6px;border-radius:6px;text-align:center;border:1px solid #333;font-size:10px}
#teleportOverlay{position:fixed;top:0;left:0;width:100%;height:100%;background:linear-gradient(to bottom,#000,#220000);display:none;z-index:9999;align-items:center;justify-content:center;flex-direction:column}
.warp{width:2px;height:100px;background:#fff;position:absolute;animation:warp 0.1s linear infinite}
@keyframes warp{0%{transform:translateY(-100vh)}100%{transform:translateY(100vh)}}
.titan-lake{background:#001122;border:1px solid #ff8c00;padding:6px;border-radius:6px;margin:3px 0;font-size:10px}
</style></head><body>
<div id=teleportOverlay><h1 id=teleportText style="color:#ff8c00;font-size:28px">🛬 ATTERRISSAGE TITAN...</h1><div id=teleportDist style="color:#00ffff;font-size:12px">Entrée atmosphérique...</div><div id=warpContainer style="position:absolute;width:100%;height:100%;overflow:hidden"></div></div>

<div class=top><b style="color:#ff8c00">🪐 V7 TITAN</b> <b style="color:#ff0044">LANDING</b>
<button class=btn style="background:#ff8c00;color:#000" onclick="show('titan')">🛬 TITAN LANDING</button>
<button class=btn-galaxy style="background:#ff0044;color:#fff;border:1px solid #444;padding:6px 10px;border-radius:8px;cursor:pointer;font-size:10px" onclick="show('galaxy')">🌌 GALAXIE</button>
<button class=btn style="background:#0B3D91" onclick="show('solar')">☀️ SOLAIRE</button>
<button class=btn onclick="show('lunes')">🌙 LUNES</button>
<button class=btn style="background:#aa00ff" onclick="show('apod')">🖼️ VISION</button>
<button class=btn style="background:#0044aa" onclick="show('avia')">✈️ AVIA</button>
<button class=btn style="background:#006600" onclick="show('agri')">🌱 POWER</button>
<button class=btn style="background:#ffaa00;color:#000" onclick="show('ia')">🤖 6 GROQ</button>
<span style="margin-left:auto;color:#ff8c00;font-size:9px">TITAN -179°C</span></div>

<div class=main><div class=sidebar><b>🪐 V7 TITAN</b><br>
✅ Atterrissage<br>✅ Lacs méthane<br>✅ Kraken Mare<br>✅ Cycle pluie<br>✅ -179°C<br>✅ Atmo azote<br>✅ 5150km > Mercure<br>✅ 1.88 g/cm³<br><hr><b>🌊 LACS</b><div class=titan-lake><b>Kraken Mare</b><br>400k km²<br>> Mer Caspienne</div><div class=titan-lake><b>Ligeia Mare</b><br>126k km²<br>Méthane pur</div><div class=titan-lake><b>Punga Mare</b><br>61k km²<br>Nord</div><hr><b>🚀 TELEPORT</b><br>Vers Titan<br>1.2B km<br><hr>LUSHI</div><div class=content>

<div id=mod-titan class=module active><h2>🛬 ATTERRISSAGE TITAN - 5150km > Mercure - Lacs Méthane -179°C</h2>
<div class=card><div class=grid><div class=kpi><b>Titan</b><div>5150 km<br>1.88 g/cm³<br>Lune Saturne<br>> Mercure</div></div><div class=kpi><b>Atmosphère</b><div>Azote 98%<br>Méthane 1.4%<br>Pression 1.45 bar<br>Epaisse</div></div><div class=kpi><b>Temp</b><div>-179°C<br>Méthane liquide<br>Cycle eau<br>Pluie rivière lac</div></div></div>
<div class=grid><button class=btn-landing onclick="landingTitan()">🛬 LANCER ATTERRISSAGE HUYGENS 2005</button><button class=btn-titan onclick="plotTitan()">🗺️ CARTE LACS METHANE</button><button class=btn-teleport onclick="plotTitan3D()">🌊 3D KRAKEN MARE</button></div>
<div id=pTitan class=plot></div>
<div class=term id=tTitan>Sequence atterrissage Huygens: Entrée atmo 6km/s -> parachute 127km -> descente 2h30 -> atterrissage sol glace + méthane. Lacs: Kraken Mare 400k km² plus grand que mer Caspienne, Ligeia Mare 126k km² méthane pur. Cycle: évaporation méthane -> nuages -> pluie -> rivières -> lacs -> évaporation. Comme eau sur Terre mais à -179°C. Cassini-Huygens 2005.</div>
<div class=grid><div class=kpi><b>Pluie</b><div>Méthane<br>Nuages noirs<br>Orages</div></div><div class=kpi><b>Rivières</b><div>Méthane liquide<br>Vid Flumina<br>400 km</div></div><div class=kpi><b>Lacs</b><div>Kraken 400k km²<br>Ligeia 126k<br>Punga 61k</div></div></div>
</div></div>

<div id=mod-galaxy class=module><h2>🌌 Galaxie + Teleport vers Titan</h2><div class=card><button class=btn-galaxy style="background:#ff0044;color:#fff;padding:6px 10px;border-radius:8px" onclick="plotGalaxy()">🌌 Charger Galaxie</button><button class=btn-teleport onclick="enableTeleport()">🚀 Teleport</button><button class=btn-titan onclick="teleportToTitan()">🪐 TELEPORT DIRECT TITAN</button><div id=pGalaxy class=plot></div><div class=term id=tGalaxy></div></div></div>

<div id=mod-solar class=module><h2>☀️ Solaire</h2><div class=card><button class=btn-gold onclick="plotSolar()">Load</button><div id=pSolar class=plot></div></div></div>
<div id=mod-lunes class=module><h2>🌙 Lunes vs Mercure</h2><div class=card><button class=btn-gold onclick="plotLunes()">Graph</button><button class=btn-titan onclick="teleportToTitan()">🚀 Vers Titan</button><div id=pLunes class=plot></div></div></div>
<div id=mod-apod class=module><h2>🖼️ Vision</h2><div class=card><button class=btn-gold onclick="loadAPOD()">APOD</button><div id=apodBox></div><div id=apodVisionBox style="display:none"><select id=visionModel><option value="llama-3.2-90b-vision-preview">90B Vision</option><option value="llama-3.2-11b-vision-preview">11B</option></select><button class=btn style="background:#aa00ff;color:#fff;padding:6px 10px;border-radius:8px" onclick="analyzeVision()">Analyser</button><div id=visionRes class=term style="height:280px"></div></div></div></div>
<div id=mod-avia class=module><h2>✈️ Avia Glenn Lushi 1208m rho 1.1</h2><div class=card><div class=grid><div><input id=avMass value="1000"><input id=avS value="16"><input id=avV value="25"></div><div><input id=avRho value="1.1"><input id=avCl value="0.8"><input id=avCd value="0.05"></div><div><div class=kpi><b>Lift</b><div id=avLift>-</div></div><div class=kpi><b>Go?</b><div id=avTakeoff>-</div></div></div></div><button class=btn style="background:#0044aa;color:#fff;padding:6px" onclick="calcAvia()">CALCUL L=0.5*rho*v²*S*Cl</button><div id=pAvia class=plot></div></div></div>
<div id=mod-agri class=module><h2>🌱 Agri POWER Lushi -11.67,27.47</h2><div class=card><button class=btn style="background:#00aa44;padding:6px 10px;border-radius:8px" onclick="loadAgriNASA()">Charger POWER</button><div class=grid><div class=kpi><b>T2M</b><div id=agT>-</div></div><div class=kpi><b>Pluie</b><div id=agP>-</div></div><div class=kpi><b>RH</b><div id=agH>-</div></div><div class=kpi><b>Maïs</b><div id=agConseil>-</div></div></div><div id=pAgri class=plot></div></div></div>
<div id=mod-ia class=module><h2>🤖 6 Groq</h2><div class=card><select id=groqModel><option value="llama-3.3-70b-versatile">🧠 70B</option><option value="llama-3.2-90b-vision-preview">👁️ 90B Vision</option><option value="llama-3.1-8b-instant">⚡ 8B</option><option value="mixtral-8x7b-32768">📚 Mixtral</option></select><select id=groqMode><option value="single">Single</option><option value="compare">Compare</option><option value="auto">Auto-fallback</option></select><div id=compareBox style="display:none"><select id=groqModel2><option value="llama-3.1-8b-instant">8B</option></select></div><textarea id=qIA rows=3>Explique atterrissage Titan Huygens 2005, lacs méthane Kraken Mare 400k km² > mer Caspienne, cycle méthane -179°C comme eau Terre, 5150km > Mercure 4879km densité 1.88 vs 5.43.</textarea><button class=btn-gold onclick="askIA()">Ask</button><button class=btn onclick="askIACompare()">Comparer</button><div class=grid style="grid-template-columns:1fr 1fr"><div><div id=iaRes class=term style="height:350px"></div></div><div id=col2 style="display:none"><div id=iaRes2 class=term style="height:350px"></div></div></div></div></div>

</div></div>
<script>
function show(m){document.querySelectorAll('.module').forEach(e=>e.classList.remove('active')); document.getElementById('mod-'+m).classList.add('active');}
let currentAPODUrl="", currentAPODTitle="", teleportEnabled=false;
document.getElementById('groqMode').addEventListener('change', e=>{ document.getElementById('compareBox').style.display=e.target.value=='compare'?'block':'none'; document.getElementById('col2').style.display=e.target.value=='compare'?'block':'none'; });
function enableTeleport(){ teleportEnabled=true; alert('🚀 Teleport actif - Clique étoile'); }
function teleportToTitan(){ startTeleport('TITAN 5150km', 1.2, 'Lacs méthane -179°C Kraken Mare 400k km²', true); }
function startTeleport(name, dist, info, isTitan=false){
 let o=document.getElementById('teleportOverlay'); o.style.display='flex'; let c=document.getElementById('warpContainer'); c.innerHTML='';
 for(let i=0;i<100;i++){ let w=document.createElement('div'); w.className='warp'; w.style.left=Math.random()*100+'%'; w.style.animationDelay=Math.random()*0.5+'s'; w.style.background=isTitan?'#ff8c00':'#fff'; c.appendChild(w); }
 let t=0; let iv=setInterval(()=>{ t+=0.05; document.getElementById('teleportText').innerText=`${isTitan?'🛬 ATTERRISSAGE':'🚀 TELEPORT'} ${name} ${Math.min(99,Math.floor(t*20))}%`; document.getElementById('teleportDist').innerText=`${info} | Dist ${dist}k al | c | ${isTitan?'Descente parachute Huygens 2h30':''}`; if(t>5){ clearInterval(iv); o.style.display='none'; if(isTitan){ show('titan'); plotTitan(); document.getElementById('tTitan').innerText=`✅ ATTERRI SUR ${name} - ${info} - Atterrissage réussi Huygens 14 janv 2005. Sol: glace d'eau + méthane. Temp -179°C. Lacs liquides méthane.`; } } },100);
}
function landingTitan(){
 startTeleport('TITAN', 1.2, 'Entrée atmosphérique 6km/s', true);
 setTimeout(()=>{ 
  let steps=["Entrée atmosphère N2 127km alt - 6km/s","Parachute principal - Décélération","Descente 2h30 - Photos brume orange","Survol rivières méthane Vid Flumina","Approche Kraken Mare 400k km²","Atterrissage sol glace - Bounce","Huygens posé - Temp -179°C - Analyse"];
  let i=0; let iv=setInterval(()=>{ if(i<steps.length){ document.getElementById('tTitan').innerText=`🛬 ${steps[i]}`; i++; } else clearInterval(iv); },800);
 },5500);
}
async function loadAPOD(){let b=document.getElementById('apodBox'); b.innerHTML='⏳...'; let r=await fetch('/nasa_apod'); let j=await r.json(); currentAPODUrl=j.url; currentAPODTitle=j.title; b.innerHTML=`<h3>${j.title}</h3><img src="${j.url}" style="width:100%;max-height:350px;object-fit:contain"><p>${(j.explanation||'').slice(0,600)}...</p>`; document.getElementById('apodVisionBox').style.display='block';}
async function analyzeVision(){let m=document.getElementById('visionModel').value; document.getElementById('visionRes').innerText='⏳...'; let r=await fetch('/vision_apod',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url:currentAPODUrl,title:currentAPODTitle,model:m})}); let j=await r.json(); document.getElementById('visionRes').innerText=j.ans;}
async function askIA(){let q=document.getElementById('qIA').value, model=document.getElementById('groqModel').value, mode=document.getElementById('groqMode').value; document.getElementById('iaRes').innerText='⏳ '+model+'...'; let r=await fetch('/ask_groq',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({q,model,mode})}); let j=await r.json(); document.getElementById('iaRes').innerText=j.ans;}
async function askIACompare(){let q=document.getElementById('qIA').value, m1=document.getElementById('groqModel').value, m2=document.getElementById('groqModel2').value; document.getElementById('iaRes').innerText='⏳...'; document.getElementById('iaRes2').innerText='⏳...'; document.getElementById('col2').style.display='block'; let r=await fetch('/ask_groq_compare',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({q,m1,m2})}); let j=await r.json(); document.getElementById('iaRes').innerText=j.ans1; document.getElementById('iaRes2').innerText=j.ans2;}
function calcAvia(){let m=parseFloat(avMass.value), S=parseFloat(avS.value), v=parseFloat(avV.value), rho=parseFloat(avRho.value), Cl=parseFloat(avCl.value); let L=0.5*rho*v*v*S*Cl, W=m*9.81; avLift.innerText=L.toFixed(1)+' N'; avTakeoff.innerText=L>W?'✅ GO':'❌ NO'; Plotly.newPlot('pAvia', [{x:[10,20,30,40,50],y:[0.5*rho*10*10*S*Cl,0.5*rho*20*20*S*Cl,0.5*rho*30*30*S*Cl,0.5*rho*40*40*S*Cl,0.5*rho*50*50*S*Cl],name:'Lift'}], {title:'Avia'});}
async function loadAgriNASA(){let r=await fetch('/nasa_power'); let j=await r.json(); let dates=Object.keys(j.T2M), tVals=Object.values(j.T2M), pVals=Object.values(j.PRECTOTCORR); agT.innerText=(tVals.reduce((a,b)=>a+b,0)/tVals.length).toFixed(1)+' C'; agP.innerText=pVals.reduce((a,b)=>a+b,0).toFixed(1)+' mm'; Plotly.newPlot('pAgri', [{x:dates,y:tVals,name:'T2M'}], {title:'Lushi POWER'});}

function plotTitan(){
 Plotly.newPlot('pTitan', [
 {x:[0,2,4,6,8,10],y:[0,1,2,1.5,2.5,1],mode:'lines+markers',line:{color:'#ff8c00',width:4},marker:{size:10,color:'#ff8c00'},name:'Rivières méthane Vid Flumina 400km'},
 {x:[2,3,4,7,8,9],y:[5,6,5.5,6,5,6],mode:'markers',marker:{size:[40,30,25,60,35,20],color:'#001122',line:{color:'#ff8c00',width:2}},name:'Lacs méthane',text:['Kraken Mare 400k km²','Ligeia Mare 126k','Punga Mare 61k','Mare','Lac','Petit lac'],hoverinfo:'text'},
 {x:[5],y:[2],mode:'markers+text',text:['🛬 Huygens 2005<br>-179°C Sol glace'],marker:{size:20,color:'red'},name:'Atterrissage'}
 ], {title:'🗺️ TITAN - CARTE LACS METHANE - Kraken Mare > Mer Caspienne - Cycle pluie rivière lac', paper_bgcolor:'#000', plot_bgcolor:'#0a0a0a', font:{color:'#fff'}, xaxis:{title:'Longitude'}, yaxis:{title:'Latitude Nord'}});
}
function plotTitan3D(){
 let x=[],y=[],z=[],c=[],s=[],txt=[];
 // Terrain glace
 for(let i=0;i<200;i++){ x.push(Math.random()*10); y.push(Math.random()*8); z.push(Math.random()*0.5); c.push('#ccccaa'); s.push(2); txt.push('Glace eau'); }
 // Lacs méthane liquide 3D
 for(let i=0;i<100;i++){ let lx=2+Math.random()*2, ly=5+Math.random()*1; x.push(lx); y.push(ly); z.push(-0.2); c.push('#001122'); s.push(8); txt.push('Kraken Mare - Méthane liquide -179°C'); }
 for(let i=0;i<60;i++){ let lx=7+Math.random()*1.5, ly=5.5+Math.random()*0.8; x.push(lx); y.push(ly); z.push(-0.15); c.push('#001a33'); s.push(6); txt.push('Ligeia Mare'); }
 x.push(5); y.push(2); z.push(0.5); c.push('red'); s.push(15); txt.push('🛬 Huygens - Atterri ici 2005');
 Plotly.newPlot('pTitan', [{x:x,y:y,z:z,mode:'markers',marker:{size:s,color:c,opacity:0.9},text:txt,hoverinfo:'text',type:'scatter3d',name:'Titan 3D'}], {title:'🌊 TITAN 3D - LACS METHANE LIQUIDE - Kraken Mare 400k km² - Profondeur 300m - Navigation possible bateau', scene:{bgcolor:'#000', xaxis:{title:'km x100'}, yaxis:{title:'km'}, zaxis:{title:'Altitude'}}, paper_bgcolor:'#000'});
}
function plotGalaxy(){
 let x=[],y=[],z=[],c=[],s=[],txt=[];
 for(let arm=0;arm<4;arm++){ for(let i=0;i<150;i++){ let r=3+Math.random()*14, th=arm*1.57 + r*0.35; x.push(r*Math.cos(th)); y.push(r*Math.sin(th)); z.push((Math.random()-0.5)*0.6); c.push(arm==1?'#00aaff':'white'); s.push(2); txt.push(`Bras ${arm}`); } }
 x.push(0,8.2,8.5); y.push(0,0,0.5); z.push(0,0,0); c.push('red','#ffaa00','#ff8c00'); s.push(16,14,10); txt.push('Sag A* Trou noir','Soleil Nous','Titan 5150km TELEPORT');
 Plotly.newPlot('pGalaxy', [{x:x,y:y,z:z,mode:'markers',marker:{size:s,color:c},text:txt,hoverinfo:'text',type:'scatter3d'}], {title:'Galaxie - Clique Titan pour teleport'});
 document.getElementById('pGalaxy').on('plotly_click', function(d){ if(!teleportEnabled){ alert('Active teleport'); return; } let pt=d.points[0]; if(pt.text.includes('Titan')) teleportToTitan(); else startTeleport(pt.text||'Etoile', 10, 'Teleport'); });
}
function plotSolar(){ let traces=[]; [{n:'Sun',r:0,c:'yellow',s:20},{n:'Mercury',r:0.39,c:'#aaa',s:5},{n:'Earth',r:1,c:'#00aaff',s:7},{n:'Jupiter',r:5.2,c:'#ffaa66',s:14},{n:'Ganymede 5268km',r:5.2,c:'#ffaa00',s:9},{n:'Saturn',r:9.5,c:'#ffdd99',s:12},{n:'Titan 5150km',r:9.5,c:'#ff8c00',s:9}].forEach(p=>{ if(p.r==0) traces.push({x:[0],y:[0],z:[0],mode:'markers+text',text:[p.n],marker:{size:p.s,color:p.c},type:'scatter3d'}); else{ let x=[],y=[]; for(let a=0;a<=360;a+=10){let rad=a*Math.PI/180; x.push(p.r*Math.cos(rad)); y.push(p.r*Math.sin(rad));} traces.push({x:x,y:y,z:Array(x.length).fill(0),mode:'lines',line:{color:p.c},name:p.n}); } }); Plotly.newPlot('pSolar', traces, {title:'Solaire'}); }
function plotLunes(){ Plotly.newPlot('pLunes', [{x:['Mercure','Ganymède','Titan'],y:[4879,5268,5150],type:'bar',marker:{color:['#aaa','#ffaa00','#ff8c00']}}], {title:'2 Lunes > Mercure'}); }
window.onload=()=>setTimeout(()=>{plotTitan(); calcAvia();},800);
</script></body></html>
"""

@app.route("/")
def home(): return render_template_string(HTML)

@app.route("/nasa_apod")
def nasa_apod():
    try: return jsonify(requests.get(f"https://api.nasa.gov/planetary/apod?api_key={NASA_KEY}", timeout=10).json())
    except: return jsonify({"title":"Titan Lakes","url":"https://apod.nasa.gov/apod/image/2301/TitanLakes.jpg","explanation":"Mock Titan"})

@app.route("/nasa_power")
def nasa_power():
    try:
        url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,PRECTOTCORR,RH2M&community=AG&longitude={LUSHI_LON}&latitude={LUSHI_LAT}&start=20240101&end=20240110&format=JSON"
        return jsonify(requests.get(url, timeout=15).json()['properties']['parameter'])
    except: return jsonify({"T2M":{"20240101":26,"20240102":27},"PRECTOTCORR":{"20240101":2,"20240102":5},"RH2M":{"20240101":65,"20240102":70}})

def call_groq(q, model):
    from groq import Groq
    client=Groq(api_key=GROQ_KEY)
    chat=client.chat.completions.create(model=model, messages=[{"role":"system","content":"Titan expert Lushi"},{"role":"user","content":q}], max_tokens=1500)
    return chat.choices[0].message.content

def call_groq_vision(url,title,model):
    from groq import Groq
    client=Groq(api_key=GROQ_KEY)
    chat=client.chat.completions.create(model=model, messages=[{"role":"user","content":[{"type":"text","text":f"Titan {title}"},{"type":"image_url","image_url":{"url":url}}]}], max_tokens=1500)
    return chat.choices[0].message.content

@app.route("/ask_groq", methods=["POST"])
def ask_groq():
    d=request.json; q=d.get("q",""); m=d.get("model","llama-3.3-70b-versatile"); mode=d.get("mode","single")
    if not GROQ_KEY: return jsonify({"ans":"No key"})
    try:
        if mode=="auto":
            for mm in GROQ_MODELS.keys():
                try: return jsonify({"ans":call_groq(q,mm),"model_used":mm})
                except: continue
        return jsonify({"ans":call_groq(q,m),"model_used":m})
    except Exception as e: return jsonify({"ans":str(e)})

@app.route("/ask_groq_compare", methods=["POST"])
def ask_groq_compare():
    d=request.json; q=d.get("q",""); m1=d.get("m1","llama-3.3-70b-versatile"); m2=d.get("m2","llama-3.1-8b-instant")
    try: return jsonify({"ans1":call_groq(q,m1),"ans2":call_groq(q,m2),"model1":m1,"model2":m2})
    except Exception as e: return jsonify({"ans1":str(e),"ans2":str(e)})

@app.route("/vision_apod", methods=["POST"])
def vision_apod():
    d=request.json; url=d.get("url",""); title=d.get("title",""); model=d.get("model","llama-3.2-90b-vision-preview")
    try: return jsonify({"ans":call_groq_vision(url,title,model)})
    except Exception as e: return jsonify({"ans":str(e)})

@app.route("/runpy", methods=["POST"])
def runpy():
    code=request.form.get('code',''); path=f"/tmp/astroveros/nasa.py"
    open(path,'w', encoding='utf-8').write(code)
    try:
        r=subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=12, cwd="/tmp/astroveros")
        return jsonify({"out":r.stdout+r.stderr})
    except: return jsonify({"out":traceback.format_exc()})

if __name__=="__main__":
    print(f"🪐 V7 TITAN LANDING READY http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000)
