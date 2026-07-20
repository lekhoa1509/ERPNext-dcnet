import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";
import { spawnSync } from "node:child_process";

function walk(directory) {
  return readdirSync(directory).flatMap((name) => {
    const path = join(directory, name);
    return statSync(path).isDirectory() ? walk(path) : [path];
  });
}

const files = walk("frontend/src").filter((path) => path.endsWith(".js"));
let failed = false;

for (const file of files) {
  const check = spawnSync(process.execPath, ["--check", file], { stdio: "inherit" });
  failed ||= check.status !== 0;

  const source = readFileSync(file, "utf8");
  if (/\bv-html\s*=/.test(source) && !file.endsWith("utils.js")) {
    console.error(`${file}: raw v-html requires explicit sanitization review`);
    failed = true;
  }

  const pendingControls = source.match(/<button[^>]+notify(?:LeadTab|Opportunity|Care|Activity)Action[^>]*>/gs) || [];
  for (const control of pendingControls) {
    if (!control.includes("showUnreadyFeatures")) {
      console.error(`${file}: unfinished production control is not feature-gated`);
      failed = true;
    }
  }
}

if (failed) process.exit(1);
console.log(`Checked ${files.length} frontend modules.`);
