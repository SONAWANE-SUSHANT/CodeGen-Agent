function calculate(num1, num2, operator) {
    switch (operator) {
        case '+':
            return num1 + num2;
        case '-':
            return num1 - num2;
        case '*':
            return num1 * num2;
        case '/':
            if (num2 !== 0) {
                return num1 / num2;
            } else {
                return 'Error: Division by zero';
            }
        default:
            return 'Error: Invalid operator';
    }
}

let currentNumber = '';
let previousNumber = '';
let currentOperator = '';

document.getElementById('number-0').addEventListener('click', function() {
    currentNumber += '0';
    document.getElementById('display').value = currentNumber;
});

document.getElementById('number-1').addEventListener('click', function() {
    currentNumber += '1';
    document.getElementById('display').value = currentNumber;
});

document.getElementById('number-2').addEventListener('click', function() {
    currentNumber += '2';
    document.getElementById('display').value = currentNumber;
});

document.getElementById('number-3').addEventListener('click', function() {
    currentNumber += '3';
    document.getElementById('display').value = currentNumber;
});

document.getElementById('number-4').addEventListener('click', function() {
    currentNumber += '4';
    document.getElementById('display').value = currentNumber;
});

document.getElementById('number-5').addEventListener('click', function() {
    currentNumber += '5';
    document.getElementById('display').value = currentNumber;
});

document.getElementById('number-6').addEventListener('click', function() {
    currentNumber += '6';
    document.getElementById('display').value = currentNumber;
});

document.getElementById('number-7').addEventListener('click', function() {
    currentNumber += '7';
    document.getElementById('display').value = currentNumber;
});

document.getElementById('number-8').addEventListener('click', function() {
    currentNumber += '8';
    document.getElementById('display').value = currentNumber;
});

document.getElementById('number-9').addEventListener('click', function() {
    currentNumber += '9';
    document.getElementById('display').value = currentNumber;
});

document.getElementById('add').addEventListener('click', function() {
    previousNumber = currentNumber;
    currentNumber = '';
    currentOperator = '+';
});

document.getElementById('subtract').addEventListener('click', function() {
    previousNumber = currentNumber;
    currentNumber = '';
    currentOperator = '-';
});

document.getElementById('multiply').addEventListener('click', function() {
    previousNumber = currentNumber;
    currentNumber = '';
    currentOperator = '*';
});

document.getElementById('divide').addEventListener('click', function() {
    previousNumber = currentNumber;
    currentNumber = '';
    currentOperator = '/';
});

document.getElementById('equals').addEventListener('click', function() {
    let result = calculate(parseFloat(previousNumber), parseFloat(currentNumber), currentOperator);
    document.getElementById('display').value = result;
    previousNumber = '';
    currentNumber = result.toString();
});

document.getElementById('clear').addEventListener('click', function() {
    currentNumber = '';
    previousNumber = '';
    currentOperator = '';
    document.getElementById('display').value = '';
});