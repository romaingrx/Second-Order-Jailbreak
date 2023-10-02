import fs from 'fs';
import path from 'path';
import { NextResponse } from "next/server";

export async function GET(request) {
    const folder = request.nextUrl.searchParams.get("folder ").replace(/\\/g, "/");
    const files = fs.readdirSync(folder);
    
    return NextResponse.json({ files });
}