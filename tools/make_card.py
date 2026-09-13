import os, re, sys
src = open('index.html', encoding='utf-8').read()
OVERRIDE = """
  /* ---- static card build: hero only, everything revealed, no chrome ---- */
  .count-section, .timeline-section, .actions, .credit, .sticky-bar,
  .scroll-hint, .petals-layer, .blessing { display: none !important; }
  .fade-up, .tl-item, .tl-vid { opacity: 1 !important; transform: none !important; filter: none !important; }
  html, body { background: #f8f5ef; }
  .hero { margin: 0 auto; }
"""
BACK_ONLY = """
  .hero, .count-section, .timeline-section, .actions, .credit, .sticky-bar,
  .scroll-hint, .petals-layer { display: none !important; }
  .blessing { display: block !important; max-width: none !important;
              padding: 12% 8% !important; }
  .blessing .rule { display: none !important; }
  .bl-img { width: 74% !important; }
  .fade-up { opacity: 1 !important; transform: none !important; filter: none !important; }
  html, body { background: #f8f5ef; }
"""
mode = sys.argv[1] if len(sys.argv) > 1 else 'front'
out = src.replace('</style>', (BACK_ONLY if mode == 'back' else OVERRIDE) + '</style>', 1)
open('_card.html', 'w', encoding='utf-8').write(out)
