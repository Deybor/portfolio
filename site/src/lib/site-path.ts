/** Resolve the same route in the local preview and GitHub Pages subdirectory. */
export function sitePath(pathname: string) {
  const base = import.meta.env.BASE_URL.replace(/\/$/, "");
  const path = base && (pathname === base || pathname.startsWith(`${base}/`))
    ? pathname.slice(base.length) : pathname;
  return path.replace(/\/$/, "") || "/";
}
