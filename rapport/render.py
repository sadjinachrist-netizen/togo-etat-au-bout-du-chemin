import os, sys, glob
import win32com.client.dynamic as dyn
src = os.path.abspath("Rapport_Etat_au_bout_du_chemin_Togo.pptx")
out = os.path.abspath("slides")
os.makedirs(out, exist_ok=True)
for f in glob.glob(os.path.join(out, "*.png")):
    os.remove(f)
app = dyn.Dispatch("PowerPoint.Application")
pres = app.Presentations.Open(src, WithWindow=False)
for i, sl in enumerate(pres.Slides, 1):
    sl.Export(os.path.join(out, f"slide{i:02d}.png"), "PNG", 1600, 900)
pres.Close(); app.Quit()
print("rendu:", len(glob.glob(os.path.join(out, "*.png"))), "slides")
