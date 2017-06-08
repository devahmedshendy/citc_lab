$(document).ready(function() {
  var page_name = document.title.split(" - ")[0];
  console.log(page_name);

  if (page_name === "Login") {


  } else if (page_name === "Home") {
    let patients = []

    $.get('/patient?json=list_of_patients', (list_of_patients) => {
      list_of_patients = JSON.parse(list_of_patients)

      list_of_patients.forEach((patient) => {
        patients.push(patient)
      })

      displayPatientsElements(patients);
    });


    $('#search-box').on("keyup keypress", (event) => {
      let targetElement = $(event.target);

      if (targetElement.val().length > 0) {
        $('#search-result').text(event.target.value);

      } else if (targetElement.val().length === 0 && $('#search-result li').length === 0) {
        displayPatientsElements(patients);
      }

    });

    $('#search-result').on("mouseover mouseout", (event) => {
      toggleClass(event.target, 'active');
    });


    /*
      <a href="#" target="_blank">
        <li class="list-group-item justify-content-between">
          Mohamed Sameh Rushdy
          <span>25 Years</span>
        </li>
      </a>
    */
    function displayPatientsElements(patients) {
      $("#search-result").html('')

      patients.forEach((patient) => {
        let anchorElement = $("<a></a>").attr({
          "href": `/analysis/personal_id/${patient.personal_id}`
        });

        let listElement = $("<li></li>")
          .addClass("list-group-item justify-content-between border-right-0 border-left-0 border-bottom-0")
          .text(patient.name);

        let spanElement = $("<span></span>")
          .text(`${patient.updated_at}`);

        spanElement.appendTo(listElement);
        listElement.appendTo(anchorElement);

        anchorElement.appendTo("#search-result");
      });
    }

  } else if (page_name === "Analysis Profile") {
    console.log("Analysis Profile Page");

    $('#patient_analyzes_list').slimScroll({
        wheelStep: 3,
        alwaysVisible: true,
        railVisible: true,
        height: '400px',
    });

  } else if (page_name === "New Patient") {
    console.log("New Patient Page");
  }



  /* Global Functions */
  function toggleClass(item, className) {
    $(item).toggleClass(className);
  }

});
