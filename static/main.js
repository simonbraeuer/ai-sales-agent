const chat = document.getElementById("chat");
const input = document.getElementById("query");
const send = document.getElementById("send");
const session_token = document.getElementById("session_token").value;

let currentOffers = [];
let currentSortField = null;
let currentSortOrder = 'desc';

send.onclick = async () => {
    const query = input.value.trim();
    if (!query) return;
    appendMessage("user", query);
    input.value = "";

    try {
        const response = await fetch("/api/query", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({query, session_token})
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();

        appendMessage("agent", data.message);

        if (data.done && data.offers.length > 0) {
            currentOffers = data.offers;
            appendOffers(data.offers);
        } else if (data.done && data.offers.length === 0) {
            appendMessage("agent", "No offers found matching your criteria. Try adjusting your search.");
        }
    } catch (error) {
        appendMessage("agent", `Error: ${error.message}. Please try again.`);
        console.error("Error querying agent:", error);
    }
};

// Allow Enter key to send message
input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        send.click();
    }
});

function appendMessage(sender, message) {
    const div = document.createElement("div");
    div.className = `message ${sender}`;
    div.textContent = message;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function appendOffers(offers) {
    // Create sort controls
    const sortControls = document.createElement("div");
    sortControls.className = "sort-controls";
    sortControls.innerHTML = `
        <label>Sort by:</label>
        <select id="sortField">
            <option value="">Default (Discount & Rating)</option>
            <option value="price">Price</option>
            <option value="discount">Discount</option>
            <option value="rating">Rating</option>
            <option value="title">Title</option>
        </select>
        <select id="sortOrder">
            <option value="desc">High to Low</option>
            <option value="asc">Low to High</option>
        </select>
    `;
    
    // Create table
    const table = document.createElement("table");
    table.id = "offersTable";
    
    const header = table.insertRow();
    const headers = [
        {text: "Title", field: "title"},
        {text: "Category", field: "category"},
        {text: "Price", field: "price"},
        {text: "Discount", field: "discount"},
        {text: "Rating", field: "rating"}
    ];
    
    headers.forEach(h => {
        const th = document.createElement("th");
        th.textContent = h.text;
        th.dataset.field = h.field;
        th.onclick = () => sortTable(h.field);
        header.appendChild(th);
    });

    renderTableRows(table, offers);

    chat.appendChild(sortControls);
    chat.appendChild(table);
    chat.scrollTop = chat.scrollHeight;

    // Add event listeners to sort controls
    document.getElementById("sortField").addEventListener("change", (e) => {
        const field = e.target.value;
        const order = document.getElementById("sortOrder").value;
        if (field) {
            sortAndRenderOffers(field, order);
        } else {
            // Default sort
            const sorted = [...currentOffers].sort((a, b) => 
                (b.discount - a.discount) || (b.rating - a.rating)
            );
            renderTableRows(table, sorted);
        }
    });

    document.getElementById("sortOrder").addEventListener("change", (e) => {
        const field = document.getElementById("sortField").value;
        const order = e.target.value;
        if (field) {
            sortAndRenderOffers(field, order);
        }
    });
}

function renderTableRows(table, offers) {
    // Remove existing rows except header
    while (table.rows.length > 1) {
        table.deleteRow(1);
    }

    offers.forEach(offer => {
        const row = table.insertRow();
        
        const title = row.insertCell();
        title.textContent = offer.title;

        const category = row.insertCell();
        category.textContent = offer.category;
        category.style.textTransform = "capitalize";

        const price = row.insertCell();
        price.textContent = `$${offer.price.toFixed(2)}`;
        price.className = "price";

        const discount = row.insertCell();
        discount.textContent = `${offer.discount}%`;
        discount.className = "discount";

        const rating = row.insertCell();
        rating.textContent = offer.rating.toFixed(1);
        rating.className = "rating";
    });
}

function sortTable(field) {
    // Toggle sort order if clicking same field
    if (currentSortField === field) {
        currentSortOrder = currentSortOrder === 'asc' ? 'desc' : 'asc';
    } else {
        currentSortField = field;
        currentSortOrder = 'desc';
    }

    sortAndRenderOffers(field, currentSortOrder);
    
    // Update UI to show sorted column
    const table = document.getElementById("offersTable");
    const headers = table.querySelectorAll("th");
    headers.forEach(th => {
        th.classList.remove("sorted", "asc", "desc");
        if (th.dataset.field === field) {
            th.classList.add("sorted", currentSortOrder);
        }
    });

    // Update dropdowns
    const sortFieldSelect = document.getElementById("sortField");
    const sortOrderSelect = document.getElementById("sortOrder");
    if (sortFieldSelect) sortFieldSelect.value = field;
    if (sortOrderSelect) sortOrderSelect.value = currentSortOrder;
}

function sortAndRenderOffers(field, order) {
    const table = document.getElementById("offersTable");
    if (!table) return;

    const sorted = [...currentOffers].sort((a, b) => {
        let aVal = a[field];
        let bVal = b[field];

        // String comparison for title and category
        if (typeof aVal === 'string') {
            aVal = aVal.toLowerCase();
            bVal = bVal.toLowerCase();
            return order === 'asc' ? 
                aVal.localeCompare(bVal) : 
                bVal.localeCompare(aVal);
        }

        // Numeric comparison
        return order === 'asc' ? aVal - bVal : bVal - aVal;
    });

    renderTableRows(table, sorted);
}
