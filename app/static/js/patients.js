$(document).ready(()=> {
  console.log("Javascript File: Patients.js");

  $(document).on('click', '[data-delete-patient]', (event)=> {
    event.preventDefault();
    delete_patient_link = event.target
    patient_id = $(delete_patient_link).attr("data-patient-id")
    fullname = $(delete_patient_link).attr("data-patient-fullname");

    var confirm_delete_patient_modal = get_confirm_delete_patient_modal(patient_id, fullname);
    $(confirm_delete_patient_modal).modal('toggle');
  })



  // $(document).on('hidden.bs.modal', '#confirm_delete_patient_modal', (event)=> {
  //   $(event.target).remove();
  // })

  // $(document).on('submit', '#confirm_delete_patient_form', (event)=> {
  //   event.preventDefault();
  //
  //   var action_url = $(event.target).attr('action');
  //   var fullname = $(".modal-title strong").text();
  //
  //   delete_patient(action_url);
  // })
  //
  //
  // function delete_patient(action_url) {
  //   console.log(action_url);
  //
  //   $.ajax({
  //     method: "POST",
  //     url: action_url
  //   })
  //   .done((messages)=> {
  //     messages = JSON.parse(messages);
  //
  //     if ( messages.hasOwnProperty("error") ) {
  //       let errors_list = messages["error"]
  //
  //       clearAlert("#delete_patient_success")
  //       showErrorAlert("#confirm_delete_patient_error", errors_list)
  //
  //     } else if ( messages.hasOwnProperty("success") ) {
  //       success_message = messages["success"];
  //       // patient_row = $(`[data-patient-fullname="${fullname}"]`).parent().parent();
  //       // $(patient_row).remove();
  //       $("#confirm_delete_patient_modal").modal('hide');
  //       location.reload();
  //       showSuccessAlert("#delete_patient_success", success_message)
  //
  //
  //     }
  //   })
  //   .fail((err)=> {
  //     console.log("Error in ajax query: " + err.statusText);
  //   })
  // }

  // ==== Patients Page Functions ====
  // Create Alert to Display Error/Success Messages
  function showErrorAlert(alert_id, errors_list) {
    var error_alert = createErrorAlert(errors_list);
    $(alert_id).html(error_alert);
  }

  function createErrorAlert(errors_list) {
      var ul_of_errors    = $(`<ul></ul>`);

      errors_list.forEach((message) => {
          let li = $(`<li>${message}</li>`).appendTo(ul_of_errors);
      });

      var error_alert = createAlert("error", ul_of_errors);
      return error_alert;
  }

  function showSuccessAlert(alert_id, success_message) {
    var success_element = createSuccessAlert(success_message);
    $(alert_id).html($(success_element));
  }

  function createSuccessAlert(success_message) {
      var success_message = $(`<p>${success_message}</p>`)

      var success_alert = createAlert("success", success_message)
      return success_alert;
  }

  function createAlert(alert_type, alert_messages) {
      var alert = null;

      if (alert_type === "error") {
          alert = $(`
              <div class='offset-1 col-10'>
                  <div class='alert alert-danger' role='alert'>
                      ${alert_messages.html()}
                  </div>
              </div>
          `)

      } else if (alert_type === "success") {
          alert = $(`
              <div class='offset-3 col-6'>
                  <div class='alert alert-success alert-dismissible fade show' role='alert'>
                      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                          <span aria-hidden="true">&times;</span>
                      </button>
                      ${alert_messages.html()}
                  </div>
              </div>
          `);
      }

      return alert;
  }

  function clearAlert(alert_id) {
    $(alert_id).html('');
  }


  // Get a Modal for Confiming Deleting Patient
  function get_confirm_delete_patient_modal(id, fullname) {
    let modal_header = `
      <h5 class="modal-title">Delete Patient <strong>${fullname}</strong></h5>
      <button type="button" class="close" data-dismiss="modal" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    `

    let modal_body = `
      <div id="confirm_delete_patient_error" class="row"></div>
      <p>
        This will delete patient's profile and all of its analyzes,
        <strong>Are you sure?</strong>
      </p>
    `

    let modal_footer = `
      <form id='confirm_delete_patient_form' action="/patients/delete/${id}" method="POST">
        <button type="submit" class="btn btn-outline-danger">Confirm</button>
        <button type="button" class="btn btn-outline-info" data-dismiss="modal">Cancel</button>
      </form>
    `
    
    return create_modal(modal_header, modal_body, modal_footer);
  }

  function create_modal(modal_header, modal_body, modal_footer) {
    return `
      <div id="confirm_delete_patient_modal" class="modal fade">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              ${modal_header}
            </div>

            <div class="modal-body">
              ${modal_body}
            </div>

            <div class="modal-footer">
              ${modal_footer}
            </div>
          </div>
        </div>
      </div>
    `
  }
})
