/* ------- VARIABLES ------- */
let transactionHistory = [];
let cards = [];

if (Array.isArray(window.savedTransactions)){
    transactionHistory = window.savedTransactions.map(function(transaction){
        return {
            id: transaction.id,
            name: transaction.transaction_name,
            amount: transaction.amount,
            card: transaction.card_name || "",
            date: transaction.transaction_date,
            filter: transaction.category
        };
    });
}

/* ------- ADD TRANSACTION ------- */
async function addTransaction() {
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
    try{
        var response = await fetch("/transactions", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                transactionName: transactionName, 
                amount: amount,
                card: card,
                transactionDate: date,
                category: filter
            })
        });
        var result = await response.json();
        if (!response.ok){
            alert(result.message);
            return;
        }
        transactionHistory.push(result.transaction);
            // resets the fields in the "Add Transaction" section
        document.getElementById("transactionName").value = "";
        document.getElementById("amount").value = "";
        document.getElementById("card").value = "";
        document.getElementById("transactionDate").value = "";
        document.getElementById("transactionFilter").value = "";
        recalculateCardBalances();
        renderTables();

    }
    catch(error){
        console.error(error);
        alert("The transaction could not be saved.");
    }
}

/* ------- DELETE TRANSACTION ------- */
async function deleteTransaction(){
    var menu = document.getElementById("historyMenu");
    var transactionIndex = menu.editIndex;
    var transaction = transactionHistory[transactionIndex];

    var confirmed = confirm("Are you sure you want to delete this transaction?");
    if(!confirmed){
        return;
    }

    try{
        var response = await fetch("/transactions/" + transaction.id, {
            method: "DELETE"
        });
        var result = await response.json();
        if(!response.ok){
            alert(result.message);
            return;
        }
        transactionHistory.splice(transactionIndex, 1);
        cards =[];
        recalculateCardBalances();
        renderTables();
    }
    catch(error){
        console.error(error);
        alert("Failed to delete transaction.");
    }

    document.getElementById("historyMenu").style.display = "none";
    document.getElementById("grayOut").style.display = "none";
}

/* ------- DELETE CARD ------- */
async function deleteCard() {

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
    document.getElementById("settingsMenu").style.display = "none";
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

// settings
document.getElementById("settingsButton").addEventListener("click", function() {
    document.getElementById("settingsMenu").style.display = "block";
    document.getElementById("grayOut").style.display = "block";
});

document.getElementById("closeSettingsWindow").addEventListener("click", function() {
    document.getElementById("settingsMenu").style.display = "none";
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

/* ------- EDIT USER INFO ------- */
function saveUserChanges() {
    document.getElementById("settingsMenu").style.display = "none";
    document.getElementById("grayOut").style.display = "none";
}

//Load saved data when the page opens
recalculateCardBalances();
renderTables();
