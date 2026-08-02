(() => {
  const visible = (el) => !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
  const authorized = (el) => el.matches('[data-overflow-authorized], .table-wrap, .tabbar, .sidebar, .workspace');
  const issues = [];
  for (const el of document.querySelectorAll('body *')) {
    if (!visible(el) || authorized(el)) continue;
    const box = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    const clippedX = ['hidden', 'clip'].includes(style.overflowX);
    const clippedY = ['hidden', 'clip'].includes(style.overflowY);
    if ((clippedX && el.scrollWidth > el.clientWidth + 1) || (clippedY && el.scrollHeight > el.clientHeight + 1)) {
      issues.push({type: 'internal-overflow', tag: el.tagName, id: el.id, className: el.className});
    }
    if (box.left < -1 || box.right > innerWidth + 1) {
      issues.push({type: 'outside-viewport', tag: el.tagName, id: el.id, left: box.left, right: box.right});
    }
    if (el.matches('button, input:not([type="checkbox"]):not([type="radio"]), select') && box.height > 0 && box.height < 30) {
      issues.push({type: 'control-too-short', tag: el.tagName, id: el.id, height: box.height});
    }
    if (el.matches('[role="dialog"], .modal, .drawer') && (box.height > innerHeight - 48 || box.width > innerWidth - 48)) {
      issues.push({type: 'overlay-outside-safe-area', tag: el.tagName, id: el.id});
    }
  }
  const result = {pass: issues.length === 0, viewport: {width: innerWidth, height: innerHeight}, issues};
  console.table(issues);
  return result;
})()
