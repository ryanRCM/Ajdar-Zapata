// TEMPORARY bridge (Ryan, 24 Nov 2026: "just do it now ... guess", "I'm not touching that remote").
// Both shop TVs are still running the TV page they loaded at 16:16 UTC, which can't be reloaded from here and
// doesn't know which TV it is; it shows show.json's "all" picture. The two TVs are identical to the site except
// for when they ask: each asks for /tv/show.json?t=<its clock in ms> every 2 minutes, exactly, one at ~17.7 s and
// the other at ~19.2 s into each 2-minute cycle. So this hands the first its half 1 (left) and the second its half 2
// (right) as "all". A guess: if the sides are wrong, swap LEFT and RIGHT below and push.
// The current TV page sends p=<its version> and is never touched. Remove this file once no TV asks without p
// (Netlify's log), i.e. once both TVs run the current page; Netlify is then just the host again.
// Swapped 24 Nov 2026 ("right becomes left"): the TV that asks at ~17.7 s is the RIGHT TV, the one at ~19.2 s the LEFT.
const LEFT = [18500, 26000], RIGHT = [12000, 18500];   // ms into the TV's 2-minute cycle
export default async (request, context) => {
  const url = new URL(request.url);
  if (url.searchParams.has('p')) return;
  const t = Number(url.searchParams.get('t'));
  if (!t) return;
  const phase = t % 120000;
  const half = phase >= LEFT[0] && phase < LEFT[1] ? 1 : phase >= RIGHT[0] && phase < RIGHT[1] ? 2 : 0;
  if (!half) return;
  const res = await context.next();
  const j = await res.json();
  // the Christmas look (lights, snow, twinkles) from 1 Nov to 6 Jan, as site/season.js
  const d = new Date(), m = d.getUTCMonth() + 1, xmas = m === 11 || m === 12 || (m === 1 && d.getUTCDate() <= 6);
  j.all = (xmas && j['tv' + half + 'x']) || j['tv' + half];
  return new Response(JSON.stringify(j), { headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });
};
export const config = { path: '/tv/show.json' };
