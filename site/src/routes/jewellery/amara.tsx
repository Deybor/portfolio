import { createFileRoute } from "@tanstack/react-router";
import { AmaraPage } from "@/components/jewellery/amara-page";

export const Route = createFileRoute("/jewellery/amara")({
  head: () => ({
    meta: [
      { title: "What if Amara had a stud? — Amara Nest" },
      {
        name: "description",
        content:
          "My independent exploration of an Amara companion earring: the necklace, three directions, the selected stud and the 3D modelling behind it.",
      },
    ],
  }),
  component: AmaraPage,
});
