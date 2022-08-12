document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
  document.querySelector('#emails-view').style.display = 'block';

  document.querySelector('#send').addEventListener('click', send_email);
});

function send_email() {
  fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
           recipients: document.querySelector('#compose-recipients').value,
           subject: document.querySelector('#compose-subject').value,
           body: document.querySelector('#compose-body').value
        })
     })
     .then(response => response.json())
     .then(result => {
        // Print result
        console.log(result);
        
     });
}



function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#display-email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  fetch('/emails/' + mailbox)

     .then(response => response.json())
     .then(emails => {
        // Print emails
        console.log(emails);

        for (let i = 0; i < emails.length; i++) {
           //create div
           let email_container = document.createElement('div');

           //assign class
           email_container.className = 'email_container';

           let sender = document.createElement('li');
           let subject = document.createElement('li');
           let timestamp = document.createElement('li');
           let archive = document.querySelector('#archive');

           sender.id = 'sender';

           sender.innerHTML = emails[i].sender;
           subject.innerHTML = emails[i].subject;
           timestamp.innerHTML = emails[i].timestamp;
           

           //add content
           email_container.append(sender);
           email_container.append(subject);
           email_container.append(timestamp);

           document.querySelector('#emails-view').append(email_container);

           email_container.addEventListener('click', function() {
              fetch('/emails/' + emails[i].id)
                 .then(response => response.json())
                 .then(email => {
                    // Print email
                    console.log(email);

                    if (emails[i].archived === true)
                    {
                      console.log("hello")
                      archive.InnerHTML = "Archive";
                    }
                    else
                    {
                      archive.InnerHTML = "Unarchive";
                    }

                    document.querySelector('#emails-view').style.display = 'none';
                    document.querySelector('#compose-view').style.display = 'none';
                    document.querySelector('#display-email').style.display = 'block';

                    const reply = document.querySelector('#reply');

                    reply.addEventListener('click', function() {
                     // Show compose view and hide other views
                     document.querySelector('#emails-view').style.display = 'none';
                     document.querySelector('#compose-view').style.display = 'block';
                     document.querySelector('#display-email').style.display = 'none';

                     // Clear out composition fields
                     document.querySelector('#compose-recipients').value = email.sender;
                     document.querySelector('#compose-subject').value = 'Re: ' + email.subject;
                     document.querySelector('#compose-body').value = 'On ' + email.timestamp + ' ' + email.sender + ' wrote: ' + email.body + '      Your reply: ';

                    })

                    document.querySelector('#text').innerHTML = email.body;
                    document.querySelector('#from').innerHTML = email.sender;
                    document.querySelector('#timestamp').innerHTML = email.timestamp;
                    document.querySelector('#subject').innerHTML = email.subject;
                    document.querySelector('#to').innerHTML = email.recipients;

                    archive.addEventListener('click', function() {
                      if (email.archived === false) {
                        fetch('/emails/' + email.id, {
                           method: 'PUT',
                           body: JSON.stringify({
                              archived: true
                           })
                        })
                  
                        load_mailbox('archive');

                      }  else if (email.archive === true) {
                          fetch('/emails/' + email.id, {
                            method: 'PUT',
                            body: JSON.stringify({
                                archived: false
                            })
                          })
                   
                        load_mailbox('inbox');
                     }

                    });
                 });
           });
        }
     });


  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#display-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}


