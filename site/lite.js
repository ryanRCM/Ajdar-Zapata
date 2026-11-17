// Lite mode (Ryan, 17 Nov 2026): the shop TVs drop off within a minute of opening the menu, so for now they get
// a stripped version with nothing that could strain the TV: no flames, snow or sparkles, no hero slides, no
// animations. Monitor 1 is the still menu; monitor 2 still steps through the menu sections, swapped instantly.
// Everything else is untouched. To bring the full show back: set LITE to false. ?full previews the full show.
(() => {
  const LITE = true;
  window.AZ_LITE = LITE && !new URLSearchParams(location.search).has('full');
  if (window.AZ_LITE) document.documentElement.classList.add('lite');
})();
