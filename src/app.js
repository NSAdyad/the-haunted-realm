import { ACTIVITIES, GLOBAL_ASSETS } from './activities.js';
import { initializePresentation } from './presentation.js';
import { mountEchoes } from './echoes.js?v=activity-1';

const main = document.querySelector('#main-content');
const navigationRegion = document.querySelector('#navigation-region');
const announcement = document.querySelector('#route-announcement');
const skipLink = document.querySelector('.skip-link');
const narrow = window.matchMedia('(max-width: 900px)');
const destinations = new Map(ACTIVITIES.map(activity => [activity.id, activity]));
let menuOpen = false;
let currentActivity = null;
let isHome = true;
let overlayScrollPosition = null;
let presentationSnapshot = null;
let activityController = null;

const escapeHtml = value => String(value).replace(/[&<>"']/g, character => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[character]));
const routeFor = activity => `#/activities/${encodeURIComponent(activity.id)}`;

navigationRegion.innerHTML = `
  <nav class="global-navigation" aria-label="Global navigation">
    <div class="navigation-controls">
      <a class="home-control" href="#/">Home</a>
      <button class="activities-control" type="button" aria-expanded="false" aria-controls="activity-drawer">
        Activities <span class="chevron" aria-hidden="true"></span>
      </button>
    </div>
    <section id="activity-drawer" class="activity-drawer" aria-label="Activities" hidden>
      <div class="drawer-chains" aria-hidden="true"></div>
      <header class="drawer-heading">
        <span>Activities</span>
        <button type="button" class="close-drawer">Close</button>
      </header>
      <a class="rail-home" href="#/">Home</a>
      <ul class="destination-list">
        ${ACTIVITIES.map(activity => `
          <li><a class="destination-link" data-destination="${escapeHtml(activity.id)}" href="${routeFor(activity)}">
            <picture class="destination-image">
              <source media="(max-width: 900px)" srcset="${escapeHtml(activity.navImage34)}">
              <img src="${escapeHtml(activity.navImage38)}" width="38" height="38" alt="">
            </picture>
            <span>${escapeHtml(activity.name)}</span>
          </a></li>`).join('')}
      </ul>
    </section>
  </nav>`;

const drawer = document.querySelector('#activity-drawer');
const toggle = document.querySelector('.activities-control');
const closeButton = document.querySelector('.close-drawer');
const homeControl = document.querySelector('.home-control');
const navLinks = [...document.querySelectorAll('.destination-link')];
const destinationList = document.querySelector('.destination-list');
const isPermanentRail = () => !isHome && !narrow.matches;

function keepCurrentDestinationVisible() {
  if (drawer.hidden) return;
  const selected = navLinks.find(link => link.dataset.destination === currentActivity?.id);
  if (!selected) return;
  const row = selected.getBoundingClientRect();
  const list = destinationList.getBoundingClientRect();
  if (row.top < list.top) destinationList.scrollTop -= list.top - row.top;
  else if (row.bottom > list.bottom) destinationList.scrollTop += row.bottom - list.bottom;
}

function updateNavigation() {
  const activityPresentation = Boolean(currentActivity) && presentation.isActive();
  document.body.classList.toggle('activity-presentation', activityPresentation);
  activityController?.onPresentationChange(activityPresentation);
  if (activityPresentation) menuOpen = false;
  const permanent = isPermanentRail() && !activityPresentation;
  const overlay = menuOpen && !permanent;
  drawer.hidden = activityPresentation || (!permanent && !menuOpen);
  toggle.setAttribute('aria-expanded', String(permanent || menuOpen));
  if (overlay && overlayScrollPosition === null) {
    overlayScrollPosition = { x: window.scrollX, y: window.scrollY };
    document.body.style.top = `-${overlayScrollPosition.y}px`;
    document.body.classList.add('is-menu-open');
  } else if (!overlay && overlayScrollPosition !== null) {
    const previousScroll = overlayScrollPosition;
    overlayScrollPosition = null;
    document.body.classList.remove('is-menu-open');
    document.body.style.top = '';
    window.scrollTo(previousScroll.x, previousScroll.y);
  }
  const compactPresentation = overlay && window.innerWidth <= 600;
  presentation.controls.classList.toggle('in-drawer', compactPresentation);
  if (activityPresentation) document.body.append(presentation.controls);
  else if (compactPresentation) closeButton.before(presentation.controls);
  else navigationRegion.append(presentation.controls);
  navigationRegion.hidden = activityPresentation;
  navigationRegion.inert = activityPresentation;
  skipLink.hidden = activityPresentation;
  presentation.button.textContent = compactPresentation
    ? (presentation.isActive() ? 'Exit mode' : 'Present')
    : (presentation.isActive() ? 'Exit presentation' : 'Presentation mode');
  navigationRegion.classList.toggle('modal-navigation', overlay);
  if (overlay) {
    navigationRegion.setAttribute('role', 'dialog');
    navigationRegion.setAttribute('aria-modal', 'true');
    navigationRegion.setAttribute('aria-label', 'Activities navigation');
  } else {
    navigationRegion.removeAttribute('role');
    navigationRegion.removeAttribute('aria-modal');
    navigationRegion.removeAttribute('aria-label');
  }
  main.inert = overlay;
  if (isHome) homeControl.setAttribute('aria-current', 'page');
  else homeControl.removeAttribute('aria-current');
  navLinks.forEach(link => {
    if (link.dataset.destination === currentActivity?.id) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  });
  keepCurrentDestinationVisible();
}

function preparePresentation() {
  presentationSnapshot = currentActivity ? {
    route: location.hash || '#/',
    scroll: overlayScrollPosition || { x: window.scrollX, y: window.scrollY },
    railScroll: destinationList.scrollTop,
    focus: document.activeElement
  } : null;
  // Clearing the overlay also removes its fixed-body scroll lock and main.inert.
  // The same activity DOM, including its future internal controls, stays mounted.
  if (currentActivity) setMenuOpen(false);
}

function restorePresentation(restore) {
  const snapshot = presentationSnapshot;
  presentationSnapshot = null;
  if (!restore || !snapshot || snapshot.route !== (location.hash || '#/')) return;
  const restorePosition = () => {
    if (presentation.isActive() || snapshot.route !== (location.hash || '#/')) return;
    destinationList.scrollTop = snapshot.railScroll;
    const focus = snapshot.focus?.isConnected && snapshot.focus.getClientRects().length
      ? snapshot.focus : main;
    focus.focus({ preventScroll: true });
    window.scrollTo(snapshot.scroll.x, snapshot.scroll.y);
  };
  restorePosition();
  requestAnimationFrame(restorePosition);
}

function setMenuOpen(open, restoreFocus = false) {
  menuOpen = open;
  updateNavigation();
  if (open && !isPermanentRail()) closeButton.focus({ preventScroll: true });
  else if (restoreFocus && !isPermanentRail()) toggle.focus({ preventScroll: true });
}

toggle.addEventListener('click', () => setMenuOpen(!menuOpen));
closeButton.addEventListener('click', () => setMenuOpen(false, true));
navigationRegion.addEventListener('click', event => {
  if (event.target.closest('a')) setMenuOpen(false);
});
document.addEventListener('keydown', event => {
  if (!menuOpen || isPermanentRail()) return;
  if (event.key === 'Escape') {
    event.preventDefault();
    setMenuOpen(false, true);
  }
  if (event.key === 'Tab') {
    const focusable = [...navigationRegion.querySelectorAll('a, button')]
      .filter(element => element.getClientRects().length && !element.disabled);
    const first = focusable[0], last = focusable.at(-1);
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault(); last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault(); first.focus();
    }
  }
});
document.addEventListener('click', event => {
  if (menuOpen && !navigationRegion.contains(event.target)) setMenuOpen(false, true);
});
skipLink.addEventListener('click', event => {
  event.preventDefault();
  setMenuOpen(false);
  main.focus();
});

function renderHome() {
  main.className = 'home-main';
  main.innerHTML = `
    <header class="home-title">
      <h1 tabindex="-1"><img class="protected-title" src="${GLOBAL_ASSETS.title}" width="650" height="215" alt="The Haunted Realm"></h1>
    </header>
    <section class="home-destinations" aria-label="Explore the activities">
      ${ACTIVITIES.map(activity => `
        <a class="scene-destination" href="${routeFor(activity)}" aria-label="${escapeHtml(activity.name)}" data-home-destination="${escapeHtml(activity.id)}">
          <span class="scene-space"><img class="activity-scene" src="${escapeHtml(activity.scene)}" alt="" loading="eager"></span>
          <span class="scene-name">
            <img class="name-rest" src="${escapeHtml(activity.lettering)}" alt="">
            <img class="name-focus" src="${escapeHtml(activity.letteringFocus)}" alt="">
          </span>
        </a>`).join('')}
    </section>`;
  updateHomeComposition();
}

function updateHomeComposition() {
  if (!isHome) return;
  const choices = main.querySelector('.home-destinations');
  if (!choices) return;
  const columns = Number.parseInt(getComputedStyle(choices).getPropertyValue('--home-columns'), 10) || 3;
  choices.style.setProperty('--home-row-count', Math.ceil(ACTIVITIES.length / columns));
}

function renderActivity(activity) {
  if (activity.id === 'echoes-of-the-past') {
    main.className = 'activity-main echoes-main';
    main.innerHTML = '<header class="activity-page-heading"><h1 tabindex="-1">Echoes of the Past</h1></header><section class="activity-stage"></section>';
    activityController = mountEchoes(main.querySelector('.activity-stage'));
    return;
  }
  main.className = 'activity-main';
  main.innerHTML = `
    <header class="activity-page-heading">
      <p class="shell-status">Page shell</p>
      <h1 tabindex="-1">${escapeHtml(activity.name)}</h1>
    </header>
    <section class="content-space activity-stage" aria-labelledby="content-area-heading">
      <h2 id="content-area-heading">Activity content area</h2>
      <p>Content and interactions will be developed after separate approval.</p>
    </section>`;
}

function renderUnknown() {
  main.className = 'activity-main';
  main.innerHTML = '<header class="activity-page-heading"><h1 tabindex="-1">Destination not found</h1></header><section class="content-space"><p>This destination is not in the current activity list.</p><a href="#/">Return Home</a></section>';
}

function renderRoute(initial = false) {
  // Browser history/direct route changes leave the old presentation before
  // replacing its activity. Entering or exiting presentation never changes URL.
  if (presentation.isActive()) presentation.leaveForRoute();
  activityController?.destroy();
  activityController = null;
  const hash = location.hash || '#/';
  const match = /^#\/activities\/([^/]+)$/.exec(hash);
  let activityId = null;
  if (match) {
    try { activityId = decodeURIComponent(match[1]); }
    catch { activityId = null; }
  }
  currentActivity = destinations.get(activityId) || null;
  isHome = hash === '#/' || hash === '#';
  menuOpen = false;
  document.body.classList.toggle('home-view', isHome);
  document.body.classList.toggle('activity-view', !isHome);
  if (isHome) renderHome();
  else if (currentActivity) renderActivity(currentActivity);
  else renderUnknown();
  updateNavigation();
  const name = isHome ? 'The Haunted Realm' : currentActivity?.name || 'Destination not found';
  document.title = isHome ? name : `${name} | The Haunted Realm`;
  announcement.textContent = `Opened ${name}`;
  window.scrollTo(0, 0);
  if (!initial || currentActivity?.id === 'echoes-of-the-past') {
    (main.querySelector('.echoes-stage') || main.querySelector('h1'))?.focus({ preventScroll: true });
  }
}

narrow.addEventListener('change', () => { menuOpen = false; updateNavigation(); });
window.addEventListener('resize', () => { updateNavigation(); updateHomeComposition(); });
window.addEventListener('hashchange', () => renderRoute());
const presentation = initializePresentation(() => updateNavigation(), {
  beforeEnter: preparePresentation,
  afterExit: restorePresentation
});
renderRoute(true);
