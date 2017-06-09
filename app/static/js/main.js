$(document).ready(function() {
    var page_name = document.title.split(" - ")[0];
    console.log(page_name);

    /* ----------
     * Login Page
     * ---------- */
    if (page_name === "Login") {

    }

    /* ---------
     * Home Page
     * --------- */
    else if (page_name === "Home") {
        displayPatientsElements('/patient/json');

        $('#search-box').on("keypress keyup", (event) => {
          let startswith_string = $(event.target).val();

          if ($("#search-box").val() !== '') {
            startswith_string.length == 0 ?
                displayPatientsElements('/patient/json') :
                displayPatientsElements(`/patient/search/json?startswith=${startswith_string}`)
          }
        });

        // Enable scroll bar for Patient Search Result
        $("#search-result").slimScroll({
            wheelStep: 3,
            alwaysVisible: true,
            railVisible: true,
            height: '400px',
        });

        $('#search-result').on("mouseover mouseout", (event) => {
          toggleClass(event.target, 'active');
        });


        /* Home Page Functions */
        function sendGetPatientsListRequest(uri) {
          return new Promise((resolve, reject) => {
              $.get(uri, (res) => {
                  var patients = [];
                  res = JSON.parse(res);

                  res.forEach((patient) => {
                    patients.push(patient);
                  });

                  resolve(patients);
              })
              .fail((err) => {
                  reject(err)
              })
          })
        }

        function displayPatientsElements(uri) {
          $("#search-result").html('');
          sendGetPatientsListRequest(uri)
            .then((patients) => {
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
                    .addClass("list-group-item justify-content-between "
                            + "border-right-0 border-left-0 border-bottom-0")
                    .text(patient.name);

                  let spanElement = $("<span></span>")
                    .text(`${patient.updated_at}`);

                  spanElement.appendTo(listElement);
                  listElement.appendTo(anchorElement);
                  anchorElement.appendTo("#search-result");
                });
            })
            .catch((err) => {
                console.log(err);
            });
        }
    }

    /* ------------------------
     * Patient Analysis Profile
     * ------------------------ */
    else if (page_name === "Analysis Profile") {
        console.log("Analysis Profile Page");

        // Enable scroll bar for Analyzes List
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

    /* ----------------
     * New Patient Page
     * ---------------- */
    else if (page_name === "New Patient") {
       console.log("New Patient Page");
    }



  /* Global Functions */
  function toggleClass(item, className) {
      $(item).toggleClass(className);
  }

});
