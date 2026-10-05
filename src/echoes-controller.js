/** A zero-based slide controller; changes are synchronous and never wrap. */
export function createSlideController(count, onChange = () => {}) {
  if (!Number.isInteger(count) || count < 1) {
    throw new RangeError('Slide count must be a positive integer.');
  }
  if (typeof onChange !== 'function') {
    throw new TypeError('Slide change listener must be a function.');
  }

  let currentIndex = 0;

  function goToSlide(index) {
    if (!Number.isInteger(index) || index < 0 || index >= count) {
      throw new RangeError('Slide index must be an integer inside the deck.');
    }
    if (index !== currentIndex) {
      currentIndex = index;
      onChange(currentIndex);
    }
    return currentIndex;
  }

  return {
    nextSlide: () => goToSlide(Math.min(currentIndex + 1, count - 1)),
    previousSlide: () => goToSlide(Math.max(currentIndex - 1, 0)),
    goToSlide,
    getIndex: () => currentIndex,
  };
}

/** Points use x/y; optional pointer metadata prevents cancelled or mixed gestures. */
export function swipeDirection(start, end) {
  if (!start || !end || start.cancelled || end.cancelled) return null;
  if ((start.pointerType && start.pointerType !== 'touch')
    || (end.pointerType && end.pointerType !== 'touch')) return null;
  if (start.pointerId != null && end.pointerId != null
    && start.pointerId !== end.pointerId) return null;
  if (![start.x, start.y, end.x, end.y].every(Number.isFinite)) return null;

  const horizontal = end.x - start.x;
  const vertical = end.y - start.y;
  if (Math.abs(horizontal) < 50 || Math.abs(horizontal) < Math.abs(vertical) * 1.4) {
    return null;
  }
  return horizontal > 0 ? 'previous' : 'next';
}

const interactiveTags = new Set(['button', 'a', 'input', 'textarea', 'select']);

/** Preserve native control/editing behavior before interpreting deck arrow keys. */
export function keyboardDirection(event) {
  if (!event || event.defaultPrevented || event.isComposing
    || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return null;
  if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return null;

  for (let element = event.target; element; element = element.parentElement) {
    if (interactiveTags.has(String(element.tagName || '').toLowerCase())
      || element.isContentEditable) return null;
  }
  return event.key === 'ArrowLeft' ? 'previous' : 'next';
}
