import {
  createRootRoute,
  HeadContent,
  Outlet,
  Scripts,
  useRouterState,
} from "@tanstack/react-router";
import { AuthProvider } from "@/lib/auth/provider";
import { PreviewHostBridge } from "@/components/preview-host-bridge";
import { ImagePreview } from "@/components/image-preview";
import { SiteFooter, SiteHeader } from "@/components/site-chrome";
import { sitePath } from "@/lib/site-path";
import appCss from "../styles.css?url";

export const Route = createRootRoute({
  head: () => ({
    meta: [
      { charSet: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { title: "Deybor 3D — Adesina Adebola" },
      {
        name: "description",
        content:
          "Product visualization, animation, and jewellery design by Adesina Adebola. Lagos.",
      },
      { name: "theme-color", content: "#f2f0eb" },
    ],
    links: [
      { rel: "icon", type: "image/svg+xml", href: "/favicon.svg" },
      { rel: "stylesheet", href: appCss },
      { rel: "stylesheet", href: "/image-viewer.css" },
      {
        rel: "stylesheet",
        href: "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Manrope:wght@400;500;600;700&display=swap",
      },
      { rel: "manifest", href: "/__grok/manifest.webmanifest" },
      { rel: "apple-touch-icon", href: "/__grok/icon-180.png" },
    ],
  }),
  component: Root,
});

function Root() {
  const jewel = useRouterState({
    select: (s) =>
      sitePath(s.location.pathname).startsWith("/jewellery") || sitePath(s.location.pathname).startsWith("/objects"),
  });

  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <HeadContent />
      </head>
      <body className={jewel ? "world-jewel" : undefined}>
        <PreviewHostBridge />
        <AuthProvider>
          <a className="skip" href="#content">
            Skip to content
          </a>
          <SiteHeader />
          <Outlet />
          <SiteFooter />
          <ImagePreview />
        </AuthProvider>
        <Scripts />
      </body>
    </html>
  );
}
