'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Zap, Plus, Trash2, Upload, Download, BookOpen } from 'lucide-react'
import { toast } from 'sonner'

interface TrainingExample {
  id: string
  question: string
  answer: string
  category: string
}

export function TrainingTab() {
  const [examples, setExamples] = useState<TrainingExample[]>([
    {
      id: '1',
      question: '¿Cuáles son los métodos de pago?',
      answer: 'Aceptamos PayPal, MercadoPago, transferencia bancaria y efectivo.',
      category: 'pagos'
    },
    {
      id: '2',
      question: '¿Hacen envíos?',
      answer: 'Sí, hacemos envíos a todo el país. El costo varía según la ubicación.',
      category: 'envios'
    }
  ])

  const [newExample, setNewExample] = useState({
    question: '',
    answer: '',
    category: ''
  })

  const addExample = () => {
    if (!newExample.question || !newExample.answer) {
      toast.error('Completa todos los campos')
      return
    }

    const example: TrainingExample = {
      id: Date.now().toString(),
      ...newExample
    }

    setExamples([...examples, example])
    setNewExample({ question: '', answer: '', category: '' })
    toast.success('Ejemplo agregado')
  }

  const removeExample = (id: string) => {
    setExamples(examples.filter(e => e.id !== id))
    toast.success('Ejemplo eliminado')
  }

  const handleSave = async () => {
    try {
      // Aquí iría la lógica para guardar en el backend
      toast.success('Entrenamiento guardado correctamente')
    } catch (error) {
      toast.error('Error al guardar el entrenamiento')
    }
  }

  const exportTraining = () => {
    const data = JSON.stringify(examples, null, 2)
    const blob = new Blob([data], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'training-data.json'
    a.click()
    toast.success('Datos exportados')
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Entrenamiento del Bot</h2>
        <p className="text-gray-600 mt-1">Enseña al bot con ejemplos de preguntas y respuestas</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Formulario para agregar ejemplos */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Plus className="w-5 h-5 text-green-600" />
                Agregar Ejemplo de Entrenamiento
              </CardTitle>
              <CardDescription>
                Enseña al bot cómo responder a preguntas específicas
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="question">Pregunta del Cliente</Label>
                <Input
                  id="question"
                  value={newExample.question}
                  onChange={(e) => setNewExample({ ...newExample, question: e.target.value })}
                  placeholder="¿Cuál es el horario de atención?"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="answer">Respuesta del Bot</Label>
                <Textarea
                  id="answer"
                  value={newExample.answer}
                  onChange={(e) => setNewExample({ ...newExample, answer: e.target.value })}
                  placeholder="Nuestro horario es de lunes a viernes de 9am a 6pm..."
                  rows={4}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="category">Categoría</Label>
                <Input
                  id="category"
                  value={newExample.category}
                  onChange={(e) => setNewExample({ ...newExample, category: e.target.value })}
                  placeholder="horarios, pagos, envios, etc."
                />
              </div>

              <Button onClick={addExample} className="w-full">
                <Plus className="w-4 h-4 mr-2" />
                Agregar Ejemplo
              </Button>
            </CardContent>
          </Card>

          {/* Lista de ejemplos */}
          <Card>
            <CardHeader>
              <CardTitle>Ejemplos de Entrenamiento ({examples.length})</CardTitle>
              <CardDescription>
                Estos ejemplos ayudan al bot a aprender
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {examples.map((example) => (
                  <div
                    key={example.id}
                    className="p-4 border border-gray-200 rounded-lg hover:border-gray-300 transition-colors"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex-1">
                        <p className="font-medium text-gray-900 mb-1">
                          {example.question}
                        </p>
                        <p className="text-sm text-gray-600 mb-2">
                          {example.answer}
                        </p>
                        <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
                          {example.category}
                        </span>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeExample(example.id)}
                        className="text-red-600 hover:text-red-700 hover:bg-red-50"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>

              {examples.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  <BookOpen className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                  <p>No hay ejemplos de entrenamiento</p>
                  <p className="text-sm">Agrega ejemplos para mejorar las respuestas del bot</p>
                </div>
              )}
            </CardContent>
          </Card>

          <div className="flex gap-3">
            <Button onClick={handleSave} className="flex-1">
              <Zap className="w-4 h-4 mr-2" />
              Guardar y Entrenar
            </Button>
            <Button onClick={exportTraining} variant="outline">
              <Download className="w-4 h-4 mr-2" />
              Exportar
            </Button>
            <Button variant="outline">
              <Upload className="w-4 h-4 mr-2" />
              Importar
            </Button>
          </div>
        </div>

        {/* Información y estadísticas */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Estadísticas</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Total de ejemplos</span>
                <span className="text-2xl font-bold text-gray-900">{examples.length}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Categorías</span>
                <span className="text-2xl font-bold text-gray-900">
                  {new Set(examples.map(e => e.category)).size}
                </span>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-green-50 to-emerald-50 border-green-200">
            <CardContent className="pt-6">
              <div className="text-center">
                <Zap className="w-8 h-8 text-green-600 mx-auto mb-2" />
                <p className="text-sm font-medium text-gray-900 mb-2">
                  Entrenamiento Continuo
                </p>
                <p className="text-xs text-gray-600">
                  El bot aprende automáticamente de cada conversación y mejora con el tiempo
                </p>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200">
            <CardContent className="pt-6">
              <div className="space-y-3">
                <p className="text-sm font-medium text-gray-900">💡 Consejos</p>
                <ul className="text-xs text-gray-600 space-y-2">
                  <li>• Usa preguntas reales de clientes</li>
                  <li>• Sé específico en las respuestas</li>
                  <li>• Agrupa por categorías similares</li>
                  <li>• Actualiza regularmente</li>
                </ul>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
