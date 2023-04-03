// Get search form and pagination link
const searchForm = document.getElementById("searchForm");
const pageLinks = document.getElementsByClassName("page-link");

// Ensure search exists
if (searchForm) {
  for (let i = 0; pageLinks.length > i; i++) {
    pageLinks[i].addEventListener("click", function (evnt) {
      // to provide refresh the page
      evnt.preventDefault();

      // get the data attribute
      const page = this.dataset.page;

      // Add hidden search input to form
      searchForm.innerHTML += `<input value=${page} name="page" hidden />`;

      // Submit the form
      searchForm.submit();
    });
  }
}
