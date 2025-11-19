import { NextResponse } from 'next/server'

export async function POST() {
  // Mantener sesión activa
  return NextResponse.json({ success: true, timestamp: Date.now() })
}
