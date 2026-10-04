// Shared display state. Route rendering and activity state remain with the router.
export function initializePresentation(onChange = () => {}, {
  beforeEnter = () => {},
  afterExit = () => {}
} = {}) {
  const region = document.querySelector('#navigation-region');
  const target = document.documentElement;
  const controls = document.createElement('div');
  controls.className = 'presentation-controls';
  controls.dataset.fullscreen = 'inactive';

  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'presentation-toggle';
  button.textContent = 'Presentation mode';
  button.setAttribute('aria-label', 'Presentation mode');
  button.setAttribute('aria-pressed', 'false');

  const feedback = document.createElement('p');
  feedback.className = 'visually-hidden presentation-status';
  feedback.setAttribute('role', 'status');
  feedback.setAttribute('aria-live', 'polite');
  feedback.setAttribute('aria-atomic', 'true');
  controls.append(button, feedback);
  region.append(controls);

  let active = false;
  let version = 0;
  let pendingRequest = null;
  let ownerVersion = null;
  let observedVersion = null;

  function updateMode(next, message) {
    active = next;
    document.body.classList.toggle('presentation-mode', active);
    const label = active ? 'Exit presentation' : 'Presentation mode';
    button.textContent = label;
    button.setAttribute('aria-label', label);
    button.setAttribute('aria-pressed', String(active));
    if (message) feedback.textContent = message;
    onChange();
  }

  function fallback(message) {
    controls.dataset.fullscreen = 'fallback';
    feedback.textContent = message;
  }

  function exitOwnedFullscreen(expectedOwner) {
    if (ownerVersion !== expectedOwner || document.fullscreenElement !== target) return;
    try {
      Promise.resolve(document.exitFullscreen()).catch(() => {
        if (!active) feedback.textContent = 'Presentation layout ended. Press Escape to leave browser fullscreen.';
      });
    } catch {
      if (!active) feedback.textContent = 'Presentation layout ended. Press Escape to leave browser fullscreen.';
    }
  }

  function leavePresentation(message = 'Presentation mode ended.', restore = true) {
    const owned = ownerVersion;
    version += 1;
    controls.dataset.fullscreen = 'inactive';
    updateMode(false, message);
    afterExit(restore);
    if (owned !== null) exitOwnedFullscreen(owned);
  }

  function enterPresentation() {
    // The router closes any site drawer before hiding site navigation. It never
    // remounts the current activity, and this remains in the activation handler.
    beforeEnter();
    const requestVersion = ++version;
    updateMode(true, 'Presentation layout is active.');
    button.focus({ preventScroll: true });

    // An earlier request may still complete after an exit. Do not issue a
    // competing request; its completion is cleaned up without resetting routes.
    if (pendingRequest || (ownerVersion !== null && ownerVersion !== requestVersion)) {
      fallback('Presentation layout is active while an earlier fullscreen request finishes. Use Exit presentation to leave.');
      if (ownerVersion !== null) exitOwnedFullscreen(ownerVersion);
      return;
    }
    if (document.fullscreenElement) {
      observedVersion = requestVersion;
      controls.dataset.fullscreen = 'native';
      feedback.textContent = 'Presentation layout is active in browser fullscreen.';
      return;
    }
    if (typeof target.requestFullscreen !== 'function' || document.fullscreenEnabled === false) {
      fallback('Presentation layout is active. Browser fullscreen is unavailable; use Exit presentation to leave.');
      return;
    }

    const request = { version: requestVersion };
    pendingRequest = request;
    controls.dataset.fullscreen = 'requesting';
    feedback.textContent = 'Presentation layout is active. Requesting browser fullscreen.';

    let result;
    try {
      // This call runs directly in the button activation, before any await or
      // promise callback, so it retains the browser's user-activation permission.
      result = target.requestFullscreen({ navigationUI: 'hide' });
    } catch {
      pendingRequest = null;
      if (active && version === requestVersion) {
        fallback('Presentation layout is active. Browser fullscreen was not allowed; use Exit presentation to leave.');
      }
      return;
    }

    Promise.resolve(result).then(() => {
      if (pendingRequest === request) pendingRequest = null;
      if (document.fullscreenElement === target) ownerVersion = requestVersion;
      if (!active || version !== requestVersion) {
        if (ownerVersion === requestVersion) exitOwnedFullscreen(requestVersion);
        return;
      }
      if (document.fullscreenElement === target) {
        observedVersion = requestVersion;
        controls.dataset.fullscreen = 'native';
        feedback.textContent = 'Presentation mode is active in browser fullscreen. Use Exit presentation or Escape to leave.';
      } else {
        fallback('Presentation layout is active. Browser fullscreen did not open; use Exit presentation to leave.');
      }
    }, () => {
      if (pendingRequest === request) pendingRequest = null;
      if (active && version === requestVersion) {
        fallback('Presentation layout is active. Browser fullscreen was not allowed; use Exit presentation to leave.');
      }
    });
  }

  button.addEventListener('click', () => {
    if (active) leavePresentation();
    else enterPresentation();
  });

  document.addEventListener('fullscreenchange', () => {
    if (document.fullscreenElement === target) {
      if (pendingRequest) ownerVersion = pendingRequest.version;
      if (ownerVersion !== null && (!active || ownerVersion !== version)) {
        exitOwnedFullscreen(ownerVersion);
        return;
      }
      if (active) {
        observedVersion = version;
        controls.dataset.fullscreen = 'native';
      }
      return;
    }
    if (document.fullscreenElement) return;
    const previousOwner = ownerVersion;
    ownerVersion = null;
    if (active && (previousOwner === version || observedVersion === version)) {
      leavePresentation('Presentation mode ended after leaving browser fullscreen.');
    }
    observedVersion = null;
  });

  document.addEventListener('keydown', event => {
    // The drawer's earlier handler gets the first Escape, retaining its
    // approved focus/close behaviour. A later Escape can leave presentation.
    if (event.key === 'Escape' && !event.defaultPrevented && active) {
      event.preventDefault();
      leavePresentation();
    }
  });

  return {
    isActive: () => active,
    controls,
    button,
    leaveForRoute: () => leavePresentation('Presentation mode ended after changing destination.', false)
  };
}
