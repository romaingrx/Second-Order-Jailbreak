import { NextResponse } from "next/server"

export async function GET(request) {
    const host = request.nextUrl.host;
    const id = request.nextUrl.searchParams.get('id')
    const type = request.nextUrl.searchParams.get('type')
    const conversations = await fetch(`http://${host}/api/conversations`).then(res => res.json())
    const conversation = conversations[type].find(c => c.file === id)
    return NextResponse.json(conversation)
}