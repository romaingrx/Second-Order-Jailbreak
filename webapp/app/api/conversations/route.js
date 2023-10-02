import { listConversations } from "@/lib/files";
import { NextResponse } from "next/server";

export async function GET() {
  const conversations = listConversations(true);
  return NextResponse.json(conversations);
}
