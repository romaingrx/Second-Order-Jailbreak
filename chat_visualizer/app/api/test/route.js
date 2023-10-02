import { getGitRoot, listConversations } from "@/lib/files";
import { NextResponse } from "next/server";

export async function GET(request) {
    const id = request.nextUrl.searchParams.get("id");
    const type = request.nextUrl.searchParams.get("type");
    const conversations = await fetch('/api/conversations').then(res => res.json());
    const conversation = conversations[type].find(c => c === id);
    return NextResponse.json(conversation);
}