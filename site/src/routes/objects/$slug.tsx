import { createFileRoute, Link, notFound } from "@tanstack/react-router";
import { ObjectProject } from "@/components/objects/object-project";
import { printedObjects } from "@/lib/printed-objects";
export const Route = createFileRoute("/objects/$slug")({
  loader: ({ params }) => {
    const project = printedObjects.find((item) => item.slug === params.slug);
    if (!project) throw notFound();
    return project;
  },
  head: ({ loaderData }) => ({
    meta: [{ title: `${loaderData?.title ?? "Object"} — Adesina Adebola` }],
  }),
  component: ProjectRoute,
  notFoundComponent: () => (
    <main className="collection" id="content">
      <div className="collection-wrap collection-intro">
        <div>
          <h1>Object not found</h1>
          <Link className="collection-link" to="/objects">
            Browse the object collection →
          </Link>
        </div>
      </div>
    </main>
  ),
});
function ProjectRoute() {
  const project = Route.useLoaderData();
  return <ObjectProject key={project.slug} project={project} />;
}
