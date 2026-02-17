document.addEventListener('DOMContentLoaded', () => {
  const videoTitleEl = document.getElementById('videoTitle');
  const positiveEl = document.getElementById('positive');
  const neutralEl = document.getElementById('neutral');
  const negativeEl = document.getElementById('negative');
  const totalEl = document.getElementById('total');
  const errorEl = document.getElementById('error');
  const warningEl = document.getElementById('warning');
  const refreshBtn = document.getElementById('refresh');
  const statusEl = document.getElementById('status');

  async function analyzeCurrentVideo() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab || !tab.url.includes('youtube.com/watch')) {
      showError('Please open a YouTube video page.');
      return;
    }

    chrome.tabs.sendMessage(tab.id, { action: 'getVideoId' }, async (response) => {
      if (chrome.runtime.lastError) {
        showError('Cannot communicate with page. Try refreshing the video page.');
        return;
      }

      const { videoId } = response;
      if (!videoId) {
        showError('Could not extract video ID from URL.');
        return;
      }

      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => document.querySelector('h1 yt-formatted-string')?.innerText.trim() || 'YouTube Video'
      }, (results) => {
        if (results && results[0]) {
          videoTitleEl.textContent = results[0].result;
        }
      });

      chrome.runtime.sendMessage({ action: 'analyze', videoId }, (result) => {
        if (result.error) {
          showError(`API Error: ${result.error}`);
          return;
        }

        const jobId = result.jobId;
        statusEl.classList.remove('hidden');
        statusEl.textContent = 'Starting analysis...';

        pollJobStatus(jobId, 
          (status) => {
            if (status.status === 'fetching') {
              statusEl.textContent = `Fetching comments... (${status.fetched || 0} so far)`;
            } else if (status.status === 'analyzing') {
              statusEl.textContent = `Analyzing comments... (${status.processed}/${status.total})`;
            }
          },
          (finalStatus) => {
            statusEl.classList.add('hidden');
            if (finalStatus.warning) {
              warningEl.textContent = finalStatus.warning;
              warningEl.classList.remove('hidden');
            } else {
              warningEl.classList.add('hidden');
            }

            const counts = finalStatus.results;
            positiveEl.textContent = counts.positive || 0;
            neutralEl.textContent = counts.neutral || 0;
            negativeEl.textContent = counts.negative || 0;
            totalEl.textContent = `Total Comments: ${counts.total || 0}`;
            errorEl.classList.add('hidden');
          },
          (errorMsg) => {
            showError(errorMsg);
          }
        );
      });
    });
  }

  function showError(msg) {
    errorEl.textContent = msg;
    errorEl.classList.remove('hidden');
    warningEl.classList.add('hidden');
    statusEl.classList.add('hidden');
    positiveEl.textContent = '0';
    neutralEl.textContent = '0';
    negativeEl.textContent = '0';
    totalEl.textContent = 'Total Comments: 0';
  }

  analyzeCurrentVideo();

  refreshBtn.addEventListener('click', () => {
    errorEl.classList.add('hidden');
    warningEl.classList.add('hidden');
    analyzeCurrentVideo();
  });
});

// Polling function – now uses the same base URL
function pollJobStatus(jobId, onUpdate, onComplete, onError) {
  const API_BASE = 'https://zoro828-yt-sentiment-analysis.hf.space';
  const poll = () => {
    fetch(`${API_BASE}/job/${jobId}`)
      .then(response => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
      })
      .then(status => {
        if (status.status === 'complete') {
          onComplete(status);
        } else if (status.status === 'error') {
          onError(status.error || 'Unknown error');
        } else {
          onUpdate(status);
          setTimeout(poll, 1000);
        }
      })
      .catch(err => onError(err.message));
  };
  poll();
} 