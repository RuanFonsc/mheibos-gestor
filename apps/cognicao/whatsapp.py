from apps.aprendizado.models import ConversaAprendizado

from .models import ConversaCognitiva, MensagemCognitiva


def espelhar_mensagem_whatsapp(conversa_aprendizado: ConversaAprendizado) -> ConversaCognitiva:
    """Espelha a mensagem recebida no contexto cognitivo sem disparar resposta."""
    conversa, _ = ConversaCognitiva.objects.get_or_create(
        origem="WHATSAPP",
        referencia_externa=f"{conversa_aprendizado.origem}:{conversa_aprendizado.instancia}:{conversa_aprendizado.contato_id}",
        defaults={"titulo": conversa_aprendizado.nome_contato or conversa_aprendizado.telefone},
    )
    mensagem = conversa_aprendizado.mensagens.order_by("-enviada_em", "-id").first()
    if mensagem and mensagem.texto:
        MensagemCognitiva.objects.get_or_create(
            conversa=conversa,
            papel="WHATSAPP",
            texto=mensagem.texto,
            defaults={"metadados": {"mensagem_id": mensagem.mensagem_id, "contato": conversa_aprendizado.contato_id}},
        )
    return conversa
