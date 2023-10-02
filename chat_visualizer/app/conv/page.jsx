import { Chat } from "@/components/chat";
import { getConversation } from "@/lib/files";

export default function ChatPage({ params, searchParams }) {
    const { id } = searchParams;
    const { history: data, config } = getConversation(id);
    return (<>
        <Chat data={data} config={config} />
    </>)
}