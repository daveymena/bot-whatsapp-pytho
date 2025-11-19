import { NextResponse } from 'next/server'

const BAILEYS_SERVER = 'http://localhost:3002'

export async function POST() {
  try {
    // Limpiar sesión en el servidor Baileys
    const cleanupResponse = await fetch(`${BAILEYS_SERVER}/cleanup`, {
      method: 'POST'
    })
    
    if (!cleanupResponse.ok) {
      throw new Error('Error al limpiar sesión en servidor Baileys')
    }
    
    const cleanupData = await cleanupResponse.json()
    
    return NextResponse.json({
      success: true,
      message: 'Sesión limpiada correctamente',
      details: cleanupData
    })
  } catch (error) {
    console.error('Error cleaning up WhatsApp:', error)
    return NextResponse.json(
      {
        success: false,
        error: 'Error al limpiar sesión',
        details: {
          memoryCleared: false,
          filesDeleted: false
        }
      },
      { status: 500 }
    )
  }
}
