$(document).ready(()=> {
    // === Home Page Initialization ====
    displayPatientsElements('/patient/json');

    $("#search-result").slimScroll({
        wheelStep: 3,
        alwaysVisible: true,
        railVisible: true,
        height: '400px',
    });


    // === Home Page Event Handlers ====
    $('#search-box').on("keypress keyup", (event) => {
      let startswith_string = $(event.target).val();

      if ($("#search-box").val() !== '') {
        startswith_string.length == 0 ?
            displayPatientsElements('/patient/json') :
            displayPatientsElements(`/patient/search/json?startswith=${startswith_string}`)
      }
    });

    $('#search-result').on("mouseover mouseout", (event) => {
      $(event.target).toggleClass('active');
    });


    // === Home Page Functions ====
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
})
