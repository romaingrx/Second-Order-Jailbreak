import fs from "fs";
import path from "path";

export function getGitRoot() {
  let currentPath = __dirname;
  while (!fs.existsSync(path.join(currentPath, ".git"))) {
    currentPath = path.join(currentPath, "..");
  }
  return currentPath;
}

export function listConversations(get_history = false) {
  const root = getGitRoot();
  const types = fs
    .readdirSync(root + "/output/report_output", { withFileTypes: true })
    .filter((dirent) => dirent.isDirectory())
    .map((dirent) => dirent.name);
  return Object.fromEntries(
    types.map((type) => {
      const files = fs.readdirSync(root + "/output/report_output/" + type);
      const files_and_infos = files.map((file) => ({
        file,
        ...getConversation(file, type, get_history),
      }));
      return [type, files_and_infos];
    })
  );
}

export function getConversationPath(id, type = null) {
  const root = getGitRoot();
  const types = fs.readdirSync(root + "/output/report_output");
  if (type === null) {
    for (const t of types) {
      const files = fs.readdirSync(root + "/output/report_output/" + t);
      if (files.includes(id)) {
        type = t;
        break;
      }
    }
  }
  if (type === null) {
    return null;
  }
  return root + "/output/report_output/" + type + "/" + id;
}

export function getConversation(
  id,
  type = null,
  get_history = true,
  get_config = true,
  get_analysis = true,
  get_review_prompt = true,
  get_result = true
) {
  function getJsonOrNull(path) {
    try {
      return JSON.parse(fs.readFileSync(path));
    } catch (e) {
      return null;
    }
  }

  const path = getConversationPath(id, type);
  const config = get_config ? getJsonOrNull(path + "/config.json") : null;
  const history = get_history ? getJsonOrNull(path + "/history.json") : null;
  const result = get_result ? getJsonOrNull(path + "/result.json") : null;
  const analysis = get_analysis
    ? getJsonOrNull(path + "/GPT4_analysis.json")
    : null;
  const review_prompt = get_review_prompt
    ? getJsonOrNull(path + "/GPT4_review_prompt.json")
    : null;

  return {
    config,
    history,
    result,
    analysis,
    review_prompt,
  };
}
