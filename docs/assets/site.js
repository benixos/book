(function(){
  var nav=document.getElementById('nav');
  if(nav){var wide=matchMedia('(min-width:56rem)').matches;nav.open=wide;}
  var blocks=document.querySelectorAll('pre > code.language-mermaid');
  if(!blocks.length||!window.mermaid)return;
  blocks.forEach(function(c){var d=document.createElement('div');d.className='mermaid';d.textContent=c.textContent;c.parentElement.replaceWith(d);});
  var dark=matchMedia('(prefers-color-scheme: dark)').matches;
  mermaid.initialize({startOnLoad:false,theme:dark?'dark':'neutral',securityLevel:'strict'});
  mermaid.run({querySelector:'.mermaid'});
})();
