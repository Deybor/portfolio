export type Project = {
  id: string;
  title: string;
  category: "Product" | "Beauty" | "Motion";
  label: string;
  cover: string;
  fit?: "contain";
  video?: string;
  images: [string, string][];
  intro: string;
  focus: string;
  details: string;
};

const asset = (file: string) => `/portfolio/${file}`;

export const projects: Project[] = [
  {
    id: "sound",
    title: "Sound in context",
    category: "Product",
    label: "Product / Lifestyle setting",
    cover: asset("speaker-wide.webp"),
    images: [
      [asset("speaker-wide.webp"), "A warm setting for an orange portable speaker."],
      [asset("speaker-detail.webp"), "A closer view of the grille, lighting, and wood surface."],
    ],
    intro: "A portable speaker, placed in the warmth of an everyday interior.",
    focus:
      "The scene pairs a saturated orange speaker with warm timber and soft background lighting. The two viewpoints move from a balanced product composition to a closer material study.",
    details:
      "Fine grille detail, wood grain, and a shallow depth of field give a familiar object a tactile presence.",
  },
  {
    id: "titan",
    title: "A new perspective on flight",
    category: "Product",
    label: "Titan Air Mobility / eVTOL visualization",
    cover: asset("titan-air.webp"),
    fit: "contain",
    images: [[asset("titan-air.webp"), "eVTOL aircraft visualization for Titan Air Mobility."]],
    intro: "An eVTOL aircraft visualization created for Titan Air Mobility.",
    focus:
      "An elevated three-quarter view brings the cabin, wings, and rotor arrangement into one composition. Directional light traces the aircraft against a dark setting.",
    details: "3D visualization with a focus on the aircraft form, reflective surfaces, and lighting.",
  },
  {
    id: "strongfood",
    title: "Strong Bar — Variant A",
    category: "Product",
    label: "StrongFood / Packaging visualization",
    cover: asset("strong-box-yellow.webp"),
    fit: "contain",
    images: [
      [asset("strong-bar-yellow.webp"), "Chocolate Hazelnut — Variant A bar."],
      [asset("strong-box-yellow.webp"), "Chocolate Hazelnut — matching display carton."],
      [asset("strong-bar-blue.webp"), "White Blueberry — Variant A bar."],
      [asset("strong-box-blue.webp"), "White Blueberry — matching display carton."],
      [asset("strong-bar-green.webp"), "Dark Choc Peanut Flavour — Variant A bar."],
      [asset("strong-box-green.webp"), "Dark Choc Peanut Flavour — matching display carton."],
    ],
    intro:
      "Bar and display-carton visualizations for StrongFood, bringing the Variant A range together across three flavours.",
    focus:
      "Yellow, blue, and green distinguish the three variants. Each wrapper is paired with its matching retail carton to show the packaging as a complete range.",
    details: "3D packaging visualization across individual wrappers and filled display cartons.",
  },
  {
    id: "serum",
    title: "A quieter kind of luxury",
    category: "Beauty",
    label: "Beauty / Product visualization",
    cover: asset("serum.webp"),
    images: [
      [asset("serum.webp"), "A minimal daylight composition with a glass platform."],
      [asset("serum-spa.webp"), "The serum in a candlelit spa setting."],
    ],
    intro: "Two visual worlds for the same serum: quiet daylight and a richly layered spa scene.",
    focus:
      "The first image uses a restrained palette and directional shadows. The second introduces towels, stone, candles, and botanicals to place the product in a ritual of care.",
    details:
      "Dark glass anchors both compositions, while reflections and soft-focus backgrounds separate the product from its surroundings.",
  },
  {
    id: "headset",
    title: "Form in suspension",
    category: "Product",
    label: "Technology / Product visualization",
    cover: asset("headset.webp"),
    images: [
      [asset("headset.webp"), "Multiple headset views arranged against a white background."],
    ],
    intro: "A study of repeated form, reflective surfaces, and a vivid orange accent.",
    focus:
      "Suspended headsets create a rhythmic composition. Different angles reveal the curved faceplate, padded interior, and woven strap.",
    details:
      "Glossy black, soft fabric, and metallic components sit together in a high-contrast lighting treatment.",
  },
  {
    id: "skincare",
    title: "Daily essentials",
    category: "Beauty",
    label: "Beauty / Packaging visualization",
    cover: asset("skincare.webp"),
    images: [
      [asset("skincare.webp"), "A diagonal arrangement of two skincare products with foliage shadows."],
    ],
    intro: "A skincare pairing framed by soft shadows, clear droplets, and pale surfaces.",
    focus:
      "A diagonal layout introduces movement to a still image, while the contrasting labels keep each product distinct.",
    details: "Subtle translucency and reflected light support the clean, fresh feel of the composition.",
  },
  {
    id: "gpu",
    title: "Engineered in light",
    category: "Product",
    label: "Technology / Product visualization",
    cover: asset("gpu-detail.webp"),
    images: [
      [asset("gpu-detail.webp"), "A close study of graphics card fans and metallic surfaces."],
      [asset("gpu.webp"), "Two graphics cards shown in an upright composition."],
    ],
    intro: "Graphics card studies exploring technical detail and cool, sculptural lighting.",
    focus:
      "Two compositions present the RTX 3080 form at different scales, from the cooling fans and layered fins to the full silhouette.",
    details:
      "Blue highlights against silver and black surfaces emphasize the geometry and repetition of the cooling assembly.",
  },
  {
    id: "candles",
    title: "After the flame",
    category: "Beauty",
    label: "Lifestyle / Lighting study",
    cover: asset("candles.webp"),
    images: [
      [
        asset("candles.webp"),
        "Glass candles on a wooden table, with a smoke trail and blurred background lights.",
      ],
    ],
    intro: "A still life built around the moment just after a candle goes out.",
    focus:
      "A fine trail of smoke draws attention to the foreground candle. The second flame and distant lights carry warmth through the scene.",
    details: "Glass, wax, wood, and smoke offer contrasting surfaces within a single low-light composition.",
  },
  {
    id: "energy",
    title: "Energy in motion",
    category: "Motion",
    label: "Motion / Product film",
    cover: asset("energy-film.jpg"),
    video: asset("energy-film.mp4"),
    images: [[asset("energy.webp"), "A close product detail with cyan fluid and condensation."]],
    intro: "A product animation exploring energy, surface detail, and movement.",
    focus:
      "Watch the film for the full sequence, with a still frame below for a closer look at the product treatment.",
    details: "Product animation and rendering created in Blender.",
  },
  {
    id: "fluid",
    title: "Fluid study",
    category: "Motion",
    label: "Motion / Fluid animation",
    cover: asset("fluid-film.jpg"),
    video: asset("fluid-film.mp4"),
    images: [],
    intro: "A short exploration of fluid movement around a product.",
    focus:
      "The clip brings flowing forms into a product scene, exploring the relationship between the object and the surrounding motion.",
    details: "Animation study created in Blender.",
  },
  {
    id: "black",
    title: "Industrial form",
    category: "Motion",
    label: "dev.tools / Industrial visualization",
    cover: asset("dev-tools-workshop.webp"),
    fit: "contain",
    video: asset("black-film.mp4"),
    images: [
      [
        asset("dev-tools-workshop.webp"),
        "PC enclosures in a workshop setting, created for dev.tools.",
      ],
    ],
    intro:
      "An industrial form study for dev.tools, pairing a rotating enclosure animation with a workshop scene.",
    focus:
      "The film explores the perforated structure in motion. The still places three enclosure configurations among tools and computer components.",
    details: "3D visualization and animation created in Blender.",
  },
  {
    id: "motion",
    title: "The reveal",
    category: "Motion",
    label: "Motion / Animation",
    cover: asset("motion-film.jpg"),
    video: asset("motion-film.mp4"),
    images: [],
    intro: "A restrained packaging reveal, moving from darkness into light.",
    focus:
      "Close framing and directional highlights gradually reveal a pale, branded package against a black background.",
    details: "Animation created in Blender.",
  },
];

export const filters = [
  { id: "All", label: "All work" },
  { id: "Product", label: "Product" },
  { id: "Beauty", label: "Beauty & lifestyle" },
  { id: "Motion", label: "Motion" },
] as const;

export type FilterId = (typeof filters)[number]["id"];
