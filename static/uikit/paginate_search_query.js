
// Get search forms and page links (ie pagination buttons)
let searchForm  = document.getElementById('searchForm');
let pageLinks = document.getElementsByClassName('page-link');
// console.log(pageLinks)
// Ensure search form exists
if(searchForm){
    for(let i=0; i<pageLinks.length;i++){
        pageLinks[i].addEventListener('click',function(e){
            e.preventDefault();
            
            // Get the data attribute
            let page = this.dataset.page;
            // console.log("Page: ",page);

            // Add hidden search input to forms
            searchForm.innerHTML += `<input value=${page} name='page' hidden />`
            
            // submit form
            searchForm.submit()

        })
    }

}