from flask import Flask, request, jsonify

app = Flask(__name__)

#Exercício 1: Calculadora
@app.route('/api/calculadora', methods=['GET'])
def calculadora():
    #Obter os números e a operação da URL
    num1 = float(request.args.get('num1'))
    num2 = float(request.args.get('num2'))
    operacao = request.args.get('operacao')

    if(operacao == 'soma'):
        resultado = num1 + num2
    elif(operacao == 'subtracao'):
        resultado = num1 - num2
    elif(operacao == 'multiplicacao'):
        resultado = num1 * num2
    elif(operacao == 'divisao'):
        if(num2 == 0):
            return jsonify({'erro': 'Divisão por 0 não é permitida.'}), 400
        resultado = num1 / num2
    else:
        return jsonify({'erro': 'Operação Inválida!'})
    
    return jsonify({'num1': num1, 'num2': num2, 'operacao': operacao, 'resultado': resultado}), 200

if __name__ == '__main__':
    app.run(debug=True)