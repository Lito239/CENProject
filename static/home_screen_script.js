/* ------- VARIABLES ------- */
let transactionHistory = [];
let cards = [];
let goals=[];
let currentSelectedGoal =null;
let editingGoalIndex =null;
if (window.savedGoals){
    goals = window.savedGoals.map(function(goal){
        return{ id:goal.id, name:goal.goal_name, startDate: goal.start_date, endDate: goal.end_date, goalAmount: goal.goal_amount};
    });
}
var currentSortType = "";
var sortAscending = true;
var currentCardSortType ="";
var cardSortAscending =true;
var headerNames ={
    date: "Date",
    name: "Name",
    amount: "Amount",
    card: "Card"
};
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
/* ------- Add Goals ------- */
async function addGoal(){
    var goalName=document.getElementById("goalName").value;
    var startDate=document.getElementById("goalStartDate").value;
    var endDate=document.getElementById("goalEndDate").value;
    var goalAmount =document.getElementById("goalAmount").value;
    if(goalName ==="" || startDate ===""|| endDate===""||goalAmount===""){
        alert("Please complete every field!");
        return;
    }
    try{
        var url="/goals";
        var method ="POST";
        if (editingGoalIndex !=null){
            url="/goals/"+goals[editingGoalIndex].id;
            method="PUT";
        }
        var response = await fetch(url,{method:method, 
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                goalName: goalName, startDate:startDate, endDate: endDate, goalAmount:goalAmount
            })
        });
        var result =await response.json();
        if(!response.ok){
            alert(result.message);
            return;
         }
        var wasEditing=editingGoalIndex!=null;
        var editedIndex=editingGoalIndex;
        if(!wasEditing){
            goals.push(result.goal);
        }
        else{
            goals[editedIndex]=result.goal;
        }
        editingGoalIndex=null;
        renderGoalDropdown();
        if(wasEditing){
            document.getElementById("goalDropdown").value=editedIndex;
            currentSelectedGoal=result.goal;
            updateGoalProgress(currentSelectedGoal);
        }
        document.getElementById("goalName").value="";
        document.getElementById("goalStartDate").value="";
        document.getElementById("goalEndDate").value="";
        document.getElementById("goalAmount").value="";
        document.getElementById("goalMenu").style.display="none";
        document.getElementById("grayOut").style.display="none";
        console.log(goals);
    }
    catch(error){
        console.error(error);
        alert("The goal could not be saved.");
}
}
async function deleteGoal() {
    if(editingGoalIndex==null){
        alert("Please select and edit a goal first.");
        return;
    }
    var goal=goals[editingGoalIndex];
    var confirmed = confirm("Are you sure you want to delete this goal?");
    if(!confirmed){
        return;
    }
    try{
        var response =await fetch("/goals/" +goal.id, { method:"DELETE"});
    goals.splice(editingGoalIndex,1);
    editingGoalIndex=null;
    currentSelectedGoal=null;
    renderGoalDropdown();
    document.getElementById("goalProgressFill").style.width="0%";
    document.getElementById("goalProgressText").textContent= "No Goal Selected";
    document.getElementById("goalMenu").style.display ="none";
    document.getElementById("grayOut").style.display ="none";
    }
    catch(error){
        console.error(error);
        alert("The goal could not be deleted.");
    }
}
function renderGoalDropdown(){
    var renderGoalDropdown =document.getElementById("goalDropdown");
    renderGoalDropdown.innerHTML="";
    var defaultOption=document.createElement("option");
    defaultOption.textContent="Select Goal";
    defaultOption.disabled =true;
    defaultOption.selected =true;
    renderGoalDropdown.appendChild(defaultOption);
    goals.forEach(function(goal,i){
        var option=document.createElement("option");
        option.value=i;
        option.textContent= goal.name;
    renderGoalDropdown.appendChild(option);
    });
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
    if(currentSelectedGoal !=null){
        updateGoalProgress(currentSelectedGoal);
    }
}

function renderTransactionHistory() {
    var historyTable = document.getElementById("historyTable");
    historyTable.innerHTML = "";

    // show transactions from transactionHistory array in history table
    transactionHistory.forEach(function(transaction, i) {
        var row = document.createElement("tr");
        row.innerHTML = "<td>" + transaction.name + "</td><td>" + transaction.amount + "</td><td>" + transaction.card + "</td>" + "<td>" +  transaction.date + "</td>";

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

function sortTransactions(sortType){
    if (currentSortType === sortType){
        sortAscending = !sortAscending;
    }
    else{
        currentSortType = sortType;
        sortAscending = true;
    }
    transactionHistory.sort(function(a,b){
        var comparison = 0;

    if (sortType ==="date"){
    comparison = new Date(a.date) - new Date(b.date);
    }
    else if (sortType === "name"){
        comparison = a.name.localeCompare(b.name);
    }
    else if (sortType === "amount"){
        comparison =Number(a.amount) - Number(b.amount);
    }
    else if (sortType === "card"){
        comparison = a.card.localeCompare(b.card)
    }
    if(sortAscending){
        return comparison;
    }
    else{
        return -comparison;
    }
    });
    document.querySelectorAll(".sort-arrow").forEach(function(arrow){
        arrow.innerHTML ="";
    });
    var currentHeader = document.getElementById(sortType +"Header");
    var currentArrow = currentHeader.querySelector(".sort-arrow");
    if (sortAscending){
        currentArrow.textContent = "▲";
    }
    else{
        currentArrow.textContent = "▼";
    }
    renderTransactionHistory();
}

function sortCards(sortType){
    if (currentCardSortType === sortType){
        cardSortAscending = !cardSortAscending;
    }
    else{
        currentCardSortType = sortType;
        cardSortAscending = true;
    }
    cards.sort(function(a,b){
        var comparison =0;
        if(sortType ==="name"){
            comparison =a.name.localeCompare(b.name);
        }
        else if(sortType==="amount"){
            comparison =Number(a.balance)-Number(b.balance);
        }
        if(cardSortAscending){
            return comparison;
        }
        else{
            return -comparison;
        }
    });
    document.querySelectorAll(".card-sort-arrow").forEach(function(arrow){
        arrow.textContent="";
    });
    var currentHeader;
    if(sortType ==="name"){
        currentHeader =document.getElementById("cardNameHeader");
    }
    else{
        currentHeader=document.getElementById("cardAmountHeader");
    }
    var currentArrow=currentHeader.querySelector(".card-sort-arrow");
    if(cardSortAscending){
        currentArrow.textContent= "▲"
    }
    else{
        currentArrow.textContent= "▼"
    }
    renderCards();
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
    document.getElementById("goalMenu").style.display = "none";
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
document.getElementById("addGoalButton").addEventListener("click", function () {
    editingGoalIndex=null;
    document.getElementById("deleteGoalButton").style.display="none";
    document.getElementById("goalName").value="";
    document.getElementById("goalStartDate").value="";
    document.getElementById("goalEndDate").value="";
    document.getElementById("goalAmount").value="";
    document.getElementById("goalMenu").style.display = "block";
    document.getElementById("grayOut").style.display = "block";

});
document.getElementById("closeGoalWindow").addEventListener("click", function () {
    document.getElementById("goalMenu").style.display = "none";
    document.getElementById("grayOut").style.display = "none";
});
document.getElementById("goalDropdown").addEventListener("change", function(){
    currentSelectedGoal =goals[this.value];
    if(currentSelectedGoal){
        updateGoalProgress(currentSelectedGoal);
    }
});
document.getElementById("editGoalButton").addEventListener("click",function(){
    var goalDropDown=document.getElementById("goalDropdown");
    var selectedIndex=goalDropDown.value;
    if(selectedIndex===""){
        alert("Please select a goal first.");
        return;
    }
    document.getElementById("deleteGoalButton").style.display="block";
    editingGoalIndex=Number(selectedIndex);
    var selectedGoal =goals[editingGoalIndex];
    document.getElementById("goalName").value=selectedGoal.name;
    document.getElementById("goalStartDate").value=selectedGoal.startDate;
    document.getElementById("goalEndDate").value=selectedGoal.endDate;
    document.getElementById("goalAmount").value=selectedGoal.goalAmount;
    document.getElementById("goalMenu").style.display="block";
    document.getElementById("grayOut").style.display="block";
    
});
document.getElementById("deleteGoalButton").addEventListener("click", function(){
    deleteGoal();
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
function updateGoalProgress(goal){
    var moneySpent =0;
    transactionHistory.forEach(function(transaction){
        if( transaction.date>= goal.startDate && transaction.date<= goal.endDate)
        {
            moneySpent += Number(transaction.amount);
        }
    });
    var actualPercent =0;
    
    if(goal.goalAmount>0){
        actualPercent=(moneySpent/goal.goalAmount) *100;
    }
    var barPercent = actualPercent;
    if(barPercent>100){
        barPercent=100;
    }
    var progressFill = document.getElementById("goalProgressFill")
    if(actualPercent<75){
        progressFill.style.backgroundColor ="rgb(99,99,152)";
    }
    else if (actualPercent<100){
        progressFill.style.backgroundColor ="rgb(210,180,60)";
    }
    else{
        progressFill.style.backgroundColor ="rgb(168,74,74)";
    }
    progressFill.style.width = barPercent+ "%";
    document.getElementById("goalDateText").textContent= goal.startDate +" to " + goal.endDate;
    document.getElementById("goalProgressText").textContent="$"+moneySpent.toFixed(2)+ " / $" + Number(goal.goalAmount).toFixed(2);
    document.getElementById("goalPercentText").textContent= actualPercent.toFixed(1) +"%";
}
/* ------- EDIT USER INFO ------- */
function saveUserChanges() {
    document.getElementById("settingsMenu").style.display = "none";
    document.getElementById("grayOut").style.display = "none";
}

//Load saved data when the page opens
recalculateCardBalances();
renderTables();
renderGoalDropdown();