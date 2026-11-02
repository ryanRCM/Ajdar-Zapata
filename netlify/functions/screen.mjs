// /api/screen — each TV checks in about once a minute (site/screen.js).
// 1. Which monitor should this TV show? The first TV gets monitor 1, the next a free one, and each
//    keeps its monitor from then on (Ryan, 2 Nov 2026: two TVs, sent to different places).
//    ?want=1 or ?want=2 pins a TV by hand.
// 2. Which deploy is live? When it changes, the TV reloads itself.
// State lives in Netlify Blobs: one small JSON document, written only when something changes.
import { getStore } from "@netlify/blobs";

const KEY = "devices";
const ACTIVE_MS = 15 * 60 * 1000; // a TV seen in the last 15 minutes holds its monitor
const TOUCH_MS = 4 * 60 * 1000;   // refresh a TV's "last seen" at most every 4 minutes, to keep writes low
const MAX_DEVICES = 20;

export function assign(devices, id, want, now) {
  const next = { ...devices };
  let d = next[id];
  let changed = false;
  if ((want === 1 || want === 2) && (!d || d.m !== want)) { d = { m: want, seen: now }; changed = true; }
  if (!d) {
    const busy = new Set(Object.entries(next).filter(([k, v]) => k !== id && now - v.seen < ACTIVE_MS).map(([, v]) => v.m));
    d = { m: busy.has(1) && !busy.has(2) ? 2 : 1, seen: now };
    changed = true;
  } else if (now - d.seen > TOUCH_MS) {
    d = { ...d, seen: now };
    changed = true;
  }
  next[id] = d;
  const ids = Object.keys(next);
  if (ids.length > MAX_DEVICES) {
    ids.sort((a, b) => next[a].seen - next[b].seen).slice(0, ids.length - MAX_DEVICES).forEach(k => delete next[k]);
    changed = true;
  }
  return { devices: next, monitor: d.m, changed };
}

const reply = body => new Response(JSON.stringify(body), {
  headers: { "content-type": "application/json", "cache-control": "no-store" },
});

export default async (req, context) => {
  const url = new URL(req.url);
  const version = context?.deploy?.id || "";
  const id = url.searchParams.get("id") || "";
  const want = Number(url.searchParams.get("want")) || 0;
  if (!/^[a-z0-9]{8,40}$/i.test(id)) return reply({ version });

  const store = getStore({ name: "screens", consistency: "strong" });
  for (let tries = 0; tries < 4; tries++) {
    const cur = await store.getWithMetadata(KEY, { type: "json" });
    const r = assign(cur?.data || {}, id, want, Date.now());
    if (!r.changed) return reply({ monitor: r.monitor, version });
    // Only write if nobody else wrote in between, so two TVs starting together can't both get monitor 1.
    const res = await store.setJSON(KEY, r.devices, cur ? { onlyIfMatch: cur.etag } : { onlyIfNew: true });
    if (res?.modified !== false) return reply({ monitor: r.monitor, version });
  }
  return reply({ version }); // still racing after 4 tries: the TV keeps its page and asks again next minute
};

export const config = { path: "/api/screen" };
