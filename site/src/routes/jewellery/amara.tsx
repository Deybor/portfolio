import { createFileRoute } from "@tanstack/react-router";
import { AmaraPage } from "@/components/jewellery/amara-page";

export const Route = createFileRoute("/jewellery/amara")({
  head: () => ({
    meta: [
      { title: "What if Amara had a stud? — Amara Nest" },
      {
        name: "description",
        content:
          "An independent digital study of a companion stud for the Amara necklace, with design decisions, technical drawings and specifications.",
      },
    ],
  }),
  component: AmaraPage,
});
