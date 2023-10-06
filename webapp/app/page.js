import { listConversations } from "@/lib/files";
import { redirect } from "next/navigation";

function App() {
  const conversations = listConversations();

  let type = null;
  let file = null;
  if (process.env.DEFAULT_CONVERSATION) {
    type = process.env.DEFAULT_CONVERSATION.split('/')[0];
    file = process.env.DEFAULT_CONVERSATION.split('/')[1];
    if (!conversations[type] || !conversations[type].find(c => c.file === file)) {
        type = null;
        file = null;
    }
  }
  type = type || Object.keys(conversations)[Math.floor(Math.random() * Object.keys(conversations).length)];
  file = file || conversations[type][Math.floor(Math.random() * conversations[type].length)].file;

  redirect(`${type}/${file}`);
}

export default App;
