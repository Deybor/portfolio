import ts from "typescript";

// Adapt public URLs only in the Pages build; local previews keep their approved paths.
export function pagesAssetPlugin(base) {
  const prefix = (value) => value.startsWith("/") && !value.startsWith("//")
    ? `${base.slice(0, -1)}${value}` : value;
  const isAsset = (value) => /^\/(?!\/)/.test(value) &&
    (/\.(?:png|jpe?g|webp|avif|gif|svg|mp4|webm|pdf|html|css|js|ico|webmanifest)(?:[?#]|$)/i.test(value) ||
      /^\/(?:jewellery|objects|portfolio)\/[^/]+\/$/.test(value));
  return {
    name: "portfolio-pages-public-urls",
    enforce: "pre",
    transform(code, id) {
      if (!id.includes("/src/") && !id.includes("\\src\\")) return;
      if (id.endsWith(".json")) {
        const rewrite = (value) => typeof value === "string" ? (isAsset(value) ? prefix(value) : value)
          : Array.isArray(value) ? value.map(rewrite)
          : value && typeof value === "object" ? Object.fromEntries(Object.entries(value).map(([key, val]) => [key, rewrite(val)])) : value;
        return { code: JSON.stringify(rewrite(JSON.parse(code))), map: null };
      }
      if (!/\.[jt]sx?$/.test(id)) return;
      const source = ts.createSourceFile(id, code, ts.ScriptTarget.Latest, true, id.endsWith("x") ? ts.ScriptKind.TSX : ts.ScriptKind.TS);
      let changed = false;
      const transformed = ts.transform(source, [(context) => {
        const visit = (node) => {
          const parent = node.parent;
          const urlAttribute = parent && ts.isJsxAttribute(parent) && /^(href|src|poster)$/.test(parent.name.getText(source));
          const urlProperty = parent && ts.isPropertyAssignment(parent) && /^(href|src|image|full|card|cardWireframe|poster|video|thumbnail)$/.test(parent.name.getText(source).replace(/["']/g, ""));
          if ((ts.isStringLiteral(node) || ts.isNoSubstitutionTemplateLiteral(node)) &&
            (isAsset(node.text) || ((urlAttribute || urlProperty) && node.text.startsWith("/")))) {
            const value = prefix(node.text);
            if (value !== node.text) { changed = true; return ts.isStringLiteral(node) ? ts.factory.createStringLiteral(value) : ts.factory.createNoSubstitutionTemplateLiteral(value); }
          }
          if (ts.isTemplateExpression(node) && node.head.text.startsWith("/") &&
              (urlProperty || node.head.text === "/portfolio/" || /\.(?:png|jpe?g|webp|avif|gif|svg|mp4|webm|pdf|html)(?:[?#]|$)/i.test(node.templateSpans.at(-1).literal.text))) {
            const value = prefix(node.head.text);
            if (value !== node.head.text) { changed = true; return ts.factory.updateTemplateExpression(node, ts.factory.createTemplateHead(value), node.templateSpans); }
          }
          return ts.visitEachChild(node, visit, context);
        };
        return (node) => ts.visitNode(node, visit);
      }]);
      const result = changed ? { code: ts.createPrinter().printFile(transformed.transformed[0]), map: null } : undefined;
      transformed.dispose();
      return result;
    },
  };
}
