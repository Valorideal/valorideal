from flask import Flask, request, send_file
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

@app.route("/")
def index():
    return "API de gráfico ativa. Use /grafico com POST para enviar dados."

@app.route("/grafico", methods=["POST"])
def gerar_grafico():
    data = request.json
    baixo = data.get("percentual_baixo", 20)
    medio = data.get("percentual_medio", 30)
    alto = data.get("percentual_alto", 50)
    valor_ideal = data.get("valor_ideal_formatado", "R$ 1.400.000,00")
    valor_m2 = data.get("valor_m2", "R$ 8.500,00 por m²")
    qtd_imoveis = data.get("quantidade_imoveis", 27)

    fig, ax = plt.subplots(figsize=(8, 4), subplot_kw={'projection': 'polar'})
    ax.set_theta_offset(3.14159)
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 10)
    ax.axis('off')

    total = baixo + medio + alto
    percentuais = [baixo, medio, alto]
    cores = ["green", "yellow", "red"]
    start_angle = 0

    for p, cor in zip(percentuais, cores):
        raio = 10
        angulo = (p / total) * 3.14159
        ax.barh(raio / 2, angulo, left=start_angle, height=raio, color=cor)
        start_angle += angulo

    angulos = [baixo / 2, baixo + medio / 2, baixo + medio + alto / 2]
    angulos = [(a / total) * 3.14159 for a in angulos]
    labels = [f"{int(baixo)}%", f"{int(medio)}%", f"{int(alto)}%"]
    for ang, label in zip(angulos, labels):
        ax.text(ang, 10.5, label, ha='center', va='center', fontsize=12, fontweight='bold')

    plt.text(0, 1, "Valor Ideal", ha='center', va='center', fontsize=12, color='gray')
    plt.text(0, 0.3, valor_ideal, ha='center', va='center', fontsize=16, fontweight='bold')
    plt.text(0, -0.3, valor_m2, ha='center', va='center', fontsize=10, color='gray')
    plt.figtext(0.5, 0.01, f"Com base em {qtd_imoveis} imóveis avaliados na região.",
                ha='center', fontsize=9, bbox={"facecolor": "#eee", "pad": 6, "edgecolor": "none"})

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    return send_file(buf, mimetype="image/png")
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

