// content.js – extracts video ID from the current YouTube page
function getVideoId() {
  const url = window.location.href;
  const match = url.match(/(?:youtu\.be\/|watch\?v=)([a-zA-Z0-9_-]{11})/);
  return match ? match[1] : null;
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getVideoId') {
    const videoId = getVideoId();
    sendResponse({ videoId });
  }
});