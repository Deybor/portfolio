import { createFileRoute } from "@tanstack/react-router";
import { WorkbenchPage } from "@/components/jewellery/workbench-page";

export const Route = createFileRoute("/jewellery/workbench")({
  head: () => ({
    meta: [
      { title: "The Workbench — 3D modelling and drawings" },
      {
        name: "description",
        content:
          "Technical drawings, model views and review dimensions for the Amara Nest companion stud.",
      },
    ],
  }),
  component: WorkbenchPage,
});
