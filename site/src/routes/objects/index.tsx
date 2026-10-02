import { createFileRoute } from "@tanstack/react-router";
import { ObjectsIndex } from "@/components/objects/objects-index";
export const Route = createFileRoute("/objects/")({
  head: () => ({
    meta: [
      { title: "Printed Objects — Adesina Adebola" },
      {
        name: "description",
        content:
          "Explore ten trophy and medal designs through beauty renders, Zenith Cup wireframes and original award design drawings.",
      },
    ],
  }),
  component: ObjectsIndex,
});
