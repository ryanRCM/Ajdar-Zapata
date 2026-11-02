// /api/screen — each TV checks in about once a minute (site/screen.js).
// 1. Which monitor should this TV show? The first TV gets monitor 1, the next a free one. Once each
//    monitor has had the same device for 20 minutes, those two are locked in as the shop TVs, and
//    every other device is told 0 and goes to the phone menu (Ryan, 2 Nov 2026).
//    ?want=1 or ?want=2 (from ?screen= on the page) re-locks a TV by hand.
// 2. Which deploy is live? When it changes, the TV reloads itself.
// State lives in Netlify Blobs: one small JSON document, written only when something changes.
import { getStore } from "@netlify/blobs";

const KEY = "devices";
const ACTIVE_MS = 15 * 60 * 1000;      // a TV seen in the last 15 minutes holds its monitor
const TOUCH_MS = 4 * 60 * 1000;        // refresh a TV's "last seen" at most every 4 minutes, to keep writes low
const LOCK_AFTER_MS = 20 * 60 * 1000;  // a device on its monitor for 20+ minutes is a TV, not a passing phone
// Set true to pause locking (the saved lock is then ignored, not deleted). Paused once on 2 Nov while
// checking which devices were the shop TVs; Ryan's next photo confirmed them, so locking is on.
const LOCK_PAUSED = false;
const MAX_DEVICES = 20;
// The two shop TVs are locked in (Ryan, 2 Nov 2026). Monitor 1 = left wall (yellow), monitor 2 = right
// wall (orange). If the locked TVs turn out to be on the wrong walls, set SWAP to true and push.
const SWAP = true;   // Ryan, 2 Nov 2026: "switch the monitors ... on the switched sides"

// state: { devices: { id: { m, first, seen } }, locked: { 1: id, 2: id } }. Older state was the devices map itself.
export function assign(state, id, want, now, kind = '') {
  const legacy = state && !state.devices && !state.locked;
  const devices = { ...(legacy ? state : state?.devices || {}) };
  let locked = state?.locked && !LOCK_PAUSED ? { ...state.locked } : null; // paused: any saved lock is ignored
  let changed = legacy && Object.keys(devices).length > 0;

  // ?screen=1 / ?screen=2 always wins: it (re)locks this device to that monitor, e.g. a TV that lost its memory.
  if (want === 1 || want === 2) {
    const d = devices[id];
    if (!d || d.m !== want) { devices[id] = { m: want, first: now - LOCK_AFTER_MS, seen: now }; changed = true; }
    if (locked && locked[want] !== id) {
      locked[want] = id;
      if (locked[3 - want] === id) delete locked[3 - want];
      changed = true;
    }
  }

  let m;
  if (locked) {
    m = locked[1] === id ? 1 : locked[2] === id ? 2 : 0; // 0: not a shop TV, so it goes to the phone menu
    const d = devices[id];
    if (m && d && (now - d.seen > TOUCH_MS || (kind && d.kind !== kind))) { // keep ?status true for the TVs
      devices[id] = { ...d, seen: now, ...(kind ? { kind } : {}) };
      changed = true;
    }
  } else {
    let d = devices[id];
    if (d && !d.first) { d = { ...d, first: d.seen }; changed = true; }
    if (!d) {
      const busy = new Set(Object.entries(devices).filter(([k, v]) => k !== id && now - v.seen < ACTIVE_MS).map(([, v]) => v.m));
      d = { m: busy.has(1) && !busy.has(2) ? 2 : 1, first: now, seen: now };
      changed = true;
    } else if (now - d.seen > TOUCH_MS) {
      d = { ...d, seen: now };
      changed = true;
    }
    if (kind && d.kind !== kind) { d = { ...d, kind }; changed = true; }
    devices[id] = d;
    m = d.m;
    // Lock once each monitor has a device that has stayed on it for 20+ minutes and is still checking in.
    const pick = n => Object.entries(devices)
      .filter(([, v]) => v.m === n && now - v.seen < ACTIVE_MS && (v.seen - (v.first || v.seen)) >= LOCK_AFTER_MS)
      .sort((a, b) => b[1].seen - a[1].seen)[0]?.[0];
    const one = pick(1), two = pick(2);
    if (one && two && !LOCK_PAUSED) { locked = { 1: one, 2: two }; changed = true; }
  }

  const ids = Object.keys(devices);
  if (ids.length > MAX_DEVICES) {
    const keep = new Set(Object.values(locked || {}));
    ids.filter(k => !keep.has(k)).sort((a, b) => devices[a].seen - devices[b].seen)
      .slice(0, ids.length - MAX_DEVICES).forEach(k => delete devices[k]);
    changed = true;
  }
  if (SWAP && m) m = 3 - m;
  // While paused, keep any saved lock in the store untouched (so un-pausing can restore it).
  const keepLock = LOCK_PAUSED && state?.locked ? state.locked : locked;
  return { state: keepLock ? { devices, locked: keepLock } : { devices }, monitor: m, changed };
}

// A short, non-identifying description of the device from its browser: enough to tell a TV from a phone.
function kindOf(ua) {
  const tv = /Tizen|Web0S|webOS|SMART-TV|SmartTV|HbbTV|BRAVIA|AFT|Android TV|GoogleTV|CrKey|Roku|VIDAA|NetCast|Philips|Hisense|TCL|Vestel/i.exec(ua);
  const os = /iPhone|iPad|Android|Windows|Mac OS X|CrOS|Linux/i.exec(ua);
  const br = /(Edg|SamsungBrowser|Firefox|Chrome|Safari)\/?(\d+)?/i.exec(ua);
  return [tv ? 'TV:' + tv[0] : '', os ? os[0] : '', br ? br[1] + (br[2] ? ' ' + br[2] : '') : ''].filter(Boolean).join(' ').slice(0, 40);
}

const reply = body => new Response(JSON.stringify(body), {
  headers: { "content-type": "application/json", "cache-control": "no-store" },
});

export default async (req, context) => {
  const url = new URL(req.url);
  const version = context?.deploy?.id || "";
  // ?status: how many TVs are checking in, on which monitor, and whether they're locked (no IDs shown).
  if (url.searchParams.has("status")) {
    const cur = await getStore({ name: "screens", consistency: "strong" }).get(KEY, { type: "json" });
    const devices = cur?.devices || (cur && !cur.locked ? cur : {}) || {};
    const now = Date.now();
    const active = Object.values(devices).filter(d => now - d.seen < ACTIVE_MS)
      .map(d => ({ monitor: d.m, device: d.kind || '?', page_open_min: d.page ? Math.round((now - d.page) / 60000) : null, last_seen_min: Math.round((now - d.seen) / 60000), on_it_min: Math.round((d.seen - (d.first || d.seen)) / 60000) }));
    return reply({ version, locked: !!cur?.locked && !LOCK_PAUSED, lock_paused: LOCK_PAUSED, locked_monitors: Object.keys(cur?.locked || {}), active });
  }
  const id = url.searchParams.get("id") || "";
  const want = Number(url.searchParams.get("want")) || 0;
  if (!/^[a-z0-9]{8,40}$/i.test(id)) return reply({ version });

  const store = getStore({ name: "screens", consistency: "strong" });
  for (let tries = 0; tries < 4; tries++) {
    const cur = await store.getWithMetadata(KEY, { type: "json" });
    const r = assign(cur?.data || {}, id, want, Date.now(), kindOf(req.headers.get("user-agent") || ""));
    // How long this TV's page has been open (minutes), so ?status shows whether it reloaded after the last deploy.
    const up = Number(url.searchParams.get("up"));
    const d = r.state.devices[id];
    if (d && Number.isFinite(up)) {
      const since = Date.now() - up * 60000;
      if (!d.page || Math.abs(d.page - since) > 90000) { d.page = since; r.changed = true; }
    }
    if (!r.changed) return reply({ monitor: r.monitor, version });
    // Only write if nobody else wrote in between, so two TVs starting together can't both get monitor 1.
    const res = await store.setJSON(KEY, r.state, cur ? { onlyIfMatch: cur.etag } : { onlyIfNew: true });
    if (res?.modified !== false) return reply({ monitor: r.monitor, version });
  }
  return reply({ version }); // still racing after 4 tries: the TV keeps its page and asks again next minute
};

export const config = { path: "/api/screen" };
