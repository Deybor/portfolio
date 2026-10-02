import { Link, useRouterState } from "@tanstack/react-router";

import { sitePath } from "@/lib/site-path";

export function SiteHeader() {
  const path = useRouterState({ select: (s) => sitePath(s.location.pathname) });
  const jewel = path.startsWith("/jewellery");
  const objects = path.startsWith("/objects");

  return (
    <header className="site-header" id="top">
      <Link className="wordmark" to="/" aria-label="Deybor 3D home">
        DEYBOR<span>3D</span>
      </Link>
      <nav className="site-nav" aria-label="Main">
        <a href="/#work">Product visualization</a>
        <Link to="/jewellery" aria-current={jewel ? "page" : undefined}>
          Jewellery
        </Link>
        <Link to="/objects" aria-current={objects ? "page" : undefined}>
          Printed objects
        </Link>
        <a href="/#about">About</a>
        <a href="/#contact">Contact</a>
      </nav>
    </header>
  );
}

export function SiteFooter() {
  const amara = useRouterState({
    select: (state) => sitePath(state.location.pathname) === "/jewellery/amara",
  });
  return (
    <footer className="site-footer">
      <Link className="wordmark" to="/">
        DEYBOR<span>3D</span>
      </Link>
      <p>Adesina Adebola / Lagos</p>
      <a href="#top">{amara ? "Back to top" : "Back to top ↑"}</a>
    </footer>
  );
}
