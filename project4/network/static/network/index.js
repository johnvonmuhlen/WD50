document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#post').addEventListener('click', new_post);

    document.querySelector('#hide').addEventListener('click', hide_newpost);

    load_posts();
});

function hide_newpost()
{
    if (document.querySelector('#new_post_container').style.display === "block")
    {
        document.querySelector('#hide').innerHTML = "Unhide";
        document.querySelector('#new_post_container').style.display = "none";
    }
    else
    {
        document.querySelector('#hide').innerHTML = "Hide";
        document.querySelector('#new_post_container').style.display = "block";
    }
}

function load_posts()
{
    fetch('/posts')
    .then(response => response.json())
    .then(posts => {
    // Print emails
        console.log(posts);
    // ... do something else with emails ...
        for (let i = 0; i < posts.length; i++)
        {
            let post_container = document.createElement('div');

            post_container.id = 'post_container';
            
            let user = document.createElement('h2');
            let content = document.createElement('p');
            let like_counter = document.createElement('h3');
            //let timestamp = document.createElement('p');
            

            user.innerHTML = posts[i].user;
            content.innerHTML = posts[i].fields.content;
            like_counter.innerHTML= posts[i].fields.likes;
            //timestamp.id = posts[i].timestamp

            post_container.append(user);
            post_container.append(content);
            post_container.append(like_counter);
            
            document.querySelector('#posts').append(post_container);

        }

    });
}