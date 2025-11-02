import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Star, Search, Filter, Eye, Edit, Trash2, Award, AlertCircle, Calendar, User } from 'lucide-react';
import api from '../config/api';

const Evaluations = () => {
  const navigate = useNavigate();
  const [evaluations, setEvaluations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    search: '',
    requires_coaching: '',
    is_exemplary: '',
  });
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 10,
    total: 0,
    pages: 0,
  });

  useEffect(() => {
    fetchEvaluations();
  }, [filters, pagination.page]);

  const fetchEvaluations = async () => {
    try {
      setLoading(true);
      const params = {
        page: pagination.page,
        per_page: pagination.per_page,
        ...filters,
      };

      const response = await api.get('/evaluations', { params });
      setEvaluations(response.data.evaluations || []);
      setPagination(prev => ({
        ...prev,
        total: response.data.total || 0,
        pages: response.data.pages || 0,
      }));
    } catch (error) {
      console.error('Erro ao carregar avaliações:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Tem certeza que deseja excluir esta avaliação?')) {
      return;
    }

    try {
      await api.delete(`/evaluations/${id}`);
      fetchEvaluations();
    } catch (error) {
      console.error('Erro ao excluir avaliação:', error);
      alert('Erro ao excluir avaliação');
    }
  };

  const getScoreColor = (score) => {
    if (score >= 4.5) return 'text-green-600 bg-green-50';
    if (score >= 3.5) return 'text-blue-600 bg-blue-50';
    if (score >= 2.5) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
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

  return (
    <div className="space-y-6">
      {/* Cabeçalho */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Avaliações</h1>
        <p className="text-gray-600 mt-1">
          Visualize e gerencie as avaliações de qualidade das chamadas
        </p>
      </div>

      {/* Filtros */}
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Search className="w-4 h-4 inline mr-1" />
              Buscar
            </label>
            <input
              type="text"
              value={filters.search}
              onChange={(e) => setFilters({ ...filters, search: e.target.value })}
              placeholder="Protocolo, operador..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Filter className="w-4 h-4 inline mr-1" />
              Requer Coaching
            </label>
            <select
              value={filters.requires_coaching}
              onChange={(e) => setFilters({ ...filters, requires_coaching: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Todos</option>
              <option value="true">Sim</option>
              <option value="false">Não</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Award className="w-4 h-4 inline mr-1" />
              Exemplar
            </label>
            <select
              value={filters.is_exemplary}
              onChange={(e) => setFilters({ ...filters, is_exemplary: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Todos</option>
              <option value="true">Sim</option>
              <option value="false">Não</option>
            </select>
          </div>
        </div>
      </div>

      {/* Lista de avaliações */}
      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : evaluations.length === 0 ? (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
          <AlertCircle className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Nenhuma avaliação encontrada
          </h3>
          <p className="text-gray-600">
            Não há avaliações que correspondam aos filtros selecionados.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {evaluations.map((evaluation) => (
            <div
              key={evaluation.id}
              className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                {/* Informações principais */}
                <div className="flex-1 space-y-3">
                  <div className="flex items-start gap-4">
                    <div className={`px-4 py-2 rounded-lg font-bold text-2xl ${getScoreColor(evaluation.overall_score)}`}>
                      {evaluation.overall_score.toFixed(1)}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-semibold text-gray-900">
                          Protocolo: {evaluation.call?.protocol || 'N/A'}
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
                      
                      <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
                        <span className="flex items-center gap-1">
                          <User className="w-4 h-4" />
                          {evaluation.call?.operator?.full_name || 'Operador não identificado'}
                        </span>
                        <span className="flex items-center gap-1">
                          <Calendar className="w-4 h-4" />
                          {formatDate(evaluation.created_at)}
                        </span>
                      </div>

                      {/* Critérios em resumo */}
                      <div className="mt-3 grid grid-cols-2 md:grid-cols-3 gap-2 text-xs">
                        <div className="flex items-center gap-1">
                          <Star className="w-3 h-3 text-yellow-400" fill="currentColor" />
                          <span>Saudação: {evaluation.greeting_score}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <Star className="w-3 h-3 text-yellow-400" fill="currentColor" />
                          <span>Comunicação: {evaluation.communication_score}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <Star className="w-3 h-3 text-yellow-400" fill="currentColor" />
                          <span>Resolução: {evaluation.problem_resolution_score}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <Star className="w-3 h-3 text-yellow-400" fill="currentColor" />
                          <span>Empatia: {evaluation.empathy_score}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <Star className="w-3 h-3 text-yellow-400" fill="currentColor" />
                          <span>Procedimentos: {evaluation.procedure_compliance_score}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <Star className="w-3 h-3 text-yellow-400" fill="currentColor" />
                          <span>Encerramento: {evaluation.closing_score}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Ações */}
                <div className="flex md:flex-col gap-2">
                  <button
                    onClick={() => navigate(`/calls/${evaluation.call_id}`)}
                    className="flex items-center gap-2 px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                    title="Ver detalhes"
                  >
                    <Eye className="w-4 h-4" />
                    <span className="text-sm">Ver</span>
                  </button>
                  <button
                    onClick={() => navigate(`/evaluations/${evaluation.id}/edit`)}
                    className="flex items-center gap-2 px-4 py-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                    title="Editar"
                  >
                    <Edit className="w-4 h-4" />
                    <span className="text-sm">Editar</span>
                  </button>
                  <button
                    onClick={() => handleDelete(evaluation.id)}
                    className="flex items-center gap-2 px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    title="Excluir"
                  >
                    <Trash2 className="w-4 h-4" />
                    <span className="text-sm">Excluir</span>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Paginação */}
      {!loading && evaluations.length > 0 && (
        <div className="flex items-center justify-between bg-white px-6 py-4 rounded-lg shadow-sm border border-gray-200">
          <div className="text-sm text-gray-600">
            Mostrando {((pagination.page - 1) * pagination.per_page) + 1} a{' '}
            {Math.min(pagination.page * pagination.per_page, pagination.total)} de{' '}
            {pagination.total} avaliações
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setPagination(prev => ({ ...prev, page: prev.page - 1 }))}
              disabled={pagination.page === 1}
              className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              Anterior
            </button>
            <button
              onClick={() => setPagination(prev => ({ ...prev, page: prev.page + 1 }))}
              disabled={pagination.page >= pagination.pages}
              className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              Próxima
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Evaluations;
