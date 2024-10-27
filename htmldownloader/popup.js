document.getElementById('downloadHtml').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  if (tab.url.startsWith('chrome://')) {
    alert('Cannot access a chrome:// URL');
    return;
  }

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: getHTMLAndTitle,
  }, (results) => {
    if (chrome.runtime.lastError) {
      console.error(chrome.runtime.lastError);
      return;
    }

    if (results && results[0] && results[0].result) {
      const { html, title } = results[0].result;
      const blob = new Blob([html], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      const filename = title ? `${title}.html` : 'page.html';
      chrome.downloads.download({
        url: url,
        filename: filename,
      }, () => {
        console.log('file downloaded', filename);
        
        fetch('http://localhost:5000/trigger_scrapy', { method: 'POST' });
      });
    } else {
      console.error('No result from content script');
    }
  });
});

function getHTMLAndTitle() {
  return {
    html: document.documentElement.outerHTML,
    title: document.title.replace(/[^a-zA-Z0-9]/g, '_'),
  };
}
