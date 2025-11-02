import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, Phone, User, Calendar, Clock, Tag, AlertCircle, 
  CheckCircle, Star, Award, MessageSquare, Plus, Edit 
} from 'lucide-react';
import api from '../config/api';
import EvaluationForm from '../components/EvaluationForm';
import { useAuth } from '../context/AuthContext';

const CallDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [call, setCall] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showEvaluationForm, setShowEvaluationForm] = useState(false);
  const [editingEvaluation, setEditingEvaluation] = useState(null);

  useEffect(() => {
    fetchCallDetails();
  }, [id]);

  const fetchCallDetails = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/calls/${id}`);
      setCall(response.data);
    } catch (error) {
      console.error('Erro ao carregar detalhes da chamada:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveEvaluation = async (formData) => {
    try {
      if (editingEvaluation) {
        await api.put(`/evaluations/${editingEvaluation.id}`, formData);
      } else {
        await api.post('/evaluations', {
          ...formData,
          call_id: parseInt(id),
        });
      }
      setShowEvaluationForm(false);
      setEditingEvaluation(null);
      fetchCallDetails();
    } catch (error) {
      console.error('Erro ao salvar avaliação:', error);
      throw error;
    }
  };

  const handleEditEvaluation = (evaluation) => {
    setEditingEvaluation(evaluation);
    setShowEvaluationForm(true);
  };

  const getStatusBadge = (status) => {
    const styles = {
      open: 'bg-blue-100 text-blue-800',
      in_progress: 'bg-yellow-100 text-yellow-800',
      resolved: 'bg-green-100 text-green-800',
      closed: 'bg-gray-100 text-gray-800',
    };
    const labels = {
      open: 'Aberto',
      in_progress: 'Em Andamento',
      resolved: 'Resolvido',
      closed: 'Fechado',
    };
    return (
      <span className={`px-3 py-1 rounded-full text-sm font-medium ${styles[status] || styles.open}`}>
        {labels[status] || status}
      </span>
    );
  };

  const getPriorityBadge = (priority) => {
    const styles = {
      low: 'bg-gray-100 text-gray-800',
      medium: 'bg-blue-100 text-blue-800',
      high: 'bg-orange-100 text-orange-800',
      urgent: 'bg-red-100 text-red-800',
    };
    const labels = {
      low: 'Baixa',
      medium: 'Média',
      high: 'Alta',
      urgent: 'Urgente',
    };
    return (
      <span className={`px-3 py-1 rounded-full text-sm font-medium ${styles[priority] || styles.medium}`}>
        {labels[priority] || priority}
      </span>
    );
  };

  const getCategoryLabel = (category) => {
    const labels = {
      support: 'Suporte',
      sales: 'Vendas',
      complaint: 'Reclamação',
      question: 'Dúvida',
      cancellation: 'Cancelamento',
    };
    return labels[category] || category;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const canEvaluate = user && (user.role === 'supervisor' || user.role === 'admin');

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!call) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
        <AlertCircle className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">Chamada não encontrada</h3>
        <button
          onClick={() => navigate('/calls')}
          className="mt-4 text-blue-600 hover:text-blue-700"
        >
          Voltar para chamadas
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Cabeçalho */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate('/calls')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900"
        >
          <ArrowLeft className="w-5 h-5" />
          Voltar
        </button>
        {canEvaluate && !showEvaluationForm && call.evaluations.length === 0 && (
          <button
            onClick={() => setShowEvaluationForm(true)}
            className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            <Plus className="w-5 h-5" />
            Nova Avaliação
          </button>
        )}
      </div>

      {/* Informações da Chamada */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-start justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              Protocolo: {call.protocol}
            </h1>
            <div className="flex flex-wrap gap-3">
              {getStatusBadge(call.status)}
              {getPriorityBadge(call.priority)}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-gray-600">Cliente</label>
              <p className="text-gray-900 flex items-center gap-2 mt-1">
                <User className="w-4 h-4" />
                {call.customer_name}
              </p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-600">Operador</label>
              <p className="text-gray-900 flex items-center gap-2 mt-1">
                <User className="w-4 h-4" />
                {call.operator?.full_name || 'Não atribuído'}
              </p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-600">Categoria</label>
              <p className="text-gray-900 flex items-center gap-2 mt-1">
                <Tag className="w-4 h-4" />
                {getCategoryLabel(call.category)}
              </p>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-gray-600">Data de Criação</label>
              <p className="text-gray-900 flex items-center gap-2 mt-1">
                <Calendar className="w-4 h-4" />
                {formatDate(call.created_at)}
              </p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-600">Duração</label>
              <p className="text-gray-900 flex items-center gap-2 mt-1">
                <Clock className="w-4 h-4" />
                {call.duration_minutes ? `${call.duration_minutes} minutos` : 'Não registrada'}
              </p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-600">Telefone</label>
              <p className="text-gray-900 flex items-center gap-2 mt-1">
                <Phone className="w-4 h-4" />
                {call.customer_phone || 'Não informado'}
              </p>
            </div>
          </div>
        </div>

        <div className="mt-6 pt-6 border-t">
          <label className="text-sm font-medium text-gray-600">Assunto</label>
          <p className="text-gray-900 mt-2">{call.subject}</p>
        </div>

        {call.description && (
          <div className="mt-4">
            <label className="text-sm font-medium text-gray-600">Descrição</label>
            <p className="text-gray-900 mt-2 whitespace-pre-wrap">{call.description}</p>
          </div>
        )}

        {call.resolution && (
          <div className="mt-4">
            <label className="text-sm font-medium text-gray-600">Resolução</label>
            <p className="text-gray-900 mt-2 whitespace-pre-wrap">{call.resolution}</p>
          </div>
        )}
      </div>

      {/* Formulário de Avaliação */}
      {showEvaluationForm && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-6">
            {editingEvaluation ? 'Editar Avaliação' : 'Nova Avaliação'}
          </h2>
          <EvaluationForm
            callId={call.id}
            existingEvaluation={editingEvaluation}
            onSave={handleSaveEvaluation}
            onCancel={() => {
              setShowEvaluationForm(false);
              setEditingEvaluation(null);
            }}
          />
        </div>
      )}

      {/* Avaliações Existentes */}
      {call.evaluations && call.evaluations.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-xl font-bold text-gray-900">Avaliações</h2>
          {call.evaluations.map((evaluation) => (
            <div
              key={evaluation.id}
              className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-4">
                  <div className="text-4xl font-bold text-blue-600">
                    {evaluation.overall_score.toFixed(1)}
                  </div>
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-medium text-gray-900">
                        Avaliado por: {evaluation.evaluator?.full_name || 'Não identificado'}
                      </span>
                      {evaluation.is_exemplary && (
                        <span className="inline-flex items-center gap-1 px-2 py-1 bg-yellow-100 text-yellow-800 text-xs font-medium rounded">
                          <Award className="w-3 h-3" />
                          Exemplar
                        </span>
                      )}
                      {evaluation.requires_coaching && (
                        <span className="inline-flex items-center gap-1 px-2 py-1 bg-orange-100 text-orange-800 text-xs font-medium rounded">
                          <AlertCircle className="w-3 h-3" />
                          Requer Coaching
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-600">
                      {formatDate(evaluation.created_at)}
                    </p>
                  </div>
                </div>
                {canEvaluate && (
                  <button
                    onClick={() => handleEditEvaluation(evaluation)}
                    className="flex items-center gap-2 text-blue-600 hover:text-blue-700"
                  >
                    <Edit className="w-4 h-4" />
                    Editar
                  </button>
                )}
              </div>

              {/* Critérios */}
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
                {[
                  { label: 'Saudação', value: evaluation.greeting_score },
                  { label: 'Comunicação', value: evaluation.communication_score },
                  { label: 'Resolução', value: evaluation.problem_resolution_score },
                  { label: 'Empatia', value: evaluation.empathy_score },
                  { label: 'Procedimentos', value: evaluation.procedure_compliance_score },
                  { label: 'Encerramento', value: evaluation.closing_score },
                ].map((criterion, index) => (
                  <div key={index} className="flex items-center gap-2">
                    <Star className="w-4 h-4 text-yellow-400" fill="currentColor" />
                    <span className="text-sm text-gray-700">
                      {criterion.label}: <strong>{criterion.value}</strong>
                    </span>
                  </div>
                ))}
              </div>

              {/* Feedback */}
              <div className="space-y-4">
                {evaluation.positive_points && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2 flex items-center gap-2">
                      <CheckCircle className="w-4 h-4 text-green-600" />
                      Pontos Positivos
                    </h4>
                    <p className="text-gray-700 pl-6">{evaluation.positive_points}</p>
                  </div>
                )}
                {evaluation.improvement_points && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2 flex items-center gap-2">
                      <AlertCircle className="w-4 h-4 text-orange-600" />
                      Pontos de Melhoria
                    </h4>
                    <p className="text-gray-700 pl-6">{evaluation.improvement_points}</p>
                  </div>
                )}
                {evaluation.general_comments && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2 flex items-center gap-2">
                      <MessageSquare className="w-4 h-4 text-blue-600" />
                      Comentários Gerais
                    </h4>
                    <p className="text-gray-700 pl-6">{evaluation.general_comments}</p>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CallDetail;
