async function processWebsite(){

    let website=document.getElementById("urlBox").value

    document.getElementById("status").innerText="Processing..."

    let response=await fetch("http://127.0.0.1:8000/process-url",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            url:website
        })

    })

    let data=await response.json()

    document.getElementById("status").innerText=data.message
}



async function askQuestion(){

    let question=document.getElementById("questionBox").value

    let response=await fetch("http://127.0.0.1:8000/ask-question",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            question:question
        })

    })

    let data=await response.json()

    let chat=document.getElementById("chatBox")

    chat.innerHTML += `<div class="user">${question}</div>`

    chat.innerHTML += `<div class="bot">${data.answer}</div>`

    document.getElementById("questionBox").value=""
}