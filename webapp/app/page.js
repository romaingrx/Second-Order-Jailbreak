import { listConversations } from "@/lib/files";
import { redirect } from "next/navigation";

function App() {
  const conversations = listConversations();
  const type = Object.keys(conversations)[Math.floor(Math.random() * Object.keys(conversations).length)];
  const conv = conversations[type][Math.floor(Math.random() * conversations[type].length)];
  redirect(`${type}/${conv.file}`);
}

export default App;
