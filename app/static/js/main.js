$(document).ready(function() {
  var page_name = document.title.split(" - ")[0];
  console.log(page_name);

  // Login Page
  if (page_name === "Login") {


  }

  // Home Page
  if (page_name === "Home") {
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

      $("#search-result").slimScroll({
          wheelStep: 3,
          alwaysVisible: true,
          railVisible: true,
          height: '400px',
      });

      $('#search-result').on("mouseover mouseout", (event) => {
        toggleClass(event.target, 'active');
      });



      // Home Page Functions
      function displayPatientsElements(patients) {
        $("#search-result").html('')
        /*
          <a href="#" target="_blank">
            <li class="list-group-item justify-content-between">
              Mohamed Sameh Rushdy
              <span>25 Years</span>
            </li>
          </a>
        */
        patients.forEach((patient) => {
          let updated_at = patient.updated_at.split("|")

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
  }

  // Analysis Profile Page
  if (page_name === "Analysis Profile") {
      console.log("Analysis Profile Page");

      $('#patient_analyzes_list').slimScroll({
          wheelStep: 3,
          alwaysVisible: true,
          railVisible: true,
          height: '400px',
      });

      $("#add_button").click((event) => {
          console.log("Form submitted");
          $("#add_cbc_analysis").submit();
          // event.preventDefault();
          // wbc = $("#wbc")
          // console.log(wbc);
      });

      // delete_patient_confirmation

      $("#delete_patient_profile").click((event) => {
          console.log("delete_patient_profile clicked");

          console.log($("#patient_id"));
          let patient_id = $("#patient_id").val()
          console.log(patient_id);
      })
  }

   if (page_name === "New Patient") {
     console.log("New Patient Page");
  }



  /* Global Functions */
  function toggleClass(item, className) {
      $(item).toggleClass(className);
  }

});
