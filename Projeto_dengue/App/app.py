from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
pacientes = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_patient', methods=['POST'])
def add_patient():
    nome = request.form['nome']
    idade = request.form['idade']
    regiao = request.form['regiao']
    sintomas = request.form.getlist('sintomas')

    paciente = {
        'nome': nome,
        'idade': idade,
        'regiao': regiao,
        'sintomas': sintomas,
        'diagnostico': verificar_dengue(sintomas)
    }

    pacientes.append(paciente)
    return redirect(url_for('result', paciente_id=len(pacientes) - 1))

def verificar_dengue(sintomas):
    sintomas_dengue = ['febre', 'dor de cabeça', 'dor atrás dos olhos', 'manchas vermelhas', 'dores nas articulações', 'dores musculares', 'náusea', 'vômito']
    sintomas_comuns = set(sintomas).intersection(set(sintomas_dengue))
    if len(sintomas_comuns) >= 3:
        return "Positivo para dengue, para amenizar sintomas como dor e febre, pode-se usar medicamentos como paracetamol e dipirona. Mantenha-se hidratado(a)."
    else:
        return "Negativo para dengue, se cuide."

@app.route('/result')
def result():
    paciente_id = int(request.args.get('paciente_id'))
    paciente = pacientes[paciente_id]
    
    regiao_dict = {}
    total_dengue = 0

    for p in pacientes:
        regiao = p['regiao']
        if p['diagnostico'].startswith("Positivo"):
            total_dengue += 1
            if regiao in regiao_dict:
                regiao_dict[regiao] += 1
            else:
                regiao_dict[regiao] = 1

    return render_template('result.html', paciente=paciente, regiao_dict=regiao_dict, total_dengue=total_dengue)

@app.route('/analise')
def analise():
    regiao_dict = {}
    total_dengue = 0

    for p in pacientes:
        regiao = p['regiao']
        if p['diagnostico'].startswith("Positivo"):
            total_dengue += 1
            if regiao in regiao_dict:
                regiao_dict[regiao] += 1
            else:
                regiao_dict[regiao] = 1

    return render_template('analise.html', regiao_dict=regiao_dict, total_dengue=total_dengue)

if __name__ == '__main__':
    app.run(debug=True)
