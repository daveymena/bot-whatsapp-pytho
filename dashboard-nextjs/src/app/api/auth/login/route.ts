import { NextRequest, NextResponse } from 'next/server'

const PYTHON_API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    // Llamar directamente al backend de Python
    const response = await fetch(`${PYTHON_API}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })

    const data = await response.json()

    if (!response.ok) {
      return NextResponse.json(
        { success: false, error: data.detail || 'Error al iniciar sesión' },
        { status: response.status }
      )
    }

    // Devolver la respuesta del backend directamente
    return NextResponse.json(data)
  } catch (error) {
    console.error('Login error:', error)
    return NextResponse.json(
      { success: false, error: 'Error de conexión' },
      { status: 500 }
    )
  }
}
