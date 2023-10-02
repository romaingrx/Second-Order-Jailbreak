import { getConversation } from "@/lib/files";
import { NextResponse } from "next/server"

export const runtime = 'nodejs';

export async function GET(request) {
    try {
        const id = request.nextUrl.searchParams.get('id')
        const conversation = getConversation(id);
        return NextResponse.json(conversation)
    } catch (e) {
        return NextResponse.error(e)
    }
}