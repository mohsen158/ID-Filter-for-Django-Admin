// Matches /<prefix>/admin/<app>/<model>/<pk>/<change|history|delete>/
const OBJECT_PAGE = /^(.*\/admin\/[^/]+\/[^/]+\/)([^/]+)\/(?:change|history|delete)\/?$/;

function convert(rawUrl) {
  let url;
  try {
    url = new URL(rawUrl);
  } catch {
    return null;
  }
  const match = url.pathname.match(OBJECT_PAGE);
  if (!match) return null;

  const [, listPath, pk] = match;
  url.pathname = listPath;
  url.search = "";
  url.hash = "";
  url.searchParams.set("id", decodeURIComponent(pk));
  return url.toString();
}

chrome.action.onClicked.addListener((tab) => {
  const target = convert(tab.url || "");
  if (!target) {
    chrome.action.setBadgeText({ tabId: tab.id, text: "✗" });
    chrome.action.setBadgeBackgroundColor({ tabId: tab.id, color: "#d33" });
    setTimeout(() => chrome.action.setBadgeText({ tabId: tab.id, text: "" }), 1500);
    return;
  }
  chrome.tabs.update(tab.id, { url: target });
});

if (typeof module !== "undefined") module.exports = { convert };
