import { useEffect } from "react";

export function ImagePreview() {
  useEffect(() => {
    if (document.getElementById("portfolio-image-viewer-script")) return;
    const script = document.createElement("script");
    script.id = "portfolio-image-viewer-script";
    script.src = "/image-viewer.js?v=reviewer-navigation";
    document.body.append(script);
  }, []);
  return null;
}
