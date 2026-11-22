// Rapport — Open Data Challenge · Défi 01 (thème libre)
// Génère Rapport_Etat_au_bout_du_chemin_Togo.pptx (10 slides)

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const OUT = path.join(__dirname, "Rapport_Etat_au_bout_du_chemin_Togo.pptx");
const CAP = (n) => { const p = path.join(__dirname, "captures", n); return fs.existsSync(p) ? p : null; };
const URL = "togo-etat-au-bout-du-chemin.streamlit.app";
const TITRE = "L'État au bout du chemin";

const C = { dark: "07301F", green: "0E7C56", lime: "4ADE80", gold: "C9962B", red: "C0392F", ink: "0C1A14",
            muted: "5F6B66", card: "E4F2EB", redl: "FBEAE8", goldl: "FBF2DC", blue: "2F5D78", white: "FFFFFF",
            grey: "F1F5F3" };
const HF = "Cambria", BF = "Calibri";

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "SADJINA Christ";
pres.title = TITRE + " — Open Data Challenge Défi 01";

// ---------------------------------------------------------------- helpers
const title = (s, t, o = {}) => s.addText(t, { x: 0.5, y: 0.3, w: 9, h: 0.68, fontFace: HF, fontSize: 25, bold: true, color: o.color || C.dark, isTextBox: true, margin: 0, valign: "middle" });
const kicker = (s, t, o = {}) => s.addText(t, { x: 0.5, y: 0.96, w: 9, h: 0.34, fontFace: BF, fontSize: 12, italic: true, color: o.color || C.muted, isTextBox: true, margin: 0, valign: "middle" });
const footer = (s, n, dark = false) => s.addText(`${TITRE}  ·  SADJINA Christ  ·  ${n} / 10`, { x: 0.5, y: 5.22, w: 9, h: 0.25, fontFace: BF, fontSize: 9, color: dark ? "9FB8AC" : C.muted, isTextBox: true, margin: 0, align: "right" });
const card = (s, x, y, w, h, fill = C.card) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: fill, width: 0 }, rectRadius: 0.08 });
function stat(s, x, y, w, h, v, l, color = C.dark, fill = C.card, fs = 28) {
  card(s, x, y, w, h, fill);
  s.addText(v, { x: x + 0.14, y: y + 0.08, w: w - 0.28, h: h * 0.5, fontFace: HF, fontSize: fs, bold: true, color, isTextBox: true, margin: 0, valign: "middle" });
  s.addText(l, { x: x + 0.14, y: y + h * 0.56, w: w - 0.28, h: h * 0.42, fontFace: BF, fontSize: 10, color: C.muted, isTextBox: true, margin: 0, valign: "top" });
}
function box(s, x, y, w, h, head, body, fill = C.card, headColor = C.dark, bfs = 10) {
  card(s, x, y, w, h, fill);
  s.addText([{ text: head, options: { bold: true, color: headColor, fontSize: 11.5, breakLine: true } }, { text: body, options: { color: C.ink, fontSize: bfs } }],
    { x: x + 0.14, y: y + 0.07, w: w - 0.28, h: h - 0.14, fontFace: BF, isTextBox: true, margin: 0, valign: "top" });
}
function numbered(s, x, y, w, n, head, body, color = C.green) {
  s.addShape(pres.shapes.OVAL, { x, y: y + 0.02, w: 0.38, h: 0.38, fill: { color }, line: { color, width: 0 } });
  s.addText(String(n), { x, y: y + 0.02, w: 0.38, h: 0.38, fontFace: HF, fontSize: 14, bold: true, color: C.white, isTextBox: true, margin: 0, align: "center", valign: "middle" });
  s.addText([{ text: head, options: { bold: true, color: C.ink, fontSize: 11.5, breakLine: true } }, { text: body, options: { color: C.muted, fontSize: 9.5 } }],
    { x: x + 0.48, y, w: w - 0.48, h: 1.0, fontFace: BF, isTextBox: true, margin: 0, valign: "top" });
}
function image(s, file, x, y, w, h, label) {
  const p = CAP(file);
  if (p) { s.addImage({ path: p, x, y, w, h }); s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: C.white, transparency: 100 }, line: { color: "C9D6CE", width: 0.75 } }); }
  else { card(s, x, y, w, h, "DCE7E0"); s.addText(label, { x, y, w, h, fontFace: BF, fontSize: 12, color: C.muted, italic: true, isTextBox: true, align: "center", valign: "middle" }); }
}
const tbl = (s, rows, x, y, w, colW) => s.addTable(rows, {
  x, y, w, colW, border: { type: "solid", color: "DCE7E0", pt: 0.5 }, fontFace: BF, fontSize: 9.5,
  color: C.ink, valign: "middle", rowH: 0.235, margin: 0.04,
});

// ================================================================ 1 · Titre
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  s.addText("OPEN DATA CHALLENGE · DÉFI 01 · THÈME LIBRE", { x: 0.6, y: 0.48, w: 8.8, h: 0.32, fontFace: BF, fontSize: 11, color: C.lime, bold: true, charSpacing: 2, isTextBox: true, margin: 0 });
  s.addText("L'État au bout du chemin", { x: 0.6, y: 0.95, w: 6.3, h: 1.1, fontFace: HF, fontSize: 36, bold: true, color: C.white, isTextBox: true, margin: 0, valign: "middle" });
  s.addText("Où les services publics s'arrêtent au Togo — et si l'argent public va là où le manque est.", { x: 0.6, y: 2.05, w: 6.1, h: 0.6, fontFace: BF, fontSize: 14.5, color: C.lime, isTextBox: true, margin: 0, valign: "top" });
  s.addText("Eau, électricité, services financiers et mobilité mesurés sur les 39 préfectures à partir de 16 jeux ouverts, puis confrontés aux 813 ouvrages du projet COSO.", { x: 0.6, y: 2.72, w: 6.1, h: 0.85, fontFace: BF, fontSize: 12.5, color: "CFE3D8", isTextBox: true, margin: 0, valign: "top" });
  s.addText([{ text: "Tableau de bord interactif : ", options: { color: "9FB8AC", fontSize: 11.5 } }, { text: URL, options: { color: C.lime, fontSize: 12.5, bold: true, hyperlink: { url: "https://" + URL } } }],
    { x: 0.6, y: 3.7, w: 6.3, h: 0.32, fontFace: BF, isTextBox: true, margin: 0 });
  s.addText([{ text: "SADJINA Christ", options: { bold: true, color: C.white, fontSize: 13.5, breakLine: true } }, { text: "Python · Streamlit · Plotly · 7 pages interactives · novembre 2026", options: { color: "9FB8AC", fontSize: 10.5 } }],
    { x: 0.6, y: 4.35, w: 6, h: 0.62, fontFace: BF, isTextBox: true, margin: 0, valign: "bottom" });
  [["1 sur 6", "Togolais vit dans une préfecture mal servie sur les quatre dimensions"],
   ["+0,63", "corrélation entre l'argent reçu et le niveau d'accès, dans la zone COSO", C.lime],
   ["5 / 10", "des préfectures les plus mal servies sont dans les Plateaux, sans programme"]].forEach(([v, l, col], i) => {
    const y = 0.95 + i * 1.25;
    s.addText(v, { x: 6.9, y, w: 2.6, h: 0.65, fontFace: HF, fontSize: 30, bold: true, color: col || C.white, isTextBox: true, margin: 0, align: "right", valign: "middle" });
    s.addText(l, { x: 6.4, y: y + 0.63, w: 3.1, h: 0.5, fontFace: BF, fontSize: 10, color: "9FB8AC", isTextBox: true, margin: 0, align: "right" });
  });
  s.addNotes("Thème libre : j'ai choisi de croiser tous les secteurs déjà traités dans les défis précédents, puis de confronter le résultat à une dépense publique réelle. Le tableau de bord en ligne est le livrable principal.");
}

// ================================================================ 2 · Démarche
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "Démarche : 16 jeux ouverts, un pipeline, sept vues");
  kicker(s, "Aucun calcul n'est fait dans l'interface : tout vient d'un script unique, relançable en une commande.");
  const steps = [["Cataloguer", "Les 1 715 jeux du portail national ont été parcourus par l'API pour identifier ceux qui sont géolocalisés à la préfecture. 16 retenus, 17 fichiers téléchargés et tracés avec leurs liens."],
    ["Fiabiliser", "Référentiel des 39 préfectures reconstruit, Mô et Avé compris. Longueurs de route calculées par haversine sur les tracés MULTILINESTRING. Deux jeux mal étiquetés identifiés (slide 8)."],
    ["Mesurer", "Quatre dimensions ramenées à l'habitant, normalisées de 0 à 100 sur les 39 préfectures, puis moyennées à parts égales. L'indice est relatif et compare le Togo à lui-même."],
    ["Confronter", "L'indice est croisé avec les 813 ouvrages COSO géolocalisés et chiffrés — seule dépense publique réelle publiée en données ouvertes — pour tester l'allocation."]];
  steps.forEach(([h, b], i) => {
    const x = 0.5 + i * 2.3; card(s, x, 1.4, 2.15, 2.7);
    s.addShape(pres.shapes.OVAL, { x: x + 0.14, y: 1.55, w: 0.4, h: 0.4, fill: { color: C.green }, line: { color: C.green, width: 0 } });
    s.addText(String(i + 1), { x: x + 0.14, y: 1.55, w: 0.4, h: 0.4, fontFace: HF, fontSize: 14, bold: true, color: C.white, isTextBox: true, margin: 0, align: "center", valign: "middle" });
    s.addText(h, { x: x + 0.63, y: 1.55, w: 1.45, h: 0.4, fontFace: BF, fontSize: 13, bold: true, color: C.dark, isTextBox: true, margin: 0, valign: "middle" });
    s.addText(b, { x: x + 0.14, y: 2.05, w: 1.87, h: 1.95, fontFace: BF, fontSize: 9.5, color: C.ink, isTextBox: true, margin: 0, valign: "top" });
  });
  box(s, 0.5, 4.25, 9.0, 0.85, "100 % des données chiffrées viennent d'opendata.gouv.tg",
      "RGPH-5 2022 (INSEED) · taux d'accès électricité et agences CEET · agences TdE · postes d'eau autonomes et pompes à motricité humaine · établissements de finance · agents mobile money · auto-écoles · réseau routier classé · formations sanitaires et densité · scolarisation · pauvreté · inventaire COSO (ANADEB, 12 jeux sectoriels). Seul apport extérieur : les contours de préfectures (geoBoundaries / OSM, 2017), utilisés pour dessiner les cartes et pour rien d'autre.",
      C.card, C.dark, 9);
  footer(s, 2);
  s.addNotes("La liste complète des 16 jeux, avec le lien de chaque page et le lien de téléchargement direct, est livrée en JSON et affichée dans la page Méthode & sources du tableau de bord.");
}

// ================================================================ 3 · L'indice
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "L'indice d'accès : quatre dimensions, une échelle");
  kicker(s, "0 = la moins bien dotée des 39 préfectures, 100 = la mieux dotée. Aucune pondération cachée.");
  const dims = [["Eau", "points d'eau (PEA + PMH)\npour 10 000 habitants", "16 036 points", C.blue],
    ["Électricité", "taux d'accès basse tension\npublié par la CEET (2021)", "57,8 % au national", C.gold],
    ["Services financiers", "établissements + agents mobile\nmoney pour 10 000 habitants", "20 448 points", C.green],
    ["Mobilité", "mètres de route classée\npar habitant", "3 373 km mesurés", "8A5A3B"]];
  dims.forEach(([n, d, v, col], i) => {
    const x = 0.5 + i * 2.3; card(s, x, 1.4, 2.15, 1.55, C.grey);
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.4, w: 0.06, h: 1.55, fill: { color: col }, line: { width: 0 } });
    s.addText(n, { x: x + 0.2, y: 1.5, w: 1.85, h: 0.3, fontFace: BF, fontSize: 12, bold: true, color: col, isTextBox: true, margin: 0 });
    s.addText(d, { x: x + 0.2, y: 1.82, w: 1.85, h: 0.6, fontFace: BF, fontSize: 9.5, color: C.ink, isTextBox: true, margin: 0, valign: "top" });
    s.addText(v, { x: x + 0.2, y: 2.5, w: 1.85, h: 0.35, fontFace: HF, fontSize: 13, bold: true, color: C.dark, isTextBox: true, margin: 0 });
  });
  image(s, "carte_indice.png", 0.5, 3.1, 3.1, 2.0, "Carte de l'indice d'accès");
  const rows = [[{ text: "Préfecture", options: { bold: true, fill: C.dark, color: C.white } }, { text: "Région", options: { bold: true, fill: C.dark, color: C.white } }, { text: "Indice", options: { bold: true, fill: C.dark, color: C.white, align: "right" } }],
    ["Assoli", "Kara", { text: "67,1", options: { align: "right", bold: true } }],
    ["Kozah", "Kara", { text: "62,3", options: { align: "right" } }],
    ["Bassar", "Kara", { text: "59,8", options: { align: "right" } }],
    [{ text: "…", options: { color: C.muted } }, { text: "", options: {} }, { text: "", options: {} }],
    ["Haho", "Plateaux", { text: "23,7", options: { align: "right", color: C.red } }],
    ["Kpendjal", "Savanes", { text: "17,4", options: { align: "right", color: C.red } }],
    ["Kpendjal-Ouest", "Savanes", { text: "16,0", options: { align: "right", color: C.red } }],
    ["Akébou", "Plateaux", { text: "11,6", options: { align: "right", color: C.red, bold: true } }]];
  tbl(s, rows, 3.8, 3.1, 2.9, [1.3, 0.95, 0.65]);
  box(s, 6.95, 3.1, 2.55, 2.0, "Ce qu'il mesure, ce qu'il ne mesure pas",
      "L'indice mesure une couverture d'infrastructures, pas un niveau de bien-être : un forage recensé n'est pas un forage qui coule.\n\nIl est relatif : 100 veut dire « la mieux dotée des 39 », pas « bien dotée ». Les quatre scores restent visibles séparément.",
      C.goldl, C.dark, 9.5);
  footer(s, 3);
  s.addNotes("La carte s'appuie sur 36 contours : les contours ouverts datent de 2017, avant la création des 39 préfectures. Agoè-Nyivé, Kpendjal-Ouest et Oti-Sud y sont fondues dans leur préfecture d'origine, par moyenne pondérée par la population.");
}

// ================================================================ 4 · Classement
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "Le manque n'est pas une affaire de taille");
  kicker(s, "La corrélation entre l'indice d'accès et la population d'une préfecture est de +0,02 : nulle.");
  image(s, "classement.png", 0.5, 1.35, 5.9, 3.75, "Classement des 39 préfectures");
  stat(s, 6.6, 1.35, 2.9, 1.0, "1 402 721", "habitants dans les 10 préfectures les moins bien servies, soit 17,3 % des Togolais", C.red, C.redl, 22);
  stat(s, 6.6, 2.45, 2.9, 1.0, "55,5 pts", "d'écart entre Assoli et Akébou, sur une échelle de 100", C.dark, C.card, 24);
  box(s, 6.6, 3.55, 2.9, 1.55, "Un problème de placement, pas de densité",
      "Ce ne sont ni les petites préfectures qui sont mal servies, ni les grandes qui le sont bien. Le manque ne suit pas la démographie : il suit l'histoire de l'implantation des équipements. C'est une bonne nouvelle — un problème de placement se corrige.",
      C.card, C.dark, 9.5);
  footer(s, 4);
  s.addNotes("Les losanges dorés marquent les 9 préfectures couvertes par le projet COSO. On voit déjà qu'elles sont surtout dans la moitié basse du classement — c'est le point de départ de la slide 6.");
}

// ================================================================ 5 · Dimensions
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "Les quatre dimensions ne se superposent pas");
  kicker(s, "Électricité et eau varient même en sens inverse (−0,44) : l'indice ne redit pas quatre fois la même chose.");
  image(s, "decomposition.png", 0.5, 1.35, 5.55, 2.35, "Décomposition de l'indice");
  image(s, "eau.png", 0.5, 3.8, 5.55, 1.3, "Eau par préfecture");
  const pires = [["Électricité", "19", C.gold], ["Services financiers", "7", C.green], ["Eau", "7", C.blue], ["Mobilité", "6", "8A5A3B"]];
  s.addText("Le point noir, préfecture par préfecture", { x: 6.25, y: 1.35, w: 3.25, h: 0.3, fontFace: BF, fontSize: 11.5, bold: true, color: C.dark, isTextBox: true, margin: 0 });
  pires.forEach(([n, v, col], i) => {
    const y = 1.72 + i * 0.52; card(s, 6.25, y, 3.25, 0.44, C.grey);
    s.addShape(pres.shapes.RECTANGLE, { x: 6.25, y, w: 0.06, h: 0.44, fill: { color: col }, line: { width: 0 } });
    s.addText(n, { x: 6.45, y, w: 2.1, h: 0.44, fontFace: BF, fontSize: 10.5, color: C.ink, isTextBox: true, margin: 0, valign: "middle" });
    s.addText(v + " / 39", { x: 8.4, y, w: 0.95, h: 0.44, fontFace: HF, fontSize: 13, bold: true, color: col, isTextBox: true, margin: 0, align: "right", valign: "middle" });
  });
  box(s, 6.25, 3.9, 3.25, 1.2, "Pourquoi cela compte",
      "Une politique nationale uniforme traiterait la bonne dimension pour une minorité de territoires. L'électricité est le premier point noir de 19 préfectures sur 39 — mais pour 20 autres, le levier est ailleurs.",
      C.goldl, C.dark, 9.5);
  footer(s, 5);
  s.addNotes("L'hydraulique villageoise se déploie précisément là où le réseau électrique n'arrive pas : d'où la corrélation négative, qui n'est pas un paradoxe mais une confirmation que les dimensions sont complémentaires.");
}

// ================================================================ 6 · LE résultat
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "L'argent va-t-il là où le manque est ? Non.", { color: C.red });
  kicker(s, "Chaque point est une préfecture. Si l'argent suivait le manque, le nuage descendrait de gauche à droite. Il monte.");
  image(s, "coso_scatter.png", 0.5, 1.35, 6.3, 3.1, "Investissement COSO par habitant selon l'indice d'accès");
  box(s, 0.5, 4.55, 6.3, 0.58, "",
      "À l'intérieur de la zone COSO, la corrélation entre l'investissement par habitant et le niveau d'accès vaut +0,63 : plus une préfecture était déjà bien servie, plus elle a reçu par habitant.",
      C.redl, C.red, 10);
  stat(s, 6.95, 1.35, 2.55, 0.95, "6 061 F", "par habitant pour les 4 préfectures les plus mal servies de la zone", C.red, C.redl, 24);
  stat(s, 6.95, 2.4, 2.55, 0.95, "11 767 F", "par habitant pour les 4 mieux servies — 1,9 fois plus", C.dark, C.card, 24);
  box(s, 6.95, 3.45, 2.55, 1.68, "Le ciblage régional, lui, est juste",
      "La zone COSO affiche un indice moyen de 30,7 contre 37,2 hors zone : le projet a bien été implanté dans la moitié la plus mal servie du pays.\n\nLe problème n'est donc pas le choix de la région, mais la répartition à l'intérieur de celle-ci.",
      C.card, C.green, 9.5);
  footer(s, 6);
  s.addNotes("Cinkassé, 11e au classement national de l'accès, est la préfecture la mieux dotée de la zone avec 23 002 F par habitant. Kpendjal-Ouest, 38e sur 39, en reçoit quatre fois moins.");
}

// ================================================================ 7 · Les deux écarts
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "Deux écarts : l'un interne, l'autre national");
  kicker(s, "L'un relève du comité de pilotage du projet, l'autre d'une décision de l'État.");
  s.addText("À l'intérieur de la zone COSO — la colonne F/habitant devrait décroître", { x: 0.5, y: 1.3, w: 4.5, h: 0.3, fontFace: BF, fontSize: 11, bold: true, color: C.dark, isTextBox: true, margin: 0 });
  const h = [{ text: "Préfecture", options: { bold: true, fill: C.dark, color: C.white } }, { text: "Rang /39", options: { bold: true, fill: C.dark, color: C.white, align: "center" } }, { text: "Ouvrages", options: { bold: true, fill: C.dark, color: C.white, align: "center" } }, { text: "F / habitant", options: { bold: true, fill: C.dark, color: C.white, align: "right" } }];
  const r1 = [h,
    ["Kpendjal-Ouest", { text: "38", options: { align: "center" } }, { text: "36", options: { align: "center" } }, { text: "5 701", options: { align: "right", color: C.red, bold: true } }],
    ["Kpendjal", { text: "37", options: { align: "center" } }, { text: "30", options: { align: "center" } }, { text: "6 138", options: { align: "right", color: C.red } }],
    ["Tandjoaré", { text: "36", options: { align: "center" } }, { text: "77", options: { align: "center" } }, { text: "9 833", options: { align: "right" } }],
    ["Tchamba", { text: "29", options: { align: "center" } }, { text: "43", options: { align: "center" } }, { text: "3 637", options: { align: "right", color: C.red } }],
    ["Oti-Sud", { text: "20", options: { align: "center" } }, { text: "151", options: { align: "center" } }, { text: "16 003", options: { align: "right" } }],
    ["Binah", { text: "16", options: { align: "center" } }, { text: "42", options: { align: "center" } }, { text: "10 136", options: { align: "right" } }],
    ["Tône", { text: "15", options: { align: "center" } }, { text: "198", options: { align: "center" } }, { text: "8 540", options: { align: "right" } }],
    ["Cinkassé", { text: "11", options: { align: "center" } }, { text: "149", options: { align: "center" } }, { text: "23 002", options: { align: "right", bold: true } }],
    ["Oti", { text: "10", options: { align: "center" } }, { text: "87", options: { align: "center" } }, { text: "11 314", options: { align: "right" } }]];
  tbl(s, r1, 0.5, 1.62, 4.5, [1.55, 0.78, 0.82, 1.15]);
  s.addText("Hors zone — sept préfectures aussi mal servies, sans un franc", { x: 5.25, y: 1.3, w: 4.25, h: 0.3, fontFace: BF, fontSize: 11, bold: true, color: C.dark, isTextBox: true, margin: 0 });
  const r2 = [[{ text: "Préfecture", options: { bold: true, fill: C.red, color: C.white } }, { text: "Région", options: { bold: true, fill: C.red, color: C.white } }, { text: "Rang /39", options: { bold: true, fill: C.red, color: C.white, align: "center" } }, { text: "Population", options: { bold: true, fill: C.red, color: C.white, align: "right" } }],
    ["Akébou", "Plateaux", { text: "39", options: { align: "center" } }, { text: "73 830", options: { align: "right" } }],
    ["Mô", "Centrale", { text: "35", options: { align: "center" } }, { text: "52 448", options: { align: "right" } }],
    ["Anié", "Plateaux", { text: "34", options: { align: "center" } }, { text: "180 158", options: { align: "right" } }],
    ["Haho", "Plateaux", { text: "33", options: { align: "center" } }, { text: "305 096", options: { align: "right" } }],
    ["Dankpen", "Kara", { text: "32", options: { align: "center" } }, { text: "185 662", options: { align: "right" } }],
    ["Est-Mono", "Plateaux", { text: "31", options: { align: "center" } }, { text: "164 460", options: { align: "right" } }],
    ["Moyen-Mono", "Plateaux", { text: "30", options: { align: "center" } }, { text: "90 505", options: { align: "right" } }],
    [{ text: "Total", options: { bold: true } }, { text: "", options: {} }, { text: "", options: {} }, { text: "1 052 159", options: { align: "right", bold: true, color: C.red } }]];
  tbl(s, r2, 5.25, 1.62, 4.25, [1.4, 1.0, 0.78, 1.07]);
  box(s, 0.5, 4.35, 9.0, 0.75, "Le reproche, tempéré",
      "COSO est un projet des régions Nord : son mandat exclut les Plateaux par construction, et il serait malhonnête de lui reprocher Akébou ou Haho. Le constat juste tient en deux parties. À l'intérieur de son mandat, sa répartition est inversée par rapport au besoin mesuré — le projet peut le corriger. Hors de son mandat, cinq préfectures des Plateaux aussi mal servies que celles du Kpendjal n'ont aucun programme équivalent identifiable dans les données ouvertes — seule une décision nationale peut le corriger.",
      C.goldl, C.dark, 9.5);
  footer(s, 7);
  s.addNotes("Parmi les 10 préfectures les moins bien servies du pays, 3 seulement sont couvertes par COSO.");
}

// ================================================================ 8 · Qualité
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "Ce que la donnée ne dit pas — et ce qu'elle dit mal");
  kicker(s, "Trois anomalies trouvées dans les sources, cinq limites assumées. Aucune ne casse les constats ; toutes en fixent la portée.");
  const anos = [["Jeu de population mal millésimé", "Le jeu intitulé « RGPH-5 2022 » contient en réalité les effectifs de 2010 : son total national est de 6,19 M contre 8,10 M au RGPH-5. Le vrai RGPH-5 est publié sous un autre slug. Les deux sont utilisés ici, chacun à sa bonne date."],
    ["Scolarisation : ventilation par sexe inutilisable", "La série « Féminin » dépasse 100 % dans six régions sur sept, ce qui est impossible pour un taux net. Au Kara, le Total publié (95,4 %) est inférieur à ses deux composantes. Seule la colonne « Total » est exploitée."],
    ["Dictionnaires servis comme données", "Plusieurs jeux exposent deux CSV dont l'un est le dictionnaire des champs, sans que les métadonnées le distinguent. Un script de téléchargement naïf récupère le mauvais fichier. Un champ « role » dans l'API éviterait l'erreur."]];
  anos.forEach(([h, b], i) => box(s, 0.5 + i * 3.1, 1.35, 2.9, 1.85, h, "\n" + b, C.redl, C.red, 9));
  s.addText("Les cinq limites, énoncées dans le tableau de bord lui-même", { x: 0.5, y: 3.35, w: 9, h: 0.3, fontFace: BF, fontSize: 11.5, bold: true, color: C.dark, isTextBox: true, margin: 0 });
  const lims = [["Électricité sur un découpage périmé", "six zones commerciales regroupent deux préfectures : cinq valeurs sont héritées, ce qui ne peut que surestimer leur accès"],
    ["Des taux au-dessus de 100 %", "abonnés au numérateur, ménages estimés au dénominateur ; conservés tels que publiés plutôt que rognés"],
    ["Un point d'eau recensé n'est pas un point d'eau qui coule", "97 ouvrages signalés hors service, sans date de dernier contrôle : l'indice mesure une couverture théorique"],
    ["Le réseau mesuré est le réseau classé", "les pistes rurales, qui portent le dernier kilomètre, ne figurent dans aucun jeu ouvert géoréférencé"],
    ["L'indice est relatif et non pondéré", "100 = la mieux dotée des 39, pas « bien dotée » ; les quatre scores restent visibles séparément"]];
  lims.forEach(([h, b], i) => {
    const y = 3.7 + i * 0.32;
    s.addText([{ text: `${i + 1}. ${h} — `, options: { bold: true, color: C.ink, fontSize: 9.5 } }, { text: b, options: { color: C.muted, fontSize: 9.5 } }],
      { x: 0.5, y, w: 9, h: 0.3, fontFace: BF, isTextBox: true, margin: 0, valign: "middle" });
  });
  footer(s, 8);
  s.addNotes("Les trois anomalies méritent d'être remontées au producteur : elles sont faciles à corriger et elles piègent tout réutilisateur.");
}

// ================================================================ 9 · Recommandations
{
  const s = pres.addSlide(); s.background = { color: C.white };
  title(s, "Trois recommandations, chiffrées et adressées");
  kicker(s, "Chacune se vérifie sur les données de ce rapport, et chacune a un destinataire.");
  const recos = [[1, "Réaligner le solde de COSO sur l'indice d'accès", "+5 706 F", "par habitant à rattraper au Kpendjal-Ouest",
    "Pour que les quatre préfectures les plus mal servies de la zone atteignent le niveau par habitant des quatre mieux servies, il faudrait y réorienter 3,1 milliards de F CFA — 22 % de l'enveloppe déjà engagée. Appliquer la règle aux seuls décaissements restants suffirait à redresser la pente sans rouvrir un marché.", "ANADEB, comité de pilotage COSO", C.gold],
    [2, "Ouvrir un volet Plateaux-Nord", "814 000", "habitants dans cinq préfectures sans programme",
      "Akébou, Anié, Haho, Est-Mono et Moyen-Mono figurent parmi les dix préfectures les moins bien servies du pays et ne relèvent d'aucun programme d'investissement communautaire identifiable. Akébou cumule le dernier rang national, 3,7 % d'accès à l'électricité et zéro ouvrage.", "Ministère du Développement à la base", C.red],
    [3, "Publier l'électricité par préfecture", "19 / 39", "préfectures dont le point noir est l'électricité",
      "C'est la seule dimension encore publiée sur un découpage commercial antérieur aux 39 préfectures, et aucun jeu ne publie le taux de desserte TdE par préfecture. Ces deux publications rendraient l'indice entièrement reproductible.", "CEET, TdE, MESPTN", C.green]];
  recos.forEach(([n, t, v, vl, b, dest, col], i) => {
    const y = 1.32 + i * 1.28;
    card(s, 0.5, y, 9.0, 1.18, i === 1 ? C.redl : C.grey);
    s.addShape(pres.shapes.OVAL, { x: 0.68, y: y + 0.14, w: 0.4, h: 0.4, fill: { color: col }, line: { width: 0 } });
    s.addText(String(n), { x: 0.68, y: y + 0.14, w: 0.4, h: 0.4, fontFace: HF, fontSize: 14, bold: true, color: C.white, isTextBox: true, margin: 0, align: "center", valign: "middle" });
    s.addText(t, { x: 1.2, y: y + 0.1, w: 5.8, h: 0.32, fontFace: HF, fontSize: 13.5, bold: true, color: C.dark, isTextBox: true, margin: 0, valign: "middle" });
    s.addText(b, { x: 1.2, y: y + 0.44, w: 5.72, h: 0.68, fontFace: BF, fontSize: 9, color: C.ink, isTextBox: true, margin: 0, valign: "top" });
    s.addText(v, { x: 7.5, y: y + 0.1, w: 1.85, h: 0.4, fontFace: HF, fontSize: 19, bold: true, color: col, isTextBox: true, margin: 0, align: "right", valign: "middle" });
    s.addText(vl, { x: 7.0, y: y + 0.52, w: 2.35, h: 0.34, fontFace: BF, fontSize: 8.5, color: C.muted, isTextBox: true, margin: 0, align: "right", valign: "top" });
    s.addText("→ " + dest, { x: 7.1, y: y + 0.88, w: 2.25, h: 0.24, fontFace: BF, fontSize: 8.5, italic: true, color: col, isTextBox: true, margin: 0, align: "right", valign: "middle" });
  });
  footer(s, 9);
  s.addNotes("Les trois recommandations sont volontairement séquencées : corriger ce qui est en cours, ouvrir ce qui manque, publier ce qui permettrait d'arbitrer.");
}

// ================================================================ 10 · Livrable
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  s.addText("Le livrable", { x: 0.6, y: 0.45, w: 6, h: 0.7, fontFace: HF, fontSize: 27, bold: true, color: C.white, isTextBox: true, margin: 0, valign: "middle" });
  s.addText("Sept pages, filtres persistants, exports CSV, sources liées une par une.", { x: 0.6, y: 1.1, w: 5.9, h: 0.34, fontFace: BF, fontSize: 11.5, italic: true, color: "9FB8AC", isTextBox: true, margin: 0, valign: "top" });
  const pages = [["Synthèse", "le constat et les trois résultats, en une page"],
    ["L'indice d'accès", "construction, carte, décomposition, profil par préfecture"],
    ["Eau, courant, argent, route", "les quatre dimensions, séparément"],
    ["Les 36 880 points", "chaque point de service sur la carte, filtrable"],
    ["L'argent va-t-il au manque ?", "le croisement COSO — le cœur de l'analyse"],
    ["Ce que l'accès change", "santé, école, pauvreté — et ce qu'on ne peut pas conclure"],
    ["Méthode & sources", "le calcul complet, les 16 jeux liés, les cinq limites"]];
  pages.forEach(([n, d], i) => {
    const y = 1.56 + i * 0.4;
    s.addText(String(i + 1).padStart(2, "0"), { x: 0.6, y, w: 0.42, h: 0.4, fontFace: HF, fontSize: 12, bold: true, color: C.lime, isTextBox: true, margin: 0, valign: "middle" });
    s.addText([{ text: n + "  ", options: { bold: true, color: C.white, fontSize: 11 } }, { text: "— " + d, options: { color: "9FB8AC", fontSize: 10 } }],
      { x: 1.05, y, w: 5.4, h: 0.4, fontFace: BF, isTextBox: true, margin: 0, valign: "middle" });
  });
  image(s, "coso_carte.png", 6.65, 1.75, 2.85, 2.1, "Les 813 ouvrages COSO");
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.65, y: 4.0, w: 2.85, h: 1.1, fill: { color: "0B5138" }, line: { width: 0 }, rectRadius: 0.08 });
  s.addText([{ text: "Tableau de bord en ligne\n", options: { color: "9FB8AC", fontSize: 9.5 } }, { text: URL, options: { color: C.lime, fontSize: 11, bold: true, hyperlink: { url: "https://" + URL } } }],
    { x: 6.8, y: 4.1, w: 2.55, h: 0.9, fontFace: BF, isTextBox: true, margin: 0, valign: "middle" });
  s.addText([{ text: "SADJINA Christ", options: { bold: true, color: C.white, fontSize: 12, breakLine: true } },
    { text: "Open Data Challenge · Défi 01 — Togo AI Lab / MESPTN — novembre 2026\nLes données sont publiques ; les calculs, les choix de méthode et les erreurs éventuelles sont les miens.", options: { color: "9FB8AC", fontSize: 9.5 } }],
    { x: 0.6, y: 4.44, w: 5.9, h: 0.72, fontFace: BF, isTextBox: true, margin: 0, valign: "top" });
  s.addNotes("L'archive livrée contient le pipeline, les 17 fichiers bruts non modifiés, les tables agrégées, le code des sept pages et la liste des sources en JSON.");
}

pres.writeFile({ fileName: OUT }).then(() => console.log("OK → " + OUT));
