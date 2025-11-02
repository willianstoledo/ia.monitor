import { useState, useEffect } from 'react';
import { Star, Save, X, AlertCircle, CheckCircle } from 'lucide-react';

const EvaluationForm = ({ callId, existingEvaluation, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    greeting_score: 0,
    communication_score: 0,
    problem_resolution_score: 0,
    empathy_score: 0,
    procedure_compliance_score: 0,
    closing_score: 0,
    positive_points: '',
    improvement_points: '',
    general_comments: '',
    requires_coaching: false,
    is_exemplary: false,
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (existingEvaluation) {
      setFormData({
        greeting_score: existingEvaluation.greeting_score || 0,
        communication_score: existingEvaluation.communication_score || 0,
        problem_resolution_score: existingEvaluation.problem_resolution_score || 0,
        empathy_score: existingEvaluation.empathy_score || 0,
        procedure_compliance_score: existingEvaluation.procedure_compliance_score || 0,
        closing_score: existingEvaluation.closing_score || 0,
        positive_points: existingEvaluation.positive_points || '',
        improvement_points: existingEvaluation.improvement_points || '',
        general_comments: existingEvaluation.general_comments || '',
        requires_coaching: existingEvaluation.requires_coaching || false,
        is_exemplary: existingEvaluation.is_exemplary || false,
      });
    }
  }, [existingEvaluation]);

  const criteria = [
    { key: 'greeting_score', label: 'Saudação e Apresentação', description: 'Cumprimento adequado e identificação clara' },
    { key: 'communication_score', label: 'Clareza e Comunicação', description: 'Linguagem clara e objetiva' },
    { key: 'problem_resolution_score', label: 'Resolução do Problema', description: 'Efetividade na solução' },
    { key: 'empathy_score', label: 'Empatia e Cordialidade', description: 'Atendimento humanizado' },
    { key: 'procedure_compliance_score', label: 'Seguimento de Procedimentos', description: 'Conformidade com processos' },
    { key: 'closing_score', label: 'Encerramento Adequado', description: 'Finalização profissional' },
  ];

  const calculateOverallScore = () => {
    const scores = [
      formData.greeting_score,
      formData.communication_score,
      formData.problem_resolution_score,
      formData.empathy_score,
      formData.procedure_compliance_score,
      formData.closing_score,
    ];
    const validScores = scores.filter(score => score > 0);
    if (validScores.length === 0) return 0;
    return (validScores.reduce((sum, score) => sum + score, 0) / validScores.length).toFixed(2);
  };

  const validateForm = () => {
    const newErrors = {};

    // Validar que todos os critérios foram pontuados
    criteria.forEach(criterion => {
      if (formData[criterion.key] === 0) {
        newErrors[criterion.key] = 'Este critério precisa ser avaliado';
      }
    });

    // Validar campos de texto obrigatórios
    if (!formData.positive_points.trim()) {
      newErrors.positive_points = 'Descreva pelo menos um ponto positivo';
    }

    if (!formData.improvement_points.trim()) {
      newErrors.improvement_points = 'Descreva pelo menos um ponto de melhoria';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleScoreChange = (criterionKey, score) => {
    setFormData(prev => ({
      ...prev,
      [criterionKey]: score,
    }));
    // Limpar erro ao alterar
    if (errors[criterionKey]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[criterionKey];
        return newErrors;
      });
    }
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));
    // Limpar erro ao alterar
    if (errors[field]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    try {
      await onSave(formData);
    } catch (error) {
      console.error('Erro ao salvar avaliação:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const StarRating = ({ value, onChange, error }) => {
    const [hover, setHover] = useState(0);

    return (
      <div className="flex flex-col">
        <div className="flex gap-1">
          {[1, 2, 3, 4, 5].map((star) => (
            <button
              key={star}
              type="button"
              onClick={() => onChange(star)}
              onMouseEnter={() => setHover(star)}
              onMouseLeave={() => setHover(0)}
              className={`transition-all ${
                star <= (hover || value)
                  ? 'text-yellow-400 scale-110'
                  : 'text-gray-300'
              }`}
            >
              <Star
                className="w-8 h-8"
                fill={star <= (hover || value) ? 'currentColor' : 'none'}
              />
            </button>
          ))}
          {value > 0 && (
            <span className="ml-2 text-sm font-medium text-gray-700 self-center">
              {value}/5
            </span>
          )}
        </div>
        {error && (
          <span className="text-sm text-red-600 mt-1 flex items-center gap-1">
            <AlertCircle className="w-4 h-4" />
            {error}
          </span>
        )}
      </div>
    );
  };

  const overallScore = calculateOverallScore();

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Cabeçalho com nota geral */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg border border-blue-200">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Avaliação de Qualidade</h3>
            <p className="text-sm text-gray-600 mt-1">
              Avalie cada critério de 1 a 5 estrelas
            </p>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-indigo-600">{overallScore}</div>
            <div className="text-sm text-gray-600">Nota Geral</div>
          </div>
        </div>
      </div>

      {/* Critérios de avaliação */}
      <div className="space-y-6">
        <h4 className="text-md font-semibold text-gray-900 border-b pb-2">
          Critérios de Avaliação
        </h4>
        
        {criteria.map((criterion) => (
          <div key={criterion.key} className="bg-white p-4 rounded-lg border border-gray-200">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
              <div className="flex-1">
                <h5 className="font-medium text-gray-900">{criterion.label}</h5>
                <p className="text-sm text-gray-600 mt-1">{criterion.description}</p>
              </div>
              <div className="md:w-64">
                <StarRating
                  value={formData[criterion.key]}
                  onChange={(score) => handleScoreChange(criterion.key, score)}
                  error={errors[criterion.key]}
                />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Campos de texto */}
      <div className="space-y-4">
        <h4 className="text-md font-semibold text-gray-900 border-b pb-2">
          Feedback Detalhado
        </h4>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Pontos Positivos *
          </label>
          <textarea
            value={formData.positive_points}
            onChange={(e) => handleInputChange('positive_points', e.target.value)}
            rows={3}
            className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
              errors.positive_points ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="Descreva os aspectos positivos do atendimento..."
          />
          {errors.positive_points && (
            <span className="text-sm text-red-600 mt-1 flex items-center gap-1">
              <AlertCircle className="w-4 h-4" />
              {errors.positive_points}
            </span>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Pontos de Melhoria *
          </label>
          <textarea
            value={formData.improvement_points}
            onChange={(e) => handleInputChange('improvement_points', e.target.value)}
            rows={3}
            className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
              errors.improvement_points ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="Descreva os pontos que podem ser melhorados..."
          />
          {errors.improvement_points && (
            <span className="text-sm text-red-600 mt-1 flex items-center gap-1">
              <AlertCircle className="w-4 h-4" />
              {errors.improvement_points}
            </span>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Comentários Gerais
          </label>
          <textarea
            value={formData.general_comments}
            onChange={(e) => handleInputChange('general_comments', e.target.value)}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Observações adicionais sobre o atendimento..."
          />
        </div>
      </div>

      {/* Checkboxes */}
      <div className="space-y-3">
        <h4 className="text-md font-semibold text-gray-900 border-b pb-2">
          Classificação Adicional
        </h4>

        <label className="flex items-start gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={formData.requires_coaching}
            onChange={(e) => handleInputChange('requires_coaching', e.target.checked)}
            className="mt-1 w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <div>
            <span className="font-medium text-gray-900">Requer Coaching</span>
            <p className="text-sm text-gray-600">
              Marque se o operador precisa de treinamento adicional
            </p>
          </div>
        </label>

        <label className="flex items-start gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={formData.is_exemplary}
            onChange={(e) => handleInputChange('is_exemplary', e.target.checked)}
            className="mt-1 w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <div>
            <span className="font-medium text-gray-900">Atendimento Exemplar</span>
            <p className="text-sm text-gray-600">
              Marque se este atendimento pode servir como exemplo para a equipe
            </p>
          </div>
        </label>
      </div>

      {/* Botões de ação */}
      <div className="flex gap-3 pt-4 border-t">
        <button
          type="submit"
          disabled={isSubmitting}
          className="flex-1 bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-colors"
        >
          {isSubmitting ? (
            <>
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Salvando...
            </>
          ) : (
            <>
              <Save className="w-5 h-5" />
              Salvar Avaliação
            </>
          )}
        </button>
        
        <button
          type="button"
          onClick={onCancel}
          disabled={isSubmitting}
          className="px-6 py-3 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 transition-colors"
        >
          <X className="w-5 h-5" />
          Cancelar
        </button>
      </div>
    </form>
  );
};

export default EvaluationForm;
