import { getGitRoot, listConversations } from "@/lib/files";
import { NextResponse } from "next/server";

export async function GET() {
    const root = getGitRoot();
    const conversations = listConversations();
    return NextResponse.json({ root, conversations });
}