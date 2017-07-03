$(document).ready(()=> {

  //-----------------------------------------
  //
  // Handling Process of Deleting User
  //-----------------------------------------
  // Delete User Link -> Clicked
  $(document).on('click', '[data-delete-user]', (event)=> {
    event.preventDefault();
    delete_user_link = event.target;
    user_id = $(delete_user_link).attr("data-user-id");
    fullname = $(delete_user_link).attr("data-user-fullname");

    var confirm_delete_user_modal = createModalToConfirmDeleteUser(user_id, fullname);
    $(confirm_delete_user_modal).modal('toggle');
  })

  // Confirm Delete User Form -> Submitted
  // $(document).on('submit', '#confirm_delete_user_form', (event)=> {
  //   event.preventDefault();
  //
  //   var action_url = $(event.target).attr('action');
  //   var fullname = $(".modal-title strong").text();
  //
  //   deleteUser(action_url);
  // });

  //-----------------------------------------
  //
  // Handling Modal Hidden Event
  //-----------------------------------------
  // Confirm Delete User Modal -> Hidden
  // $(document).on('hidden.bs.modal', '#confirm_delete_user_modal', (event)=> {
  //   $(event.target).remove();
  // })

  //-----------------------------------------
  //
  // Users Page Functions
  //-----------------------------------------
  // Send Delete User To Server
  function deleteUser(action_url) {
    $.ajax({
      method: "POST",
      url: action_url
    })
    .done((messages)=> {
      messages = JSON.parse(messages);

      if ( messages.hasOwnProperty("error") ) {
        console.log("error");

      } else if ( messages.hasOwnProperty("success") ) {
        user_row = $(`[data-user-fullname="${fullname}"]`).parent().parent();
        // $(user_row).remove();
        location.reload();

        $("#confirm_delete_user_modal").modal('hide');
      }
    })
    .fail((err)=> {
      console.log("Error in ajax query: " + err.statusText);
    })
  }


  // Create Modal to Confirm Delete User
  function createModalToConfirmDeleteUser(id, fullname) {
    let modal_header = `
      <h5 class="modal-title">Delete User <strong>${fullname}</strong></h5>
      <button type="button" class="close" data-dismiss="modal" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    `

    let modal_body = `
      <p>Are you sure?</p>
    `

    let modal_footer = `
      <form id='confirm_delete_user_form' action="/users/delete/${id}" method="POST">
        <button type="button" name='cancel' class="btn btn-secondary" data-dismiss="modal">Cancel</button>
        <button type="submit" name='confirm' class="btn btn-danger">Confirm</button>
      </form>
    `

    let confirm_delete_user_modal =  createModal("confirm_delete_user_modal", modal_header, modal_body, modal_footer);

    return confirm_delete_user_modal;
  }


  function createModal(modal_id, modal_header, modal_body, modal_footer) {
    let modal =  $(`
      <div id="${modal_id}" class="modal fade">
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
    `);

    return modal;
  }
})
