#!/usr/bin/env bash
# Regenerate the social-preview card and icons from their HTML sources.
# Needs: node + playwright (npm i playwright), and ImageMagick for the .ico.
set -euo pipefail
cd "$(dirname "$0")"
node - <<'JS'
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const shot = async (file, w, h, out, scale=1) => {
    const p = await b.newPage({ viewport:{width:w,height:h}, deviceScaleFactor:scale });
    await p.goto('file://' + process.cwd() + '/' + file, { waitUntil:'networkidle' });
    await p.waitForTimeout(1500);              // let webfonts settle
    await p.screenshot({ path: out, clip:{x:0,y:0,width:w,height:h} });
    await p.close();
    console.log('  →', out);
  };
  await shot('assets/og-image.html', 1200, 630, 'assets/og-cover.png');
  await shot('assets/icon.html', 512, 512, 'assets/icon-512.png');
  await shot('assets/icon.html', 512, 512, 'assets/apple-touch-icon.png');
  await b.close();
})();
JS
convert assets/apple-touch-icon.png -resize 180x180 assets/apple-touch-icon.png
convert assets/icon-512.png -resize 32x32 assets/favicon-32.png
convert assets/icon-512.png -resize 16x16 assets/favicon-16.png
convert assets/favicon-32.png assets/favicon-16.png assets/favicon.ico
echo "Done."
