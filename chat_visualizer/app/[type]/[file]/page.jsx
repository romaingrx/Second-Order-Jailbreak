import { ConversationShowcase } from "@/components/Conversation/showcase";
import { listConversations } from "@/lib/files";

export function generateStaticParams(){
  const conversations = listConversations();
  let params = []
  for (const [type, files] of Object.entries(conversations)) {
    for (const file of files) {
      params.push({ type, file: file.file });
    }
  }
  return params;
}

export default function ChatPage({ params }) {
  const { type, file } = params;
  const conversations = listConversations();
  return (
    <>
      <ConversationShowcase
        conversations={conversations}
        initialConversation={{ type, file }}
        onSelectRedirect
      />
    </>
  );
}
