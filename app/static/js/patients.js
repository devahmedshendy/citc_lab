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

  $(document).on('hidden.bs.modal', '#confirm_delete_patient_modal', (event)=> {
    $(event.target).remove();
  })

  $(document).on('submit', '#confirm_delete_patient_form', (event)=> {
    event.preventDefault();

    var action_url = $(event.target).attr('action');
    var fullname = $(".modal-title strong").text();

    delete_patient(action_url);
  })


  function delete_patient(action_url) {
    console.log(action_url);

    $.ajax({
      method: "POST",
      url: action_url
    })
    .done((messages)=> {
      messages = JSON.parse(messages);

      if ( messages.hasOwnProperty("error") ) {
        console.log("error");

      } else if ( messages.hasOwnProperty("success") ) {
        patient_row = $(`[data-patient-fullname="${fullname}"]`).parent().parent();
        $(patient_row).remove()

        $("#confirm_delete_patient_modal").modal('hide');
      }
    })
    .fail((err)=> {
      console.log("Error in ajax query: " + err.statusText);
    })
  }

  // ==== Patients Page Functions ====
  // Get a Modal for Confiming Deleting Patient
  function get_confirm_delete_patient_modal(id, fullname) {
    let header = `
      <h5 class="modal-title">Delete Patient <strong>${fullname}</strong></h5>
      <button type="button" class="close" data-dismiss="modal" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    `

    let body = `
      <p>
        This will delete patient's profile and all of its analyzes,
        <strong>Are you sure?</strong>
      </p>
    `

    let footer = `
      <form id='confirm_delete_patient_form' action="/patients/delete/${id}" method="POST">
        <button type="submit" class="btn btn-danger">Yes, Sure</button>
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
      </form>
    `
    return create_modal(header, body, footer);
  }

  function create_modal(header, body, footer) {
    return `
      <div id="confirm_delete_patient_modal" class="modal fade">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              ${header}
            </div>

            <div class="modal-body">
              ${body}
            </div>

            <div class="modal-footer">
              ${footer}
            </div>
          </div>
        </div>
      </div>
    `
  }
})
