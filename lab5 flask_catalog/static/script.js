function displayItems() {
    fetch('/items')
        .then(res => res.json())
        .then(data => {
            const tbody = document.querySelector('#itemsTable tbody');
            tbody.innerHTML = ''; // curățăm tabelul
            data.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.id}</td>
                    <td>${item.name}</td>
                    <td>${item.quantity}</td>
                    <td>${item.price}</td>
                `;
                tbody.appendChild(row);
            });
        });
}

function addItem() {
    const id = parseInt(document.getElementById('indexInput').value);
    const name = document.getElementById('nameInput').value;
    const quantity = parseInt(document.getElementById('quantityInput').value);
    const price = parseFloat(document.getElementById('priceInput').value);

    fetch('/items', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ id, name, quantity, price })
    }).then(() => displayItems());
}

function editItem() {
    const id = parseInt(document.getElementById('indexInput').value);
    const name = document.getElementById('nameInput').value;
    const quantity = parseInt(document.getElementById('quantityInput').value);
    const price = parseFloat(document.getElementById('priceInput').value);

    fetch(`/items/${id}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ name, quantity, price })
    }).then(() => displayItems());
}

function deleteItem() {
    const id = parseInt(document.getElementById('indexInput').value);
    fetch(`/items/${id}`, {
        method: 'DELETE'
    }).then(() => displayItems());
}

window.onload = displayItems;
