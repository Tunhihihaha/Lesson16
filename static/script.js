document.addEventListener('DOMContentLoaded', () => {
    const booksBody = document.getElementById('books-body');
    const searchInput = document.getElementById('search-input');
    const authorFilter = document.getElementById('author-filter');
    let allBooksData = [];

    function renderBooks(books) {
        booksBody.innerHTML = '';
        if (books.length === 0) {
            booksBody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: #e74c3c; font-weight: bold;">Không tìm thấy kết quả phù hợp.</td></tr>`;
            return;
        }

        books.forEach((book, index) => {
            const row = booksBody.insertRow();

            row.insertCell().textContent = index + 1; 

            row.insertCell().textContent = book.title; 

            row.insertCell().textContent = book.author; 

            row.insertCell().textContent = book.price.toFixed(2); 

            row.insertCell().textContent = `${book.rating} sao`;

            row.insertCell().textContent = book.stock_status;

            row.insertCell().textContent = book.quantity; 
        });
    }

    function populateAuthorFilter(authors) {
        authors.forEach(author => {
            const option = document.createElement('option');
            option.value = author;
            option.textContent = author;
            authorFilter.appendChild(option);
        });
    }

    async function fetchData() {
        try {
            const booksResponse = await fetch('/api/books'); 
            if (!booksResponse.ok) {
                throw new Error('Lỗi khi tải dữ liệu sách');
            }
            allBooksData = await booksResponse.json();
            
            const authorsResponse = await fetch('/api/authors');
            if (!authorsResponse.ok) {
                throw new Error('Lỗi khi tải danh sách tác giả');
            }
            const authors = await authorsResponse.json();
c
            renderBooks(allBooksData);
            populateAuthorFilter(authors); 

        } catch (error) {
            console.error('Lỗi tải dữ liệu:', error);
            booksBody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: #c0392b;">Không thể kết nối đến máy chủ hoặc tải dữ liệu.</td></tr>`;
        }
    }

    function filterAndSearchBooks() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        const selectedAuthor = authorFilter.value; 

        let filteredBooks = allBooksData.filter(book => {
            const matchesAuthor = !selectedAuthor || book.author === selectedAuthor;
            const matchesSearch = !searchTerm || 
                                  book.title.toLowerCase().includes(searchTerm) ||
                                  book.author.toLowerCase().includes(searchTerm);

            return matchesAuthor && matchesSearch;
        });

        renderBooks(filteredBooks);
    }

    searchInput.addEventListener('input', filterAndSearchBooks);
    authorFilter.addEventListener('change', filterAndSearchBooks); 

    fetchData();
});
