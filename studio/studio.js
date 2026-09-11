'use strict';
// Original, deterministic synthesis experiment. No model or external audio service.
const $ = (id) => document.getElementById(id);
const names = { piano: 'Piano', bass: 'Bass', drums: 'Drums', strings: 'Strings' };
const colors = { piano: ['#edf0e6', '#929e7d'], bass: ['#eee9f4', '#ab97c3'], drums: ['#f4e9df', '#cba780'], strings: ['#e6eef1', '#8baab7'] };
const chords = [[48, 52, 55, 59], [45, 48, 52, 55], [41, 45, 48, 52], [43, 47, 50, 52]];
const clone = (x) => JSON.parse(JSON.stringify(x));
const storageKey = 'maestro-music-kitchen-v1';
const defaultProject = () => ({ version: 1, name: 'Evening sketch', tempo: 92,
  tracks: Object.keys(names).map((id) => ({ id, locked: id === 'piano', muted: false,
    phrases: Array.from({ length: 4 }, (_, i) => ({ density: id === 'drums' ? .6 : .45,
      contour: [.28, .38, .56, .48, .7, .56, .42, .3].map((v) => Math.min(.95, v + i * .015)), rhythm: null })) })) });
let project = defaultProject();
try {
  const saved = JSON.parse(localStorage.getItem(storageKey));
  if (saved?.version === 1 && typeof saved.name === 'string' && Number.isFinite(saved.tempo)
      && saved.tempo >= 50 && saved.tempo <= 160 && saved.tracks?.length === 4
      && saved.tracks.every((t, i) => t.id === Object.keys(names)[i] && t.phrases?.length === 4
        && t.phrases.every((p) => Number.isFinite(p.density) && p.density >= .15 && p.density <= 1
          && p.contour?.length === 8 && p.contour.every((v) => Number.isFinite(v) && v >= 0 && v <= 1)
          && (p.rhythm === null || (Array.isArray(p.rhythm) && p.rhythm.length > 0
            && p.rhythm.every((n) => Number.isInteger(n) && n >= 0 && n < 32)))))) project = saved;
} catch { /* Private browsing or a stale project should never prevent playback. */ }
let selection = { track: 'bass', phrase: 2 };
let draft, undoStack = [], previous = null, comparing = false, taps = [];
let audio = null, master = null, playing = false, timer = null, startTime = 0, pausedBeat = 0, scheduledBeat = 0, playbackTempo = project.tempo;
let activeVoices = [];

function announce(text) { $('announcement').textContent = text; }
function save() {
  try { localStorage.setItem(storageKey, JSON.stringify(project)); $('save-state').textContent = 'Saved on this device'; }
  catch { $('save-state').textContent = 'Use Project to save a copy'; }
}
function track(id, source = project) { return source.tracks.find((t) => t.id === id); }
function remember() { undoStack.push(clone(project)); if (undoStack.length > 30) undoStack.shift(); previous = clone(project); comparing = false; }
function refreshComparison() {
  $('before').disabled = !previous;
  $('before').setAttribute('aria-pressed', String(comparing));
  $('after').setAttribute('aria-pressed', String(!comparing));
  $('undo').disabled = !undoStack.length;
}
function recipeText() {
  return `phrase ${selection.track} [${selection.phrase * 2 + 1}:${selection.phrase * 2 + 2}] {\n  density ${draft.density.toFixed(2)}\n  contour [${draft.contour.map((x) => x.toFixed(2)).join(', ')}]\n  rhythm ${draft.rhythm ? '[' + draft.rhythm.join(', ') + ']' : 'auto'}\n}`;
}
function drawContour() {
  const points = draft.contour.map((v, i) => [10 + i * 260 / 7, 115 - v * 100]);
  const d = points.map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(1)},${y.toFixed(1)}`).join(' ');
  $('contour-line').setAttribute('d', d);
  $('contour-fill').setAttribute('d', `${d} L270,130 L10,130 Z`);
  $('contour-points').innerHTML = points.map(([x, y]) => `<circle cx="${x}" cy="${y}" r="3"/>`).join('');
  $('density').value = Math.round(draft.density * 100);
  $('density-value').value = `${Math.round(draft.density * 100)}%`;
  $('recipe').value = recipeText();
}
function loadSelection() {
  const selected = track(selection.track);
  draft = clone(selected.phrases[selection.phrase]);
  $('selected-name').textContent = `${names[selected.id]} · bars ${selection.phrase * 2 + 1}–${selection.phrase * 2 + 2}`;
  $('selected-description').textContent = selected.locked ? 'This part is protected. Unpin it on the track to edit.' : 'Try giving this phrase somewhere to go.';
  $('shape-controls').disabled = selected.locked;
  $('rhythm-controls').disabled = selected.locked;
  $('apply').disabled = selected.locked;
  $('run-recipe').disabled = selected.locked;
  taps = []; renderTaps(); drawContour();
}

// Every phrase compiles to the same explicit events used by the canvas and synthesizer.
function phraseEvents(id, phrase, config) {
  const events = [], harmony = chords[phrase];
  const count = Math.round(3 + config.density * 10);
  const offsets = config.rhythm || Array.from({ length: count }, (_, i) => Math.floor(i * 32 / count));
  if (id === 'piano') {
    offsets.forEach((step, i) => events.push({ beat: phrase * 8 + step / 4, duration: .65,
      midi: harmony[i % 4] + 12 + (config.contour[i % 8] > .65 ? 12 : 0), velocity: .55, kind: id }));
    [0, 4].forEach((b) => harmony.slice(0, 3).forEach((n) => events.push({ beat: phrase * 8 + b, duration: 2.4, midi: n, velocity: .27, kind: id })));
  } else if (id === 'bass') {
    offsets.forEach((step, i) => events.push({ beat: phrase * 8 + step / 4, duration: .6,
      midi: harmony[Math.min(3, Math.floor(config.contour[i % 8] * 4))] - 12, velocity: .68, kind: id }));
  } else if (id === 'strings') {
    const stringSteps = config.rhythm || (config.density > .7 ? [0, 8, 16, 24] : [0, 16]);
    stringSteps.forEach((step, i) => harmony.slice(1, config.density > .4 ? 4 : 3).forEach((n) => events.push({ beat: phrase * 8 + step / 4,
      duration: config.density > .7 ? 1.9 : 3.8, midi: n + 12 + (config.contour[i % 8] > .7 ? 12 : 0), velocity: .2, kind: id })));
  } else {
    const accents = config.rhythm || [0, 6, 16, 22];
    accents.forEach((step) => events.push({ beat: phrase * 8 + step / 4, duration: .2, midi: 36, velocity: .65, kind: 'kick' }));
    [4, 12, 20, 28].forEach((step) => events.push({ beat: phrase * 8 + step / 4, duration: .15, midi: 38, velocity: .35, kind: 'snare' }));
    const every = config.density > .7 ? 1 : config.density > .35 ? 2 : 4;
    for (let i = 0; i < 32; i += every) events.push({ beat: phrase * 8 + i / 4, duration: .06, midi: 42,
      velocity: .1 + config.contour[Math.floor(i / 4)] * .15, kind: 'hat' });
  }
  return events;
}
function allEvents(source = project) {
  return source.tracks.filter((t) => !t.muted).flatMap((t) => t.phrases.flatMap((p, i) => phraseEvents(t.id, i, p))).sort((a, b) => a.beat - b.beat);
}
function clipSvg(id, i, config) {
  const events = phraseEvents(id, i, config);
  const pitches = events.map((e) => e.midi), lo = Math.min(...pitches), hi = Math.max(...pitches);
  return `<svg viewBox="0 0 120 36" preserveAspectRatio="none" aria-hidden="true">${events.map((e) => {
    const x = (e.beat - i * 8) / 8 * 116;
    const y = 30 - (e.midi - lo) / Math.max(12, hi - lo) * 27;
    return `<rect x="${x}" y="${y}" width="${Math.max(2, e.duration / 8 * 100)}" height="2.8" rx="1.2" fill="currentColor" opacity="${e.velocity + .22}"/>`;
  }).join('')}</svg>`;
}
function renderTracks() {
  const source = comparing ? previous : project;
  $('tracks').innerHTML = source.tracks.map((t) => `<div class="track-row ${t.muted ? 'muted-track' : ''}" style="--clip-bg:${colors[t.id][0]};--clip-ink:${colors[t.id][1]}">
    <div class="track-label"><strong>${names[t.id]}</strong><small>${t.id === 'piano' ? 'Original demo motif' : t.id === 'drums' ? 'A soft pocket' : t.id === 'strings' ? 'A little atmosphere' : 'A moving foundation'}</small>
    <div class="track-buttons"><button data-mute="${t.id}" aria-label="${t.muted ? 'Unmute' : 'Mute'} ${t.id}" aria-pressed="${t.muted}">${t.muted ? 'Muted' : 'Mute'}</button><button data-lock="${t.id}" aria-label="${t.locked ? 'Unpin' : 'Pin'} ${t.id}" aria-pressed="${t.locked}">${t.locked ? 'Pinned' : 'Pin'}</button></div></div>
    <div class="track-clips">${t.phrases.map((p, i) => `<button class="clip ${selection.track === t.id && selection.phrase === i ? 'selected' : ''}" data-track="${t.id}" data-phrase="${i}" aria-pressed="${selection.track === t.id && selection.phrase === i}" aria-label="Select ${t.id}, bars ${i * 2 + 1} to ${i * 2 + 2}"><small>${t.id === 'piano' ? ['Cmaj7', 'Am7', 'Fmaj7', 'G6'][i] : `Phrase ${i + 1}`}</small>${clipSvg(t.id, i, p)}</button>`).join('')}</div></div>`).join('');
  $('tracks').querySelectorAll('[data-track]').forEach((button) => button.addEventListener('click', () => {
    selection = { track: button.dataset.track, phrase: Number(button.dataset.phrase) };
    loadSelection(); renderTracks();
    announce(`Selected ${names[selection.track]}, bars ${selection.phrase * 2 + 1}–${selection.phrase * 2 + 2}.`);
    if (window.innerWidth <= 650) document.querySelector('.inspector').scrollIntoView({ behavior: 'auto', block: 'start' });
  }));
  $('tracks').querySelectorAll('[data-mute]').forEach((button) => button.addEventListener('click', () => {
    remember(); const t = track(button.dataset.mute); t.muted = !t.muted; changed();
  }));
  $('tracks').querySelectorAll('[data-lock]').forEach((button) => button.addEventListener('click', () => {
    remember(); const t = track(button.dataset.lock); t.locked = !t.locked; changed(); loadSelection();
    announce(`${names[t.id]} ${t.locked ? 'protected from phrase edits' : 'is now editable'}.`);
  }));
}
function changed() { save(); refreshComparison(); renderTracks(); if (playing) restartPlayback(); }
function applyDraft(startPlayback = true) {
  if (track(selection.track).locked) { announce('This part is pinned. Unpin it before editing.'); return; }
  remember(); track(selection.track).phrases[selection.phrase] = clone(draft); changed();
  const message = `${names[selection.track]}, bars ${selection.phrase * 2 + 1}–${selection.phrase * 2 + 2} changed. Other phrases and parts preserved.`;
  $('change-description').textContent = message; announce(message);
  if (startPlayback) { stopPlayback(); pausedBeat = selection.phrase * 8; play(); }
}

// Audio engine shared by interactive playback and offline WAV rendering.
function voice(ctx, output, event, when, secondsPerBeat) {
  const frequency = 440 * 2 ** ((event.midi - 69) / 12);
  const gain = ctx.createGain(); gain.connect(output);
  const duration = event.duration * secondsPerBeat;
  let source;
  if (event.kind === 'hat' || event.kind === 'snare') {
    const length = Math.ceil(ctx.sampleRate * .18), buffer = ctx.createBuffer(1, length, ctx.sampleRate), samples = buffer.getChannelData(0);
    let seed = 41;
    for (let i = 0; i < length; i++) { seed = (seed * 16807) % 2147483647; samples[i] = (seed / 2147483647 * 2 - 1); }
    source = ctx.createBufferSource(); source.buffer = buffer;
    const filter = ctx.createBiquadFilter(); filter.type = 'highpass'; filter.frequency.value = event.kind === 'hat' ? 6500 : 1800;
    source.connect(filter); filter.connect(gain);
  } else {
    source = ctx.createOscillator(); source.type = event.kind === 'strings' ? 'triangle' : event.kind === 'bass' ? 'sine' : 'triangle';
    source.frequency.setValueAtTime(event.kind === 'kick' ? 130 : frequency, when);
    if (event.kind === 'kick') source.frequency.exponentialRampToValueAtTime(42, when + .13);
    source.connect(gain);
  }
  const attack = event.kind === 'strings' ? .13 : .005;
  const end = when + Math.max(duration, attack + .03) + (event.kind === 'strings' ? .2 : .08);
  gain.gain.setValueAtTime(.0001, when);
  gain.gain.exponentialRampToValueAtTime(Math.max(.001, event.velocity), when + attack);
  gain.gain.exponentialRampToValueAtTime(.0001, end);
  source.start(when); source.stop(end + .02);
  if (ctx === audio) {
    activeVoices.push({ source, gain });
    source.onended = () => { gain.disconnect(); source.disconnect(); activeVoices = activeVoices.filter((v) => v.source !== source); };
  }
}
function ensureAudio() {
  if (!audio) {
    const Audio = window.AudioContext || window.webkitAudioContext;
    if (!Audio) throw new Error('Web Audio is unavailable in this browser.');
    audio = new Audio(); master = audio.createGain(); master.gain.value = .19; master.connect(audio.destination);
  }
  return audio.resume();
}
function silence() {
  activeVoices.forEach(({ source, gain }) => { try { gain.gain.cancelScheduledValues(audio.currentTime); gain.gain.setTargetAtTime(.0001, audio.currentTime, .008); source.stop(audio.currentTime + .04); } catch { /* Already ended. */ } });
  activeVoices = [];
}
function currentBeat() { return playing ? (audio.currentTime - startTime) / (60 / playbackTempo) : pausedBeat; }
function tick() {
  if (!playing) return;
  const source = comparing ? previous : project, spb = 60 / playbackTempo;
  const now = currentBeat(), until = now + .14 / spb;
  const events = allEvents(source);
  for (let cycle = Math.floor(scheduledBeat / 32); cycle <= Math.floor(until / 32); cycle++) {
    events.forEach((e) => {
      const beat = e.beat + cycle * 32;
      if (beat >= scheduledBeat && beat < until) voice(audio, master, e, Math.max(audio.currentTime, startTime + beat * spb), spb);
    });
  }
  scheduledBeat = until;
  const beat = ((now % 32) + 32) % 32;
  $('position').innerHTML = `${String(Math.floor(beat / 4) + 1).padStart(2, '0')} <span>/ 08</span>`;
  const inner = document.querySelector('.timeline-inner');
  $('playhead').style.left = `${116 + beat / 32 * (inner.clientWidth - 132)}px`;
}
async function play() {
  if (playing) { pausedBeat = currentBeat() % 32; stopPlayback(false); return; }
  try {
    await ensureAudio(); if (playing) return;
    playbackTempo = (comparing ? previous : project).tempo;
    startTime = audio.currentTime - pausedBeat * (60 / playbackTempo); scheduledBeat = pausedBeat; playing = true;
    $('play').textContent = 'Ⅱ'; $('play').setAttribute('aria-label', 'Pause arrangement'); $('playhead').hidden = false;
    tick(); timer = setInterval(tick, 25);
  } catch (e) { announce(`Cannot start audio: ${e.message}`); }
}
function stopPlayback(reset = true) {
  playing = false; clearInterval(timer); silence(); $('play').textContent = '▶'; $('play').setAttribute('aria-label', 'Play arrangement');
  $('playhead').hidden = true;
  if (reset) { pausedBeat = 0; $('position').innerHTML = '01 <span>/ 08</span>'; }
}
function restartPlayback() { pausedBeat = currentBeat() % 32; stopPlayback(false); play(); }

function renderTaps() {
  const steps = tapSteps();
  $('rhythm-dots').innerHTML = Array.from({ length: 16 }, (_, i) => `<i class="${steps.some((s) => s % 16 === i) ? 'active' : ''}"></i>`).join('');
  $('use-rhythm').disabled = taps.length < 2;
}
function tapSteps() { return [...new Set(taps.map((t) => Math.round((t - taps[0]) / (60000 / project.tempo) * 4) % 32))].sort((a, b) => a - b); }
async function tap() {
  if (track(selection.track).locked) { announce('Select an unpinned part to demonstrate a rhythm.'); return; }
  const now = performance.now();
  if (taps.length && now - taps[0] > 8 * 60000 / project.tempo) taps = [];
  taps.push(now); renderTaps();
  try { await ensureAudio(); voice(audio, master, { kind: 'hat', midi: 42, velocity: .3, duration: .08 }, audio.currentTime, 1); } catch { /* Visual tapping still works. */ }
}
function curve(type) {
  if (track(selection.track).locked) { announce('Select an unpinned phrase first.'); return; }
  draft.contour = Array.from({ length: 8 }, (_, i) => type === 'rise' ? .15 + i * .1 : type === 'fall' ? .85 - i * .1 : .45);
  drawContour(); announce('Contour prepared. Choose “Hear this change” to apply it.');
}
function direction(text) {
  if (track(selection.track).locked) { announce('Select an unpinned phrase first.'); return; }
  const lower = text.toLowerCase(); let recognized = false;
  if (/sparse|space|less|gentl|quiet/.test(lower)) { draft.density = .25; recognized = true; }
  if (/dense|busy|full|more notes/.test(lower)) { draft.density = .85; recognized = true; }
  if (/ris|upward/.test(lower)) { curve('rise'); recognized = true; }
  if (/fall|downward/.test(lower)) { curve('fall'); recognized = true; }
  if (!recognized) { announce('This prototype understands sparse, dense, rising, and falling. General AI prompting is not connected yet.'); return; }
  drawContour(); applyDraft();
}

$('ruler').innerHTML = Array.from({ length: 8 }, (_, i) => `<span>${i + 1}</span>`).join('');
$('project-name').value = project.name; $('tempo').value = project.tempo;
$('project-name').addEventListener('change', () => { remember(); project.name = $('project-name').value.trim() || 'Untitled sketch'; $('project-name').value = project.name; changed(); });
$('tempo').addEventListener('change', () => {
  const n = Number($('tempo').value);
  if (!Number.isFinite(n) || n < 50 || n > 160) { $('tempo').value = project.tempo; announce('Choose a tempo between 50 and 160 BPM.'); return; }
  const wasPlaying = playing; if (wasPlaying) stopPlayback(); remember(); project.tempo = n; changed(); if (wasPlaying) play();
});
$('play').addEventListener('click', play); $('stop').addEventListener('click', () => stopPlayback());
$('apply').addEventListener('click', () => applyDraft());
$('density').addEventListener('input', () => { draft.density = Number($('density').value) / 100; drawContour(); });
document.querySelectorAll('[data-curve]').forEach((b) => b.addEventListener('click', () => curve(b.dataset.curve)));
let drawing = false;
function pointerContour(e) {
  if (!drawing || track(selection.track).locked) return;
  const r = $('contour').getBoundingClientRect();
  const i = Math.max(0, Math.min(7, Math.round((e.clientX - r.left) / r.width * 7)));
  draft.contour[i] = Math.max(.05, Math.min(.95, 1 - (e.clientY - r.top) / r.height)); drawContour();
}
$('contour').addEventListener('pointerdown', (e) => { drawing = true; $('contour').setPointerCapture(e.pointerId); pointerContour(e); });
$('contour').addEventListener('pointermove', pointerContour);
['pointerup', 'pointercancel', 'lostpointercapture'].forEach((name) => $('contour').addEventListener(name, () => { drawing = false; }));
$('tap').addEventListener('pointerdown', (e) => { if (e.button === 0) { e.preventDefault(); tap(); } });
$('tap').addEventListener('click', (e) => { if (e.detail === 0) tap(); });
$('clear-taps').addEventListener('click', () => { taps = []; renderTaps(); });
$('use-rhythm').addEventListener('click', () => { draft.rhythm = tapSteps(); drawContour(); announce('Your tapped timing is in the recipe. Choose “Hear this change” to apply it.'); });
$('direction-form').addEventListener('submit', (e) => { e.preventDefault(); direction($('direction').value); });
document.querySelectorAll('[data-direction]').forEach((b) => b.addEventListener('click', () => direction(b.dataset.direction)));
document.querySelectorAll('[data-preset]').forEach((b) => b.addEventListener('click', () => {
  if (track(selection.track).locked) { announce('Select an unpinned phrase to use an ingredient.'); return; }
  if (b.dataset.preset === 'space') draft.density = .2; else curve('rise'); drawContour();
  announce('Ingredient added to this phrase’s recipe. Choose “Hear this change” to listen.');
}));
$('before').addEventListener('click', () => { if (!previous) return; comparing = true; refreshComparison(); renderTracks(); if (playing) restartPlayback(); announce('Listening to the version before your last change.'); });
$('after').addEventListener('click', () => { comparing = false; refreshComparison(); renderTracks(); if (playing) restartPlayback(); announce('Listening to the current version.'); });
$('undo').addEventListener('click', () => { if (!undoStack.length) return; previous = clone(project); project = undoStack.pop(); comparing = false;
  $('project-name').value = project.name; $('tempo').value = project.tempo; changed(); loadSelection(); announce('Last change undone.'); });
$('reset').addEventListener('click', () => { remember(); stopPlayback(); project = defaultProject(); selection = { track: 'bass', phrase: 2 };
  $('project-name').value = project.name; $('tempo').value = project.tempo; changed(); loadSelection(); announce('Original demo restored. Undo is available.'); });
document.addEventListener('keydown', (e) => {
  if (/INPUT|TEXTAREA|SELECT|BUTTON|SUMMARY/.test(e.target.tagName) || e.ctrlKey || e.metaKey || e.altKey || e.repeat) return;
  if (e.code === 'Space') { e.preventDefault(); play(); }
  if (e.key.toLowerCase() === 't') { e.preventDefault(); tap(); }
});
$('run-recipe').addEventListener('click', () => {
  try {
    const text = $('recipe').value.trim();
    const match = text.match(/^phrase (piano|bass|drums|strings) \[(\d+):(\d+)\] \{\s*density ([\d.]+)\s*contour (\[[\d.,\s]+\])\s*rhythm (auto|\[[\d,\s]+\])\s*\}$/);
    if (!match) throw new Error('Use phrase, density, contour, and rhythm in the displayed recipe format.');
    const start = Number(match[2]), end = Number(match[3]), density = Number(match[4]);
    const contour = JSON.parse(match[5]), rhythm = match[6] === 'auto' ? null : JSON.parse(match[6]);
    if (![1, 3, 5, 7].includes(start) || end !== start + 1) throw new Error('Choose a two-bar phrase: 1:2, 3:4, 5:6, or 7:8.');
    if (!Number.isFinite(density) || density < .15 || density > 1) throw new Error('Density must be between 0.15 and 1.');
    if (contour.length !== 8 || contour.some((x) => !Number.isFinite(x) || x < 0 || x > 1)) throw new Error('Contour needs eight values between 0 and 1.');
    if (rhythm && (!rhythm.length || rhythm.length > 32 || rhythm.some((x) => !Number.isInteger(x) || x < 0 || x > 31))) throw new Error('Rhythm needs integer steps from 0 to 31.');
    if (track(match[1]).locked) throw new Error('That track is pinned. Unpin it on the timeline before changing it.');
    selection = { track: match[1], phrase: (start - 1) / 2 }; loadSelection();
    draft = { density, contour, rhythm: rhythm ? [...new Set(rhythm)].sort((a, b) => a - b) : null };
    drawContour(); applyDraft();
  } catch (e) { announce(`Recipe not applied: ${e.message}`); }
});

function download(blob, filename) {
  const url = URL.createObjectURL(blob), a = document.createElement('a'); a.href = url; a.download = filename;
  document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 10000);
}
function filename() { return project.name.replace(/[^a-z0-9-_]/gi, '-').replace(/-+/g, '-').slice(0,60) || 'music-kitchen'; }
$('export-project').addEventListener('click', () => { download(new Blob([JSON.stringify(project, null, 2)], { type: 'application/json' }), `${filename()}.kitchen.json`); announce('Project exported. This browser also saves your working session automatically.'); });
$('export-audio').addEventListener('click', async () => {
  const button = $('export-audio'); button.disabled = true; button.textContent = 'Rendering…';
  try {
    const spb = 60 / project.tempo, ctx = new OfflineAudioContext(1, Math.ceil((32 * spb + 1) * 44100), 44100);
    const gain = ctx.createGain(); gain.gain.value = .19; gain.connect(ctx.destination);
    allEvents(project).forEach((e) => voice(ctx, gain, e, e.beat * spb, spb));
    const buffer = await ctx.startRendering(), data = buffer.getChannelData(0), bytes = new ArrayBuffer(44 + data.length * 2), view = new DataView(bytes);
    const ascii = (offset, s) => [...s].forEach((c, i) => view.setUint8(offset + i, c.charCodeAt(0)));
    ascii(0, 'RIFF'); view.setUint32(4, 36 + data.length * 2, true); ascii(8, 'WAVE'); ascii(12, 'fmt ');
    view.setUint32(16, 16, true); view.setUint16(20, 1, true); view.setUint16(22, 1, true); view.setUint32(24, 44100, true);
    view.setUint32(28, 88200, true); view.setUint16(32, 2, true); view.setUint16(34, 16, true); ascii(36, 'data'); view.setUint32(40, data.length * 2, true);
    data.forEach((v, i) => view.setInt16(44 + i * 2, Math.max(-1, Math.min(1, v)) * 32767, true));
    download(new Blob([bytes], { type: 'audio/wav' }), `${filename()}.wav`); announce('Current arrangement exported as a WAV file.');
  } catch (e) { announce(`Audio export failed: ${e.message}`); }
  finally { button.disabled = false; button.textContent = '↓ Audio'; }
});
$('reference-image').addEventListener('change', (e) => {
  const file = e.target.files[0]; if (!file) return;
  if (!file.type.startsWith('image/') || file.size > 8 * 1024 * 1024) { announce('Choose an image smaller than 8 MB.'); return; }
  const reader = new FileReader(); reader.onload = () => {
    $('reference-preview').src = reader.result; $('image-reference').hidden = false;
    announce('Image added as a visual reference for this visit. It is not sent to an AI model or saved with the project.');
  }; reader.readAsDataURL(file);
});
$('remove-image').addEventListener('click', () => { $('image-reference').hidden = true; $('reference-preview').removeAttribute('src'); $('reference-image').value = ''; });
document.addEventListener('visibilitychange', () => { if (document.hidden && playing) { pausedBeat = currentBeat() % 32; stopPlayback(false); } });
loadSelection(); renderTracks(); refreshComparison(); save();
