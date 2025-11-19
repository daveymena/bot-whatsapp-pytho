import { NextResponse } from 'next/server'

const PYTHON_API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

export async function POST() {
  try {
    const response = await fetch(`${PYTHON_API}/admin/whatsapp/disconnect`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error disconnecting WhatsApp:', error)
    return NextResponse.json(
      { success: false, error: 'Error al desconectar WhatsApp' },
      { status: 500 }
    )
  }
}
