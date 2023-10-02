import { listConversations } from "@/lib/files";
import { ConversationShowcase } from "./showcase";

export function ConversationPlayground() {
    const files = listConversations();
    return <ConversationShowcase conversationList={files} />
}