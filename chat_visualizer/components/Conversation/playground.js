import { listConversations } from "@/lib/files";
import { ConversationShowcase } from "./showcase";

export function ConversationPlayground() {
    const conversations = listConversations();
    return <ConversationShowcase conversations={conversations} />
}