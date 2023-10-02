import { getConversation } from "@/lib/files";
import { NextResponse } from "next/server"

export async function GET(request) {
    const id = request.nextUrl.searchParams.get('id')
    const conversation = getConversation(id);
    return NextResponse.json(conversation)
}