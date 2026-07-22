/* 
------- TO-DO -------
- Add an option to delete a transaction
- Add an option to sort/filter cards by differnt factors
*/

/* ------- VARIABLES ------- */
let transactionHistory = [];
let cards = [];

/* ------- ADD TRANSACTION ------- */
function addTransaction() {
    // stores typed values
    var transactionName = document.getElementById("transactionName").value;
    var amount = document.getElementById("amount").value;
    var card = document.getElementById("card").value;
    var date = document.getElementById("transactionDate").value;
    var filter = document.getElementById("transactionFilter").value;

    // required fields
    if (transactionName === "" || amount === "") {
        alert("Invalid transaction.");
        return;
    }

    // adds transaction to the history array
    transactionHistory.push({name: transactionName, amount: amount, card: card, date: date, filter: filter});

    // resets the fields in the "Add Transaction" section
    document.getElementById("transactionName").value = "";
    document.getElementById("amount").value = "";
    document.getElementById("card").value = "";

    recalculateCardBalances();
    renderTables();
}

/* ------- RECALCULATION ------- */
function recalculateCardBalances() {
    cards.forEach(function(card) {
        card.balance = 0; 
    });

    transactionHistory.forEach(function(transaction) {
        if (transaction.card === "") {
            return;
        }
        var cardExists = cards.find(function (card) {
            return card.name === transaction.card;
        });
        if (cardExists) {
            cardExists.balance += parseFloat(transaction.amount);
        }
        else {
            cards.push({name: transaction.card, balance: parseFloat(transaction.amount)});
        }
    });
}

/* ------- RENDER TABLES FROM ARRAYS ------- */
function renderTables() {
    renderTransactionHistory();
    renderCards();
    renderCardOptions();
}

function renderTransactionHistory() {
    var historyTable = document.getElementById("historyTable");
    historyTable.innerHTML = "";

    // show transactions from transactionHistory array in history table
    transactionHistory.forEach(function(transaction, i) {
        var row = document.createElement("tr");
        row.innerHTML = "<td>" +  transaction.name + "</td><td>" + transaction.amount + "</td><td>" + transaction.card + "</td>";

        row.addEventListener("click", function () {
            var menu = document.getElementById("historyMenu");
            document.getElementById("editTransactionName").value = transaction.name;
            document.getElementById("editTransactionAmount").value = transaction.amount;
            document.getElementById("editTransactionCard").value = transaction.card;
            document.getElementById("editTransactionDate").value = transaction.date;
            document.getElementById("editTransactionFilter").value = transaction.filter;

            menu.style.display = "block";
            document.getElementById("grayOut").style.display = "block";
            menu.editIndex = i;
        });
        historyTable.appendChild(row);
    });
}

function renderCards() {
    var cardManagement = document.getElementById("cards");
    cardManagement.innerHTML = "";

    // show cards in card management table
    cards.forEach(function(card, i) {
        var row = document.createElement("tr");
        row.innerHTML = "<td>" +  card.name + "</td><td>" + card.balance + "</td>";

        row.addEventListener("click", function () {
            var menu = document.getElementById("cardMenu");
            document.getElementById("editCardName").value = card.name;

            menu.style.display = "block";
            document.getElementById("grayOut").style.display = "block";
            menu.editIndex = i;
        });
        cardManagement.appendChild(row);
    });
}

function renderCardOptions(){
    var select = document.getElementById("expandButton");
    select.length = 1;
    cards.forEach(function(card) {
        var option = document.createElement("option");
        option.text = card.name;
        select.add(option);
    });
}

/* ------- EVENT LISTENERS ------- */
// allows to pick a card from a dropdown menu
document.getElementById("expandButton").addEventListener("change", function() {
    document.getElementById("card").value = this.value;
    this.selectedIndex = 0;
});

// clicking anywhere besides the edit section will close an edit section
document.getElementById("grayOut").addEventListener("click", function() {
    document.getElementById("historyMenu").style.display = "none";
    document.getElementById("cardMenu").style.display = "none";
    this.style.display = "none";
});

// closes window when a button is pressed
document.getElementById("closeWindow").addEventListener("click", function() {
    document.getElementById("historyMenu").style.display = "none";
    document.getElementById("grayOut").style.display = "none";
});

document.getElementById("closeCardWindow").addEventListener("click", function() {
    document.getElementById("cardMenu").style.display = "none";
    document.getElementById("grayOut").style.display = "none";
});

/* ------- EDITORS ------- */
function saveTransactionChanges(button) {
    var menu = document.getElementById("historyMenu");
    var transaction = transactionHistory[menu.editIndex];

    transaction.name = document.getElementById("editTransactionName").value;
    transaction.amount = document.getElementById("editTransactionAmount").value;
    transaction.card = document.getElementById("editTransactionCard").value;
    transaction.date = document.getElementById("editTransactionDate").value;
    transaction.filter = document.getElementById("editTransactionFilter").value;

    menu.style.display = "none";
    document.getElementById("grayOut").style.display = "none";
    
    recalculateCardBalances();
    renderTables();
}

function saveCardChanges(button) {
    var menu = document.getElementById("cardMenu");
    var card = cards[menu.editIndex];

    var oldName = card.name;
    var newName = document.getElementById("editCardName").value;

    transactionHistory.forEach(function(transaction) {
        if (transaction.card === oldName) {
            transaction.card = newName;
        }
    });

    card.name = newName;

    menu.style.display = "none";
    document.getElementById("grayOut").style.display = "none";
    
    recalculateCardBalances();
    renderTables();
}