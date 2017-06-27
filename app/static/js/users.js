$(document).ready(()=> {
  console.log("Javascript File: Users.js");

  // console.log( $("[data-delete-user]") );
  $(document).on('click', '[data-delete-user]', (event)=> {
    event.preventDefault();
    delete_user_link = event.target
    user_id = $(delete_user_link).attr("data-user-id")
    fullname = $(delete_user_link).attr("data-user-fullname");
    // fullname = $(delete_user_link).parent().siblings().first().text();

    var confirm_delete_user_modal = get_confirm_delete_user_modal(user_id, fullname);
    $(confirm_delete_user_modal).modal('toggle');
  })

  $(document).on('hidden.bs.modal', '#confirm_delete_user_modal', (event)=> {
    $(event.target).remove();
  })

  $(document).on('submit', '#confirm_delete_user_form', (event)=> {
    event.preventDefault();

    var action_url = $(event.target).attr('action');
    var fullname = $(".modal-title strong").text();

    delete_user(action_url);
  })


  function delete_user(action_url) {
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
        user_row = $(`[data-user-fullname="${fullname}"]`).parent().parent();
        $(user_row).remove()

        $("#confirm_delete_user_modal").modal('hide');
      }
    })
    .fail((err)=> {
      console.log("Error in ajax query: " + err.statusText);
    })
  }

  // ==== Users Page Functions ====
  // Get a Modal for Confiming Deleting User
  function get_confirm_delete_user_modal(id, fullname) {
    let header = `
      <h5 class="modal-title">Delete User <strong>${fullname}</strong></h5>
      <button type="button" class="close" data-dismiss="modal" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    `

    let body = `
      <p>Are you sure?</p>
    `

    let footer = `
      <form id='confirm_delete_user_form' action="/users/delete/${id}" method="POST">
        <button type="submit" class="btn btn-danger">Yes, Sure</button>
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
      </form>
    `
    return create_modal(header, body, footer);
  }

  function create_modal(header, body, footer) {
    return `
      <div id="confirm_delete_user_modal" class="modal fade">
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
