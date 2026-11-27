// TEMPORARY bridge for the two shop TVs still running the TV page they opened on 24 Nov 2026 at 16:16 UTC (e28571b).
// That page can't be reloaded from here, doesn't know which TV it is and shows show.json's "all"; it asks for
// /tv/show.json?t=<its clock in ms> every 2 minutes. This tells the two apart and hands each its half as "all", from
// the live show.json, so they always show the newest pictures. The current TV page sends p=<its version>: untouched.
//
// Telling them apart (27 Nov 2026, from 23 hours of Netlify's log). Each TV's 2-minute timer runs about 95 ppm fast,
// so the moment its request ARRIVES slips back about 8.2 s (left) and 8.6 s (right) a day, in a straight line (within
// ±0.16 s); the two lines are 1.1 s apart and spreading. Its clock reading t stays to the millisecond until the TV
// corrects its clock, then jumps: those jumps broke the first version's fixed windows (24 Nov), and both TVs fell back
// to the whole menu (Ryan's photo, 27 Nov 13:43). Left TV = the one that opened at 16:16:19 (o=1795536979 in its
// reports), right TV = 16:16:18 (o=1795536978): Ryan, 24 Nov, "right becomes left" (the 16:16:18 TV is on the right).
//
// Each TV also gets its half in the az_tv cookie, which the current TV page reads when it starts: after a restart it
// knows which TV it is with no remote and no help. Every answer is logged (Netlify's request log, "logs").
// Remove this file once no TV asks without p= (Netlify's log); Netlify is then just the host again.
const CYCLE = 120000, T0 = Date.UTC(2026, 10, 27, 13, 45);   // the fit's reference time, 27 Nov 2026 13:45 UTC
const TV = [
  { half: 1, side: 'left', at: 110074, perDay: -8241, t: 114341 },    // ms into the 2-minute cycle at T0; drift per day
  { half: 2, side: 'right', at: 108940, perDay: -8558, t: 115241 },
];
const apart = (a, b) => { const d = (((a - b) % CYCLE) + CYCLE) % CYCLE; return Math.min(d, CYCLE - d); };
// When the request arrived, to the millisecond: Netlify's request ID is a ULID, which begins with it. (Date.now() here
// can be up to a second late when the function starts cold: 27 Nov 13:59, 0.7 s.)
const B32 = '0123456789ABCDEFGHJKMNPQRSTVWXYZ';
const ulidMs = id => { if (!/^[0-7][0-9A-HJKMNP-TV-Z]{25}$/i.test(id || '')) return 0; let v = 0; for (const c of id.slice(0, 10).toUpperCase()) v = v * 32 + B32.indexOf(c); return v; };

export default async (request, context) => {
  const url = new URL(request.url);
  if (url.searchParams.has('p')) return;
  const t = Number(url.searchParams.get('t'));
  if (!t) return;
  const clock = Date.now(), byId = ulidMs(context.requestId) || ulidMs(request.headers.get('x-nf-request-id'));
  const now = byId && byId <= clock + 1000 && byId > clock - 10000 ? byId : clock, days = (now - T0) / 86400000;
  const near = TV.map(tv => ({ tv, d: apart(now, tv.at + tv.perDay * days), dt: apart(t, tv.t) })).sort((a, b) => a.d - b.d);
  // 1. its clock reading exactly as that TV's (until it corrects its clock), arriving about when that TV does
  let pick = near.find(n => n.dt <= 50 && n.d <= 700);
  // 2. else by when it arrives: clearly the nearer of the two lines (only with the exact arrival time: a late clock
  //    would make the right TV look like the left one)
  if (!pick && now === byId && near[0].d <= 600 && near[1].d - near[0].d >= 300) pick = near[0];
  console.log(`tv-old t ${t % CYCLE} arrived ${now % CYCLE} (${now === byId ? 'request id' : 'clock'}): ${near.map(n => `${n.tv.side} ${Math.round(n.d)}ms`).join(', ')} -> ${pick ? pick.tv.side : 'whole menu'}`);
  if (!pick) return;
  const half = pick.tv.half;
  const res = await context.next();
  const j = await res.json();
  // the Christmas look (lights, snow, twinkles) from 1 Nov to 6 Jan, as site/season.js
  const d = new Date(now), m = d.getUTCMonth() + 1, xmas = m === 11 || m === 12 || (m === 1 && d.getUTCDate() <= 6);
  j.all = (xmas && j['tv' + half + 'x']) || j['tv' + half];
  return new Response(JSON.stringify(j), { headers: {
    'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store',
    'set-cookie': `az_tv=${half}; Max-Age=157680000; Path=/; SameSite=Lax; Secure` } });
};
export const config = { path: '/tv/show.json' };
