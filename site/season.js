// Seasons switch themselves on by date (Ryan, 2 Nov 2026: "Christmas versions, Halloween versions that
// automatically update during the month"). Sets <html data-season="..."> before the page draws; the CSS in
// /season.css hides each season's extras outside its dates. Add a season: a new line below, and its
// [data-season-only="name"] elements or CSS.
(() => {
  const d = new Date(), m = d.getMonth() + 1, day = d.getDate();
  let season = 'none';
  if (m === 11 || m === 12 || (m === 1 && day <= 6)) season = 'christmas';   // 1 Nov - 6 Jan
  else if (m === 10) season = 'halloween';                                     // October (nothing built yet)
  const q = new URLSearchParams(location.search).get('season');                // ?season=christmas to preview
  document.documentElement.dataset.season = q || season;
})();
