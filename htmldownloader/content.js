chrome.runtime.sendMessage({
    type: 'getHTML',
    result: document.documentElement.outerHTML,
    title: document.title
  });
  