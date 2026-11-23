(function(){
  window.DCLogic = class {
    constructor(props){ this.props = props || {}; this.state = {}; }
    setState(p){ this.state = Object.assign({}, this.state, typeof p === 'function' ? p(this.state) : p); window.__dcRender(); }
    forceUpdate(){ window.__dcRender(); }
  };
  const HOLE = /\{\{\s*([^}]+?)\s*\}\}/g;
  function get(scope, path){
    path = path.trim();
    if (path === 'true') return true; if (path === 'false') return false;
    if (/^-?\d+(\.\d+)?$/.test(path)) return Number(path);
    let v = scope;
    for (const k of path.split('.')) { if (v == null) return undefined; v = v[k]; }
    return v;
  }
  const interp = (s, sc) => s.replace(HOLE, (_, p) => { const v = get(sc, p); return v == null ? '' : String(v); });
  const whole = s => { const m = (s || '').match(/^\s*\{\{\s*([^}]+?)\s*\}\}\s*$/); return m ? m[1] : null; };
  function proc(node, scope, out){
    if (node.nodeType === 3) { out.appendChild(document.createTextNode(interp(node.nodeValue, scope))); return; }
    if (node.nodeType !== 1) return;
    const tag = node.tagName.toLowerCase();
    if (tag === 'helmet') return;
    if (tag === 'sc-if') { if (get(scope, whole(node.getAttribute('value')))) for (const c of node.childNodes) proc(c, scope, out); return; }
    if (tag === 'sc-for') {
      const list = get(scope, whole(node.getAttribute('list'))) || []; const as = node.getAttribute('as') || 'item';
      list.forEach((it, i) => { const s = Object.create(scope); s[as] = it; s.$index = i; for (const c of node.childNodes) proc(c, s, out); });
      return;
    }
    const el = document.createElementNS(node.namespaceURI, node.localName);
    let selVal = null;
    for (const a of node.attributes) {
      const w = whole(a.value);
      if (a.name.startsWith('on') && w) { const fn = get(scope, w); if (typeof fn === 'function') el.addEventListener(a.name.slice(2), fn); continue; }
      if (a.name.startsWith('hint-')) continue;
      const v = interp(a.value, scope);
      if (a.name === 'value' && tag === 'select') { selVal = v; continue; }
      el.setAttribute(a.name, v);
    }
    for (const c of node.childNodes) proc(c, scope, el);
    if (selVal !== null) el.value = selVal;
    out.appendChild(el);
  }
  document.addEventListener('DOMContentLoaded', () => {
    const xdc = document.querySelector('x-dc');
    const helmet = xdc.querySelector('helmet');
    if (helmet) for (const c of [...helmet.childNodes]) document.head.appendChild(c.cloneNode(true));
    const tpl = xdc.cloneNode(true); xdc.remove();
    const src = document.querySelector('script[type="text/x-dc"]').textContent;
    const Component = (new Function('DCLogic', src + '\n;return Component;'))(window.DCLogic);
    const inst = new Component({});
    const root = document.createElement('div'); root.id = 'dc-root'; document.body.prepend(root);
    window.__dcRender = () => {
      root.innerHTML = '';
      const vals = inst.renderVals();
      for (const c of tpl.childNodes) proc(c, vals, root);
    };
    window.__dcRender();
    window.__dcReady = true;
  });
})();
