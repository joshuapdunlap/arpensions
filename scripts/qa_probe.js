/* Local QA only. This file is never copied into the published site. */
(() => {
  const vitals = {lcpMs:null, cls:0, maxInteractionMs:0};
  for (const type of ['largest-contentful-paint','layout-shift','event']) {
    try {new PerformanceObserver(list=>{for(const entry of list.getEntries()) {
      if(type==='largest-contentful-paint')vitals.lcpMs=entry.startTime;
      if(type==='layout-shift'&&!entry.hadRecentInput)vitals.cls+=entry.value;
      if(type==='event'&&entry.interactionId)vitals.maxInteractionMs=Math.max(vitals.maxInteractionMs,entry.duration);
    }}).observe({type,buffered:true,durationThreshold:16});}catch{}
  }
  addEventListener('load',async()=>{
    await document.fonts.ready;
    const results=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});
    const output=document.createElement('details');output.id='qa-report';output.setAttribute('data-pagefind-ignore','');
    const summary=document.createElement('summary');summary.textContent='Local QA results';
    const pre=document.createElement('pre');pre.id='qa-result-json';output.append(summary,pre);document.body.append(output);
    const update=()=>{
      const report={path:location.pathname,width:innerWidth,height:innerHeight,theme:document.documentElement.dataset.theme||'light',nojs:new URLSearchParams(location.search).has('nojs'),documentWidth:document.documentElement.scrollWidth,overflow:document.documentElement.scrollWidth>document.documentElement.clientWidth,violations:results.violations.map(v=>({id:v.id,impact:v.impact,description:v.description,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))})),incomplete:results.incomplete.map(v=>({id:v.id,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))})),labVitals:{...vitals},externalResources:performance.getEntriesByType('resource').map(r=>r.name).filter(url=>new URL(url).origin!==location.origin),hiddenVisible:[...document.querySelectorAll("[hidden]")].filter(e=>getComputedStyle(e).display!=="none").map(e=>e.id||e.className),images:[...document.images].filter(i=>i.complete&&!i.naturalWidth).map(i=>i.src)};
      pre.textContent=JSON.stringify(report);
      fetch('/__qa/report',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(report)});
    };
    update();setTimeout(update,1000);document.addEventListener('click',()=>setTimeout(update,300));
  });
})();
