export type JewelleryView = {
  kind: "renders" | "cad" | "wireframe" | "dimensions" | "sketches";
  label: string;
  image: string;
  full: string;
  width: number;
  height: number;
};

export type JewelleryPiece = {
  slug: string;
  title: string;
  category: string;
  description: string;
  story: string;
  note: string;
  card: string;
  cardWireframe: string;
  views: JewelleryView[];
  downloads: { label: string; href: string }[];
  specification?: string;
};

function view(
  slug: string,
  file: string,
  kind: JewelleryView["kind"],
  label: string,
  width: number,
  height: number,
  full = `${file}.png`,
): JewelleryView {
  return {
    kind,
    label,
    image: `/jewellery/${slug}/${file}.webp`,
    full: `/jewellery/${slug}/${full}`,
    width,
    height,
  };
}

function specificationViews(slug: string): JewelleryView[] {
  const sheets = [
    ["01-design-specification-overview.svg", "Design & specification overview"],
    ["02-assembly-dimensions.svg", "Assembly dimensions"],
    ["03-construction-stone-setting.svg", "Construction & stone setting"],
    ["04-materials,-finish-bill-of-materials.svg", "Materials, finish & bill of materials"],
    ["05-manufacturing-route-tolerances.svg", "Manufacturing route & tolerances"],
    ["06-sample-review-quality-control.svg", "Sample review & quality control"],
    ["07-costing,-moq-supplier-quotation.svg", "Costing, MOQ & supplier quotation"],
    ["08-release-checklist-source-control.svg", "Sample approval & release"],
  ];
  return sheets.map(([file, label]) => ({
    kind: "dimensions",
    label,
    image: `/jewellery/${slug}/technical/${file}`,
    full: `/jewellery/${slug}/technical/${file}`,
    width: 1190,
    height: 842,
  }));
}

export const jewelleryPieces: JewelleryPiece[] = [
  {
    slug: "confluence",
    title: "Confluence",
    category: "Three-stone ring",
    description: "Two sweeping shoulders. Three graduated stones.",
    story:
      "I brought two opposing sweeps together around three stones. The open setting keeps the centre in view, while the band carries the movement around the finger.",
    note: "Digital design study. Proposed materials and stone sizes; physical sample approval pending.",
    card: "/jewellery/confluence/render-01-environment.webp",
    cardWireframe: "/jewellery/confluence/cover-wireframe.webp",
    views: [
      view("confluence", "render-01-environment", "renders", "Environment render", 2400, 2400),
      view("confluence", "render-02-studio", "renders", "Studio render", 2400, 2400),
      view("confluence", "render-03", "renders", "Setting detail", 2800, 2800),
      view(
        "confluence",
        "wireframe-01",
        "wireframe",
        "Pre-setting model wireframe",
        1800,
        1600,
      ),
      view(
        "confluence",
        "wireframe-02",
        "wireframe",
        "Open stock-prong setting wireframe",
        1800,
        1600,
      ),
      ...specificationViews("confluence"),
      view("confluence", "sketches-01", "sketches", "Concept studies", 1600, 1380, "sketches.svg"),
    ],
    specification: "/jewellery/confluence/specification.html",
    downloads: [
      {
        label: "Technical specification / 8 sheets",
        href: "/jewellery/confluence/technical-specification.pdf",
      },
      { label: "Technical drawing", href: "/jewellery/confluence/dimensions.pdf" },
    ],
  },
  {
    slug: "iced-out-ring",
    title: "Iced-out ring",
    category: "Stone-set band",
    description: "A bold iced-out gold ring with dense pavé-set stones for a clean, luxurious finish.",
    story:
      "A stone-set band designed for continuous sparkle, with angled outer rows and open galleries that keep the setting light and refined.",
    note: "Digital design study. Model units interpreted as millimetres; nominal ring size and stone schedule TBC.",
    card: "/jewellery/iced-out-ring/render-01-gallery.webp",
    cardWireframe: "/jewellery/iced-out-ring/cover-wireframe.webp",
    views: [
      view("iced-out-ring", "render-01-gallery", "renders", "Gallery render", 3000, 2250),
      view("iced-out-ring", "render-01", "renders", "Beauty render", 1600, 1400),
      ...specificationViews("iced-out-ring"),
    ],
    specification: "/jewellery/iced-out-ring/specification.html",
    downloads: [
      {
        label: "Technical specification / 8 sheets",
        href: "/jewellery/iced-out-ring/technical-specification.pdf",
      },
      { label: "Technical drawing", href: "/jewellery/iced-out-ring/dimensions.pdf" },
    ],
  },
  {
    slug: "heartline-pendant",
    title: "Heartline",
    category: "Heart pendant",
    description: "An open heart, with a second line held inside.",
    story:
      "I worked with two heart-shaped lines: an outer sweep of stones and a smaller gold line inside. The open centre lets the shape read clearly without filling it in.",
    note: "Digital design study. Proposed gold finish and stones; chain shown for presentation.",
    card: "/jewellery/heartline-pendant/render-01-studio.webp",
    cardWireframe: "/jewellery/heartline-pendant/cover-wireframe.webp",
    views: [
      view("heartline-pendant", "render-01-studio", "renders", "Studio render", 2400, 2400),
      view("heartline-pendant", "render-01", "renders", "Pendant with reference chain", 1700, 1900),
      view(
        "heartline-pendant",
        "dimensions-01",
        "dimensions",
        "Pendant dimensions",
        1600,
        1120,
        "dimensions.svg",
      ),
    ],
    downloads: [
      {
        label: "Pendant technical drawing",
        href: "/jewellery/heartline-pendant/dimensions.svg",
      },
    ],
  },
  {
    slug: "ribbon-leaf",
    title: "Ribbon Leaf",
    category: "Drop earrings",
    description: "A ribbon-shaped leaf, suspended beneath a cluster of stones.",
    story: "I paired a small stone cluster with an articulated line of settings and an open leaf-shaped drop. A central stone sits inside the ribbon, with smaller stones following one edge.",
    note: "Digital design study. Dimensions describe the metal assembly; materials and production specifications TBC.",
    card: "/jewellery/ribbon-leaf/render-01-studio.webp",
    cardWireframe: "/jewellery/ribbon-leaf/cover-wireframe.webp",
    views: [
      view("ribbon-leaf", "render-01-studio", "renders", "Studio render", 2500, 3000),
      { kind: "dimensions", label: "Assembly dimensions / model measurements", image: "/jewellery/ribbon-leaf/dimensions.svg", full: "/jewellery/ribbon-leaf/dimensions.svg", width: 1600, height: 1120 },
    ],
    downloads: [{ label: "Dimension drawing", href: "/jewellery/ribbon-leaf/dimensions.svg" }],
  },
];
