import { createFileRoute } from "@tanstack/react-router";
import { JewelleryLanding } from "@/components/jewellery/landing";

export const Route = createFileRoute("/jewellery/")({
  head: () => ({
    meta: [
      { title: "Jewellery Design — Adesina Adebola" },
      {
        name: "description",
        content:
          "Rings, a heart pendant, and an independent Amara companion earring study. Jewellery design, 3D modelling and visualization by Adesina Adebola.",
      },
    ],
  }),
  component: JewelleryLanding,
});
