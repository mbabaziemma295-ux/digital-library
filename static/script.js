// Image Assets
const imgNovel = "https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&q=80&w=400";
const imgMotivation = "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?auto=format&fit=crop&q=80&w=400";
const imgScience = "https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&q=80&w=400";
const imgEnglish = "https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&q=80&w=400";

// CLEANED BOOK DATABASE
const books = [
    // --- NOVELS ---
    {title:"1984", author:"George Orwell", year:"1949", category:"Novel", continent:"Europe", desc:"A dystopian novel about totalitarianism.", img: imgNovel, readUrl:"https://www.gutenberg.org/files/7370/7370-h/7370-h.htm"},
    {title:"Pride and Prejudice", author:"Jane Austen", year:"1813", category:"Novel", continent:"Europe", desc:"A romantic novel of manners.", img: imgNovel, readUrl:"https://www.gutenberg.org/files/1342/1342-h/1342-h.htm"},
    {title:"The Adventures of Sherlock Holmes", author:"Arthur Conan Doyle", year:"1892", category:"Novel", continent:"Europe", desc:"Stories of the famous detective.", img: imgNovel, readUrl:"https://www.gutenberg.org/files/1661/1661-h/1661-h.htm"},
    {title:"Moby Dick", author:"Herman Melville", year:"1851", category:"Novel", continent:"North America", desc:"The obsessive quest of Captain Ahab.", img: imgNovel, readUrl:"https://www.gutenberg.org/files/2701/2701-h/2701-h.htm"},
    {title:"Alice's Adventures in Wonderland", author:"Lewis Carroll", year:"1865", category:"Novel", continent:"Europe", desc:"A girl falls into a fantasy world.", img: imgNovel, readUrl:"https://www.gutenberg.org/files/11/11-h/11-h.htm"},
    
    // --- MOTIVATION ---
    {title:"As a Man Thinketh", author:"James Allen", year:"1903", category:"Motivation", continent:"Europe", desc:"On the power of thought.", img: imgMotivation, readUrl:"https://www.gutenberg.org/files/5658/5658-h/5658-h.htm"},
    {title:"Think and Grow Rich", author:"Napoleon Hill", year:"1937", category:"Motivation", continent:"North America", desc:"Classic self-help on success.", img: imgMotivation, readUrl:"https://www.gutenberg.org/files/53424/53424-h/53424-h.htm"},
    {title:"Meditations", author:"Marcus Aurelius", year:"180", category:"Motivation", continent:"Europe", desc:"Personal writings of Roman Emperor.", img: imgMotivation, readUrl:"https://www.gutenberg.org/files/2680/2680-h/2680-h.htm"},
    {title:"Self-Reliance", author:"Ralph Waldo Emerson", year:"1841", category:"Motivation", continent:"North America", desc:"Trust your intuition.", img: imgMotivation, readUrl:"https://www.gutenberg.org/files/16643/16643-h/16643-h.htm"},

    // --- SCIENCE ---
    {title:"Flatland", author:"Edwin A. Abbott", year:"1884", category:"Science", continent:"Europe", desc:"A romance of many dimensions.", img: imgScience, readUrl:"https://www.gutenberg.org/files/201/201-h/201-h.htm"},
    {title:"On the Origin of Species", author:"Charles Darwin", year:"1859", category:"Science", continent:"Europe", desc:"Theory of evolution.", img: imgScience, readUrl:"https://www.gutenberg.org/files/2009/2009-h/2009-h.htm"},
    {title:"The Chemical History of a Candle", author:"Michael Faraday", year:"1861", category:"Science", continent:"Europe", desc:"Lectures on chemistry and physics of flames.", img: imgScience, readUrl:"https://www.gutenberg.org/files/22644/22644-h/22644-h.htm"},
    {title:"Six Easy Pieces", author:"Richard Feynman", year:"1994", category:"Science", continent:"North America", desc:"Essentials of physics explained.", img: imgScience, readUrl:"https://archive.org/details/SixEasyPiecesFeynman"},

    // --- LEARNING ENGLISH ---
    {title:"English Grammar", author:"Gould Brown", year:"1851", category:"Learning English", continent:"North America", desc:"Comprehensive guide to English grammar.", img: imgEnglish, readUrl:"https://www.gutenberg.org/files/38984/38984-h/38984-h.htm"},
    {title:"Word Power Made Easy", author:"Norman Lewis", year:"1949", category:"Learning English", continent:"Asia", desc:"Vocabulary building system.", img: imgEnglish, readUrl:"https://archive.org/details/WordPowerMadeEasyNormanLewis"},
    {title:"The Elements of Style", author:"William Strunk Jr.", year:"1918", category:"Learning English", continent:"North America", desc:"Classic writing style guide.", img: imgEnglish, readUrl:"https://www.gutenberg.org/files/37134/37134-h/37134-h.htm"},
    {title:"Practical English", author:"T. O. Cone", year:"1904", category:"Learning English", continent:"North America", desc:"Lessons in speaking and writing English.", img: imgEnglish, readUrl:"https://www.gutenberg.org/files/18047/18047-h/18047-h.htm"}
];

// State variables
let currentMode = 'genre'; // 'genre' or 'world'
let currentFilterValue = 'All';
const container = document.getElementById('booksContainer');
const subTabsContainer = document.getElementById('subTabsContainer');
const searchInput = document.getElementById('searchInput');

// --- MAIN TAB LOGIC ---
function switchMainTab(mode, value, btnElement) {
    currentMode = mode;
    currentFilterValue = value;

    // Update Main Button Styling
    const buttons = document.querySelectorAll('.main-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    if(btnElement) btnElement.classList.add('active'); // Check if element exists (for initial load)

    // Clear sub-tabs
    subTabsContainer.innerHTML = '';

    // Logic based on Mode
    if (mode === 'world') {
        renderSubTabs('continent');
        applyFilters();
    } else {
        applyFilters();
    }
}

// --- SUB TAB LOGIC ---
function renderSubTabs(type) {
    let items = [];
    if (type === 'continent') {
        items = ['All', 'Africa', 'Asia', 'Europe', 'North America', 'South America', 'Australia', 'Antarctica'];
    }

    items.forEach(item => {
        const btn = document.createElement('button');
        btn.className = 'sub-btn';
        if (item === 'All') btn.classList.add('active');
        btn.innerText = item;
        btn.onclick = function() {
            document.querySelectorAll('.sub-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentFilterValue = item;
            applyFilters();
        };
        subTabsContainer.appendChild(btn);
    });
}

// --- APPLY FILTERS ---
function applyFilters() {
    let result = books;

    if (currentMode === 'genre') {
        if (currentFilterValue !== 'All') {
            result = result.filter(book => book.category === currentFilterValue);
        }
    } else if (currentMode === 'world') {
        if (currentFilterValue !== 'All') {
            result = result.filter(book => book.continent === currentFilterValue);
        }
    }

    renderBooks(result, currentMode);
}

// Render Books Function
function renderBooks(booksToRender, mode) {
    container.innerHTML = "";
    if(booksToRender.length === 0) {
        container.innerHTML = "<p style='text-align:center; width:100%; color:#666; grid-column: 1/-1; font-size:1.2rem;'>No books found in this folder.</p>";
        return;
    }

    booksToRender.forEach(book => {
        const card = document.createElement('div');
        card.classList.add('book-card');
        
        let continentBadgeHTML = '';
        if (mode === 'world') {
            continentBadgeHTML = `<span class="continent-badge" style="display:block">${book.continent}</span>`;
        }

        card.innerHTML = `
            ${continentBadgeHTML}
            <span class="category-badge">${book.category}</span>
            <img src="${book.img}" alt="${book.title}">
            <div class="book-details">
                <div>
                    <h3>${book.title}</h3>
                    <div class="book-info">
                        <p><strong>Author:</strong> ${book.author}</p>
                        <p><strong>Year:</strong> ${book.year}</p>
                    </div>
                </div>
                <button class="view-btn" onclick='openModal(${JSON.stringify(book)})'>View Details</button>
            </div>
        `;
        container.appendChild(card);
    });
}

// Search Logic
searchInput.addEventListener('keyup', (e) => {
    const searchString = e.target.value.toLowerCase();
    
    let baseList = books;
    if (currentMode === 'genre' && currentFilterValue !== 'All') {
        baseList = baseList.filter(book => book.category === currentFilterValue);
    } else if (currentMode === 'world' && currentFilterValue !== 'All') {
        baseList = baseList.filter(book => book.continent === currentFilterValue);
    }

    const filteredBooks = baseList.filter((book) => {
        return (
            book.title.toLowerCase().includes(searchString) || 
            book.author.toLowerCase().includes(searchString)
        );
    });
    renderBooks(filteredBooks, currentMode);
});

// Reader Logic
function openSideReader(url, title) {
    window.open(url, '_blank');
}

// Modal Logic
function openModal(book) {
    const modalBody = document.getElementById('modal-body');
    modalBody.innerHTML = `
        <img src="${book.img}" alt="Book Cover">
        <div class="modal-details">
            <h2>${book.title}</h2>
            <h4>By ${book.author} (${book.year})</h4>
            <p><strong>Category:</strong> ${book.category}</p>
            <p><strong>Continent:</strong> ${book.continent}</p>
            <br>
            <p>${book.desc}</p>
            <div class="read-link" onclick="openSideReader('${book.readUrl}', '${book.title}')">Read Book Now</div>
        </div>
    `;
    document.getElementById('bookModal').style.display = "block";
}

function closeModal() {
    document.getElementById('bookModal').style.display = "none";
}

window.onclick = function(event) {
    let modal = document.getElementById('bookModal');
    if(event.target == modal) {
        modal.style.display = "none";
    }
}

// Initial Load
renderBooks(books, 'genre');