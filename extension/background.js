// background.js
async function startAnalysis(videoId) {
  try {
    const response = await fetch('http://localhost:5000/analyze_video', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ video_id: videoId })
    });
    if (!response.ok) {
      const err = await response.text();
      throw new Error(`API error (${response.status}): ${err}`);
    }
    const data = await response.json();
    return data.job_id;
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
}

async function pollJobStatus(jobId, onUpdate, onComplete, onError) {
  const poll = async () => {
    try {
      const response = await fetch(`http://localhost:5000/job/${jobId}`);
      if (!response.ok) {
        const err = await response.text();
        throw new Error(`Poll error: ${err}`);
      }
      const status = await response.json();

      if (status.status === 'complete') {
        onComplete(status);
        return;
      } else if (status.status === 'error') {
        onError(status.error || 'Unknown error');
        return;
      } else {
        onUpdate(status);
        setTimeout(poll, 1000); // poll every second
      }
    } catch (error) {
      onError(error.message);
    }
  };
  poll();
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'analyze') {
    startAnalysis(request.videoId)
      .then(jobId => {
        sendResponse({ jobId });
        // The popup will now poll; we don't keep the channel open.
      })
      .catch(error => sendResponse({ error: error.message }));
    return true; // keep channel open for startAnalysis response
  }
});