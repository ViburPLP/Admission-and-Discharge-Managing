document.getElementById('downloadHtml').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  // Ensure the tab URL is not a chrome:// URL
  if (tab.url.startsWith('chrome://')) {
    alert('Cannot access a chrome:// URL');
    return;
  }

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: getHTML,
  }, (results) => {
    if (chrome.runtime.lastError) {
      console.error(chrome.runtime.lastError);
      return;
    }

    if (results && results[0] && results[0].result) {
      const html = results[0].result;
      const blob = new Blob([html], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      chrome.downloads.download({
        url: url,
        filename: 'page.html'
      });
    } else {
      console.error('No result returned from content script');
    }
  });
});

function getHTML() {
  return document.documentElement.outerHTML;
}
