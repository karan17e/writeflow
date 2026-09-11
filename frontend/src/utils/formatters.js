export function countWords(text = '') {
  if (!text) return 0;
  return text.trim().split(/\s+/).filter(Boolean).length;
}

export function estimateReadingTime(wordCount = 0) {
  const wordsPerMinute = 200;
  const minutes = Math.ceil(wordCount / wordsPerMinute);
  return minutes <= 1 ? '1 min read' : `${minutes} min read`;
}

export function formatDate(isoString) {
  if (!isoString) return '';
  const date = new Date(isoString);
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date);
}

export function formatErrorMessage(err, defaultMsg = 'An unexpected error occurred.') {
  if (!err) return defaultMsg;
  if (typeof err === 'string') return err;

  const responseData = err.response?.data;
  let detail = responseData?.detail || responseData?.message || responseData?.error || err.message;

  if (Array.isArray(detail)) {
    const messages = detail.map((item) => {
      if (typeof item === 'string') return item;
      if (item && typeof item === 'object') {
        const field = Array.isArray(item.loc)
          ? item.loc.filter((l) => l !== 'body' && l !== 'query' && l !== 'path').join('.')
          : item.loc;
        const msg = item.msg || item.message || JSON.stringify(item);
        return field ? `${field}: ${msg}` : msg;
      }
      return String(item);
    });
    return messages.join(' | ');
  }

  if (detail && typeof detail === 'object') {
    if (detail.msg) return String(detail.msg);
    if (detail.message) return String(detail.message);
    try {
      return JSON.stringify(detail);
    } catch {
      return defaultMsg;
    }
  }

  if (detail && typeof detail === 'string') {
    return detail;
  }

  return err.message || defaultMsg;
}
