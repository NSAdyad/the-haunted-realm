import { ECHOES_SLIDES } from './echoes-content.js?v=activity-1';
import { createSlideController, keyboardDirection, swipeDirection } from './echoes-controller.js?v=activity-1';

const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const items = (entries, className) => entries?.length ? `<dl class="${className}">${entries.map(entry => `<div><dt>${escape(entry.label)}</dt><dd>${entry.text}</dd></div>`).join('')}</dl>` : '';

function slideMarkup(slide, index) {
  const images = (slide.images || []).map(image => `<figure class="echoes-image"><img src="${escape(image.src)}" alt="${escape(image.alt)}" decoding="async">${image.caption ? `<figcaption>${escape(image.caption)}</figcaption>` : ''}</figure>`).join('');
  const profiles = slide.comparison?.length ? `<div class="echoes-comparison">${slide.comparison.map((profile,i) => `<section><h3>${escape(profile.label)}</h3>${(slide.images || [])[i] ? `<img class="echoes-record-image" src="${escape(slide.images[i].src)}" alt="${escape(slide.images[i].alt)}">` : ''}<p class="echoes-measure">${escape(profile.weight)}</p><p>${escape(profile.name)}</p><p>${escape(profile.location)}<br>${escape(profile.date)}</p>${profile.note ? `<p class="echoes-record-note">${escape(profile.note)}</p>` : ''}</section>`).join('')}</div>` : '';
  return `<article class="echoes-slide echoes-layout-${escape(slide.layout)}" data-slide-index="${index}" data-source="${escape(slide.source || 'opening')}" ${index ? 'hidden' : ''} aria-labelledby="echoes-heading-${index}">
    <header class="echoes-slide-heading"><span class="echoes-chapter">${index ? `Echoes of the Past · ${String(index).padStart(2,'0')}` : 'The Haunted Realm'}</span><h2 id="echoes-heading-${index}">${escape(slide.title)}</h2>${slide.subtitle ? `<p class="echoes-subtitle">${escape(slide.subtitle)}</p>` : ''}</header>
    <div class="echoes-slide-body ${profiles ? 'has-comparison' : ''}">
      ${profiles || `<div class="echoes-copy">${(slide.paragraphs || []).map(text => `<p>${text}</p>`).join('')}${items(slide.timeline,'echoes-timeline')}${items(slide.facts,'echoes-facts')}${items(slide.ingredients,'echoes-ingredients')}</div><div class="echoes-visual">${images}${items(slide.flow,'echoes-flow')}${items(slide.cycle,'echoes-cycle')}</div>`}
      ${profiles ? `<div class="echoes-record-summary">${(slide.paragraphs || []).map(text => `<p>${text}</p>`).join('')}</div>` : ''}
    </div>
  </article>`;
}

// One mounted stage and one controller survive shared Presentation Mode changes.
export function mountEchoes(stage) {
  stage.className = 'content-space activity-stage echoes-stage';
  stage.setAttribute('aria-label','Echoes of the Past history presentation');
  stage.setAttribute('tabindex','0');
  stage.innerHTML = `<div class="echoes-deck">${ECHOES_SLIDES.map(slideMarkup).join('')}</div>
    <button type="button" class="echoes-zone echoes-zone-left" aria-label="Previous screen"><span>Previous</span></button>
    <button type="button" class="echoes-zone echoes-zone-right" aria-label="Next screen"><span>Next</span></button>
    <footer class="echoes-controls"><span class="echoes-guidance">Tap either side · Left / Right keys</span><button type="button" class="echoes-position" aria-label="Choose a screen" aria-expanded="false" aria-controls="echoes-overview">1 / ${ECHOES_SLIDES.length}</button><span class="echoes-end" hidden>End of the historical journey</span></footer>
    <section class="echoes-overview" id="echoes-overview" role="dialog" aria-modal="true" aria-label="Choose a screen" hidden><header><h3>Echoes of the Past</h3><button type="button" class="echoes-close-overview">Close overview</button></header><ol>${ECHOES_SLIDES.map((slide,i) => `<li><button type="button" data-go-slide="${i}"><span>${String(i+1).padStart(2,'0')}</span> ${escape(slide.title)}</button></li>`).join('')}</ol></section>
    <p class="visually-hidden echoes-announcement" role="status" aria-live="polite" aria-atomic="true"></p>`;
  const slides = [...stage.querySelectorAll('.echoes-slide')];
  const deck = stage.querySelector('.echoes-deck');
  const position = stage.querySelector('.echoes-position');
  const previous = stage.querySelector('.echoes-zone-left');
  const next = stage.querySelector('.echoes-zone-right');
  const overview = stage.querySelector('.echoes-overview');
  const footer = stage.querySelector('.echoes-controls');
  const cleanup = new AbortController();
  let overviewOpen = false;
  let gesture = null;
  let suppressClickUntil = 0;
  let presenting = false;
  let shown = 0;
  const controller = createSlideController(slides.length, index => {
    slides[shown].hidden = true;
    shown = index;
    slides[index].hidden = false;
    slides[index].querySelector('.echoes-slide-body').scrollTop = 0;
    update();
    stage.querySelector('.echoes-announcement').textContent = `${index+1} of ${slides.length}. ${ECHOES_SLIDES[index].title}`;
  });
  function update() {
    const index = controller.getIndex();
    stage.dataset.slideIndex = String(index);
    position.textContent = `${index+1} / ${slides.length}`;
    position.setAttribute('aria-label',`Choose a screen, current ${index+1} of ${slides.length}`);
    previous.disabled = index === 0;
    next.disabled = index === slides.length-1;
    stage.querySelector('.echoes-end').hidden = index !== slides.length-1;
    overview.querySelectorAll('[data-go-slide]').forEach(button => {
      if(Number(button.dataset.goSlide) === index) button.setAttribute('aria-current','step');
      else button.removeAttribute('aria-current');
    });
  }
  function toggleOverview(open, restore = true) {
    overviewOpen = open;
    overview.hidden = !open;
    position.setAttribute('aria-expanded',String(open));
    deck.inert = open;
    previous.inert = next.inert = footer.inert = open;
    if(open) {
      const selected = overview.querySelector(`[data-go-slide="${controller.getIndex()}"]`);
      selected.focus({preventScroll:true});
      selected.scrollIntoView({block:'nearest'});
    }
    else if(restore) position.focus({preventScroll:true});
  }
  const on = (target,type,handler) => target.addEventListener(type,handler,{signal:cleanup.signal});
  on(previous,'click', event => {event.stopPropagation(); controller.previousSlide(); stage.focus({preventScroll:true});});
  on(next,'click', event => {event.stopPropagation(); controller.nextSlide(); stage.focus({preventScroll:true});});
  on(position,'click', () => toggleOverview(!overviewOpen));
  on(stage.querySelector('.echoes-close-overview'),'click', () => toggleOverview(false));
  on(overview,'click',event => {
    const target = event.target.closest('[data-go-slide]');
    if(!target) return;
    controller.goToSlide(Number(target.dataset.goSlide));
    toggleOverview(false,false);
    stage.focus({preventScroll:true});
  });
  on(stage,'click',event => {
    if(overviewOpen || performance.now() < suppressClickUntil || event.target.closest('button,a,input,textarea,select,[contenteditable],.echoes-controls,.echoes-overview')) return;
    if(window.getSelection()?.toString()) return;
    const bounds = stage.getBoundingClientRect();
    if(event.clientX < bounds.left+bounds.width/2) controller.previousSlide();
    else controller.nextSlide();
    stage.focus({preventScroll:true});
  });
  on(stage,'keydown',event => {
    if(overviewOpen && event.key === 'Escape') {
      event.preventDefault();
      event.stopPropagation();
      toggleOverview(false);
    }
  });
  on(document,'keydown',event => {
    if(!stage.contains(document.activeElement) && document.activeElement !== stage.parentElement) return;
    if(overviewOpen) {
      if(event.key === 'Escape') {event.preventDefault(); event.stopImmediatePropagation(); toggleOverview(false);}
      else if(event.key === 'Tab') {
        const buttons = [...overview.querySelectorAll('button')];
        const first = buttons[0], last = buttons.at(-1);
        if(event.shiftKey && document.activeElement === first) {event.preventDefault();last.focus();}
        else if(!event.shiftKey && document.activeElement === last) {event.preventDefault();first.focus();}
      }
      return;
    }
    const direction = keyboardDirection(event);
    if(direction) {event.preventDefault();direction === 'next' ? controller.nextSlide() : controller.previousSlide();}
  });
  on(stage,'pointerdown',event => {
    if(event.pointerType !== 'touch' || overviewOpen || event.target.closest('button,a,input,textarea,select,[contenteditable],.echoes-controls')) {gesture=null;return;}
    gesture = {x:event.clientX,y:event.clientY,pointerType:event.pointerType,pointerId:event.pointerId};
  });
  on(stage,'pointerup',event => {
    if(!gesture) return;
    if(event.target.closest('button,a,input,textarea,select,[contenteditable],.echoes-controls')) {gesture=null;return;}
    const direction = swipeDirection(gesture,{x:event.clientX,y:event.clientY,pointerType:event.pointerType,pointerId:event.pointerId});
    gesture = null;
    if(direction) {suppressClickUntil=performance.now()+500; direction === 'next' ? controller.nextSlide() : controller.previousSlide(); stage.focus({preventScroll:true});}
  });
  on(stage,'pointercancel',() => {gesture=null;});
  update();
  return {
    ...controller,
    onPresentationChange(active) {
      if(active === presenting) return;
      presenting=active;
      // Entering from a site control gives keyboard teaching control to the stage.
      if(active) {
        queueMicrotask(() => {
          if(presenting && stage.isConnected && document.activeElement?.matches('.presentation-toggle')) {
            const focus = overviewOpen ? overview.querySelector(`[data-go-slide="${controller.getIndex()}"]`) : stage;
            focus.focus({preventScroll:true});
          }
        });
      }
      if(!active && overviewOpen) toggleOverview(false,false);
    },
    destroy() {cleanup.abort();}
  };
}
