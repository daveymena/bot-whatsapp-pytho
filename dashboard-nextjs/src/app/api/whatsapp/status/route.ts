import { NextResponse } from 'next/server'

const PYTHON_API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

export async function GET() {
  try {
    const response = await fetch(`${PYTHON_API}/admin/whatsapp/status`, {
      cache: 'no-store'
    })
    
    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching WhatsApp status:', error)
    return NextResponse.json(
      {
        success: false,
        status: 'DISCONNECTED',
        qrCode: null,
        connection: {
          phoneNumber: null,
          lastConnectedAt: null,
          isActive: false
        }
      },
      { status: 200 }
    )
  }
}
