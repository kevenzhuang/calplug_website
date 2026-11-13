// Builds brand-kit/calplug-slides-template.pptx and brand-kit/calplug-flyer-template.pptx.
// Run from the repository root: node brand-kit/source/make_templates.js   (needs: npm install pptxgenjs sharp)
// Colors and fonts follow DESIGN.md section 3 and section 10 (Brand kit).
const pptxgen = require("pptxgenjs");
const sharp = require("sharp");
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..", "..");
const OUT = path.join(ROOT, "brand-kit");
let applyTheme = null;
try { applyTheme = require(process.env.PPTX_APPLY_THEME || "./apply_theme.js").applyTheme; } catch (e) { /* optional */ }

const THEME = {
  name: "CalPlug",
  headFontFace: "Montserrat",
  bodyFontFace: "Arial",
  colors: { dk1: "1B2530", lt1: "FFFFFF", dk2: "0E2A47", lt2: "F6F8FA",
    accent1: "005BAA", accent2: "8BC53F", accent3: "4A7A1C", accent4: "5B6875", accent5: "E3E8EE", accent6: "0E2A47",
    hlink: "005BAA", folHlink: "004A8C" },
};
const C = THEME.colors;
const img = (p) => "image/png;base64," + fs.readFileSync(path.join(ROOT, p)).toString("base64");

async function ringPng(px) {
  // The ring of the CalPlug logo with its own proportions (inner radius 74% of outer), split on the horizontal.
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 166 166" width="${px}" height="${px}">
  <path d="M0 83A83 83 0 0 1 166 83H144.7A61.7 61.7 0 0 0 21.3 83Z" fill="#005BAA"/><path d="M0 83A83 83 0 0 0 166 83H144.7A61.7 61.7 0 0 1 21.3 83Z" fill="#8BC53F"/></svg>`;
  return "image/png;base64," + (await sharp(Buffer.from(svg)).png().toBuffer()).toString("base64");
}

async function main() {
  const ring = await ringPng(1200);
  const ringPlain = ring;

  // ---------- Slides ----------
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  pres.title = "CalPlug slide template";
  const logo = img("assets/legacy/calpluglogo-small.png");
  const logoSmall = img("assets/brand/calplug-logo-compact.png");
  const foot = [
    { rect: { x: 0, y: 6.55, w: 13.333, h: 0.95, fill: { color: C.dk2 } } },
    { rect: { x: 0, y: 6.5, w: 13.333, h: 0.05, fill: { color: C.accent2 } } },
    { image: { data: img("assets/brand/uci-logo-white.png"), x: 0.7, y: 6.86, w: 1.95, h: 0.33 } },
    { image: { data: img("assets/brand/calit2-logo.png"), x: 2.95, y: 6.75, w: 0.55, h: 0.55 } },
    { text: { text: "calplug.org", options: { x: 10.4, y: 6.75, w: 2.25, h: 0.55, align: "right", fontFace: "Arial", fontSize: 16, bold: true, color: "FFFFFF", margin: 0 } } },
  ];
  pres.defineSlideMaster({
    title: "CalPlug Cover",
    background: { color: "FFFFFF" },
    objects: [
      { image: { data: ring, x: 9.1, y: 0.95, w: 5.4, h: 5.4 } },
      ...foot,
      { image: { data: logo, x: 0.7, y: 0.6, w: 3.9, h: 1.08 } },
      { placeholder: { options: { name: "title", type: "title", align: "left", bold: true, x: 0.7, y: 2.3, w: 8.0, h: 1.9, fontSize: 40, color: C.dk2, valign: "bottom", margin: 0 }, text: "Presentation title" } },
      { placeholder: { options: { name: "subtitle", type: "body", align: "left", x: 0.7, y: 4.4, w: 8.0, h: 0.6, fontSize: 20, color: C.dk1, margin: 0 }, text: "Subtitle or event name" } },
      { placeholder: { options: { name: "byline", type: "body", align: "left", x: 0.7, y: 5.15, w: 8.0, h: 0.8, fontSize: 14, color: C.accent4, margin: 0 }, text: "Presenter, Month Day, Year" } },
    ],
  });
  pres.defineSlideMaster({
    title: "CalPlug Section",
    background: { color: C.dk2 },
    objects: [
      { image: { data: ringPlain, x: 0.7, y: 1.6, w: 1.1, h: 1.1 } },
      { rect: { x: 0, y: 7.45, w: 13.333, h: 0.05, fill: { color: C.accent2 } } },
      { placeholder: { options: { name: "title", type: "title", align: "left", bold: true, x: 0.7, y: 3.0, w: 11.0, h: 1.6, fontSize: 40, color: "FFFFFF", valign: "top", margin: 0 }, text: "Section title" } },
      { placeholder: { options: { name: "body", type: "body", align: "left", x: 0.7, y: 4.7, w: 11.0, h: 0.8, fontSize: 18, color: "C5D0DC", margin: 0 }, text: "One line about this section" } },
    ],
  });
  pres.defineSlideMaster({
    title: "CalPlug Content",
    background: { color: "FFFFFF" },
    objects: [
      { image: { data: logoSmall, x: 10.85, y: 6.95, w: 1.78, h: 0.33 } },
      { placeholder: { options: { name: "title", type: "title", align: "left", bold: true, x: 0.7, y: 0.5, w: 11.9, h: 0.9, fontSize: 30, color: C.dk2, valign: "top", margin: 0 }, text: "Slide title says the message" } },
      { placeholder: { options: { name: "body", type: "body", align: "left", x: 0.7, y: 1.7, w: 11.9, h: 4.9, fontSize: 18, color: C.dk1, valign: "top", margin: 0 }, text: "Body text" } },
    ],
    slideNumber: { x: 0.7, y: 6.95, w: 1, h: 0.33, fontFace: "Arial", fontSize: 11, color: C.accent4 },
  });

  let s = pres.addSlide({ masterName: "CalPlug Cover" });
  s.addText("Presentation title", { placeholder: "title" });
  s.addText("Subtitle or event name", { placeholder: "subtitle" });
  s.addText("Presenter, Month Day, Year", { placeholder: "byline" });
  s.addNotes("Cover. Keep the logo, ring and bottom band as they are. Replace the three lines of text.");

  s = pres.addSlide({ masterName: "CalPlug Section" });
  s.addText("Section title", { placeholder: "title" });
  s.addText("One line about this section", { placeholder: "body" });

  s = pres.addSlide({ masterName: "CalPlug Content" });
  s.addText("Slide title says the message", { placeholder: "title" });
  s.addText([
    { text: "One idea per slide; the title states it", options: { bullet: true, breakLine: true } },
    { text: "Blue (#005BAA) for links and highlights, green (#8BC53F) for shapes only, never for text", options: { bullet: true, breakLine: true } },
    { text: "Titles in Montserrat, text in Arial (or Inter), at least 18 pt", options: { bullet: true } },
  ], { placeholder: "body", paraSpaceAfter: 10 });

  const slidesFile = path.join(OUT, "calplug-slides-template.pptx");
  await pres.writeFile({ fileName: slidesFile });

  // ---------- Flyer (US Letter, portrait) ----------
  const fly = new pptxgen();
  fly.defineLayout({ name: "LETTER_PORTRAIT", width: 8.5, height: 11 });
  fly.layout = "LETTER_PORTRAIT";
  fly.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  fly.title = "CalPlug flyer template";
  fly.defineSlideMaster({
    title: "CalPlug Flyer",
    background: { color: "FFFFFF" },
    objects: [
      { image: { data: logo, x: 0.6, y: 0.55, w: 3.3, h: 0.91 } },
      { image: { data: ring, x: 6.0, y: -1.7, w: 3.7, h: 3.7 } },
      { rect: { x: 0.6, y: 5.75, w: 7.3, h: 2.6, fill: { color: C.lt2 }, line: { color: C.accent5, width: 0.75 } } },
      { text: { text: "Photo or diagram", options: { x: 0.6, y: 6.85, w: 7.3, h: 0.4, align: "center", fontFace: "Arial", fontSize: 12, color: C.accent4, margin: 0 } } },
      { rect: { x: 0, y: 10.0, w: 8.5, h: 1.0, fill: { color: C.dk2 } } },
      { rect: { x: 0, y: 9.95, w: 8.5, h: 0.05, fill: { color: C.accent2 } } },
      { image: { data: img("assets/brand/uci-logo-white.png"), x: 0.6, y: 10.33, w: 1.95, h: 0.33 } },
      { image: { data: img("assets/brand/calit2-logo.png"), x: 2.85, y: 10.22, w: 0.56, h: 0.56 } },
      { text: { text: "calplug.org", options: { x: 5.65, y: 10.22, w: 2.25, h: 0.56, align: "right", fontFace: "Arial", fontSize: 16, bold: true, color: "FFFFFF", margin: 0 } } },
      { placeholder: { options: { name: "kind", type: "body", align: "left", x: 0.6, y: 2.05, w: 6.5, h: 0.4, fontSize: 14, bold: true, color: C.accent3, margin: 0 }, text: "CALPLUG WORKSHOP" } },
      { placeholder: { options: { name: "title", type: "title", align: "left", bold: true, x: 0.6, y: 2.5, w: 7.3, h: 1.9, fontSize: 36, color: C.dk2, valign: "top", margin: 0 }, text: "Event title" } },
      { placeholder: { options: { name: "when", type: "body", align: "left", x: 0.6, y: 4.55, w: 7.3, h: 1.0, fontSize: 16, color: C.dk1, margin: 0 }, text: "Date and time" } },
      { placeholder: { options: { name: "pic", type: "pic", x: 0.6, y: 5.75, w: 7.3, h: 2.6 }, text: "" } },
      { placeholder: { options: { name: "about", type: "body", align: "left", x: 0.6, y: 8.55, w: 7.3, h: 1.2, fontSize: 13, color: C.accent4, valign: "top", margin: 0 }, text: "Two or three sentences about the event, and how to register." } },
    ],
  });
  const f = fly.addSlide({ masterName: "CalPlug Flyer" });
  f.addText("CALPLUG WORKSHOP", { placeholder: "kind" });
  f.addText("Event title in one or two lines", { placeholder: "title" });
  f.addText([{ text: "Month Day, Year, 10:00 am – 3:00 pm", options: { breakLine: true } }, { text: "Calit2 Auditorium, UC Irvine" }], { placeholder: "when" });
  f.addText("Two or three sentences about the event: who it is for, what they will hear, and how to register.", { placeholder: "about" });
  f.addNotes("Flyer. Put one photo or diagram in the picture area (right-click > Change Picture, or insert into the placeholder). Keep the logo, ring and bottom band.");
  const flyerFile = path.join(OUT, "calplug-flyer-template.pptx");
  await fly.writeFile({ fileName: flyerFile });

  if (applyTheme) { await applyTheme(slidesFile, THEME); await applyTheme(flyerFile, THEME); }
  console.log("Wrote", slidesFile, flyerFile);
}
main();
