import { getConversation } from "@/lib/files";
import { NextResponse } from "next/server"

export async function GET(request, { params }) {
    const { id } = params;
    const conversation = getConversation(id);
    return NextResponse.json(conversation)
}