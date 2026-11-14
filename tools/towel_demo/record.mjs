// Render the captured Towel run to static/demo/towel-preview.mp4 and its poster.
//
//   npm install --no-save puppeteer-core   (once, in this directory)
//   node record.mjs
//
// Needs Chrome (set CHROME_PATH if it is not in the default macOS location)
// and ffmpeg. Each frame is drawn by render.html's renderAt(t) and piped to
// ffmpeg, so the video is a function of capture.json alone.
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { readFile, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import puppeteer from 'puppeteer-core';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = join(here, '..', '..', 'static', 'demo');
const FPS = 30;
const WIDTH = 1280;
const HEIGHT = 800;
const chrome = process.env.CHROME_PATH ?? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

const capture = JSON.parse(await readFile(join(here, 'capture.json'), 'utf8'));
const browser = await puppeteer.launch({ executablePath: chrome, headless: true });
const page = await browser.newPage();
await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(join(here, 'render.html')).href);
const { duration, poster } = await page.evaluate((c) => setCapture(c), capture);

const ffmpeg = spawn('ffmpeg', [
  '-loglevel', 'error', '-y',
  '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
  '-c:v', 'libx264', '-preset', 'veryslow', '-crf', '27', '-tune', 'animation', '-g', '300',
  '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an',
  join(outDir, 'towel-preview.mp4'),
], { stdio: ['pipe', 'inherit', 'inherit'] });

const frames = Math.ceil(duration * FPS);
for (let frame = 0; frame < frames; frame++) {
  await page.evaluate((t) => renderAt(t), frame / FPS);
  const png = await page.screenshot({ type: 'png' });
  if (!ffmpeg.stdin.write(png)) await once(ffmpeg.stdin, 'drain');
  if (frame % 150 === 0) console.log(`frame ${frame}/${frames}`);
}
ffmpeg.stdin.end();
const [code] = await once(ffmpeg, 'close');
if (code !== 0) throw new Error(`ffmpeg exited with status ${code}`);

await page.evaluate((t) => renderAt(t), poster);
await writeFile(join(outDir, 'towel-preview.jpg'), await page.screenshot({ type: 'jpeg', quality: 70 }));
console.log(`${frames} frames, ${duration.toFixed(1)} s`);

await Promise.race([browser.close(), new Promise((resolve) => setTimeout(resolve, 5000))]);
process.exit(0);
