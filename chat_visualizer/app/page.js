import { ConversationShowcase } from "@/components/Conversation/showcase";
import { listConversations } from "@/lib/files";

function App() {
  const files = listConversations();
  return (
    <>
      <div className="text-zinc-900">
       <ConversationShowcase conversationList={files} />
      </div>
    </>
  );
}

export default App;
