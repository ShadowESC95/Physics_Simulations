from pylatex import Document, Section, Subsection, Figure, NoEscape

doc = Document()
doc.preamble.append(NoEscape(r'\title{Ξχ Phase Report}'))
doc.preamble.append(NoEscape(r'\author{ShadowESC95}'))
doc.append(NoEscape(r'\maketitle'))

with doc.create(Section("Phase Spiral")):
    with doc.create(Figure(position='h!')) as fig:
        fig.add_image('plots/phase_spiral.png', width='120mm')
        fig.add_caption("Ξχ entropy-curvature-drift spiral.")

with doc.create(Section("UMAP Stability")):
    with doc.create(Figure(position='h!')) as fig:
        fig.add_image('plots/xi_chi_umap_clusters.png', width='120mm')
        fig.add_caption("UMAP clustering of Ξχ fields.")

doc.generate_pdf("XiChi_Report", clean_tex=False)
