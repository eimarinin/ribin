document.getElementById('addBookForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const title = document.getElementById('title').value;
    const author = document.getElementById('author').value;

    fetch('/addBook', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: title, author: author }),
    })
        .then(response => response.json())
        .then(data => {
            alert('Book added! ID: ' + data.id);
            document.getElementById('title').value = '';
            document.getElementById('author').value = '';
        })
        .catch(error => {
            console.error('Error adding book:', error);
            alert('Error adding book');
        });
});

function fetchBooks() {
    fetch('/listBooks')
        .then(response => response.json())
        .then(data => {
            const list = document.getElementById('bookList');
            list.innerHTML = '';
            data.books.forEach(book => {
                const li = document.createElement('li');
                li.textContent = `${book.title} by ${book.author}`;
                list.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Error fetching books:', error);
        });
}

function getBookById() {
    const id = document.getElementById('bookId').value;
    fetch(`/getBook?id=${id}`)
        .then(response => response.json())
        .then(data => {
            const details = document.getElementById('bookDetails');
            if (data.book) {
                details.innerHTML = `<h3>${data.book.title}</h3><p>Author: ${data.book.author}</p>`;
            } else {
                details.innerHTML = 'Book not found.';
            }
        })
        .catch(error => {
            console.error('Error fetching book:', error);
        });
}
