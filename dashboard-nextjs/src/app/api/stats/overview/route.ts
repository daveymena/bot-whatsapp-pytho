import { NextResponse } from 'next/server'

export async function GET() {
  try {
    // Conectar con el backend Python
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:5000'
    
    const response = await fetch(`${backendUrl}/api/stats/overview`, {
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error('Failed to fetch stats from backend')
    }

    const data = await response.json()
    
    return NextResponse.json({
      success: true,
      stats: data
    })
  } catch (error) {
    console.error('Error fetching overview stats:', error)
    
    // Retornar datos de ejemplo si el backend no está disponible
    return NextResponse.json({
      success: true,
      stats: {
        totalConversations: 0,
        activeConversations: 0,
        totalProducts: 0,
        totalCustomers: 0,
        totalMessages: 0,
        isConnected: false
      }
    })
  }
}
