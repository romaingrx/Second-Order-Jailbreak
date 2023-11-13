import { ConversationShowcase } from "@/components/Conversation/showcase";
import { listConversations } from "@/lib/files";

export function generateStaticParams() {
  const conversations = listConversations();
  let params = [];
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
      <div className="flex flex-col gap-4 py-4">
        <hr className="w-2/3 mx-auto"/>
        <div className="text-center text-gray-500 text-sm">
          Below, you can select a conversation to visualize the configuration of
          the agents, the messages they sent to each other and the analysis of
          the conversation by GPT-4.
        </div>
        <ConversationShowcase
          conversations={conversations}
          initialConversation={{ type, file }}
          onSelectRedirect
        />
      </div>
    </>
  );
}
