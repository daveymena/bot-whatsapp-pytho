import { NextResponse } from 'next/server'

const BAILEYS_SERVER = 'http://localhost:3002'

export async function POST() {
  try {
    // Primero desconectar
    await fetch(`${BAILEYS_SERVER}/disconnect`, {
      method: 'POST'
    })
    
    // Esperar un poco
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Error resetting WhatsApp:', error)
    return NextResponse.json(
      { success: false, error: 'Error al resetear WhatsApp' },
      { status: 500 }
    )
  }
}
