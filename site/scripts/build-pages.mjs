import { spawnSync } from "node:child_process";

for (const args of [["scripts/with-app-env.mjs", "vite", "build"], ["scripts/finish-pages.mjs"]]) {
  const result = spawnSync(process.execPath, args, { stdio: "inherit", env: { ...process.env, VITE_GITHUB_PAGES: "true" } });
  if (result.status !== 0) process.exit(result.status || 1);
}
