import { useState, useEffect } from 'react';
import axios from 'axios';
import { User, Clock } from 'lucide-react';

export default function Conversations() {
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      const response = await axios.get('http://localhost:3000/admin/conversations/recent');
      setConversations(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading conversations:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Cargando conversaciones...</div>;
  }

  return (
    <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Conversaciones Recientes</h2>
      
      <div className="space-y-4">
        {conversations.map((conv, index) => (
          <div key={index} className="flex items-start gap-3 p-4 hover:bg-gray-50 rounded-lg transition-colors">
            <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
              <User size={20} className="text-green-600" />
            </div>
            <div className="flex-1">
              <div className="flex items-center justify-between mb-1">
                <p className="font-medium text-gray-900">{conv.phone}</p>
                <span className="text-xs text-gray-500 flex items-center gap-1">
                  <Clock size={12} />
                  {new Date(conv.created_at).toLocaleTimeString()}
                </span>
              </div>
              <p className="text-sm text-gray-600 mb-2">{conv.message.substring(0, 100)}...</p>
              <div className="flex gap-2">
                <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
                  {conv.intent}
                </span>
                <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                  {conv.sentiment}
                </span>
                <span className="px-2 py-1 bg-purple-100 text-purple-700 text-xs rounded-full">
                  {conv.agent_type}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
