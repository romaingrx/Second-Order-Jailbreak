import { getConversation } from "@/lib/files";
import { NextResponse } from "next/server"

export async function GET(request) {
    const id = request.nextUrl.searchParams.get('id')
    console.log({ id })
    const conversation = getConversation(id);
    console.log({ conversation })
    return NextResponse.json(conversation)
}