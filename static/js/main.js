
//Getting Search Form and Page Link
let searchForm = document.getElementById('searchForm')
let pageLinks = document.getElementsByClassName('page-link')

// Checking if we have Serach Form or not
if (searchForm) {
    for(let i = 0; pageLinks.length > i; i++ ){
        pageLinks[i].addEventListener('click', function (e) {
            e.preventDefault()
        
            // Get the Data Attribute
            let page = this.dataset.page

            //Add hidden Search input to form
            searchForm.innerHTML += `<input value=${page} name="page" hidden/>`
            
            ///Submit Form
            searchForm.submit()
        })
    }
}